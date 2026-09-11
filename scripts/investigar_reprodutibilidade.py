"""Diagnóstico local: usa o código do notebook sem reexecutar buscas completas."""
import argparse
import contextlib
import hashlib
import io
import json
import sys
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--label', default='atual')
parser.add_argument('--numpy-path')
parser.add_argument('--save-distances', action='store_true')
parser.add_argument('--tree-search', action='store_true')
args = parser.parse_args()
if args.numpy_path:
    sys.path.insert(0, str(Path(args.numpy_path).resolve()))

import numpy as np
import pandas as pd
import sklearn
from sklearn.impute import KNNImputer
from sklearn.base import clone
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.model_selection import cross_validate
from threadpoolctl import threadpool_limits, threadpool_info


def digest(a):
    return hashlib.sha256(np.asarray(a).tobytes()).hexdigest()


def main():
    notebook = json.loads((ROOT/'notebooks/modeling/predicao_uti_pediatrica.ipynb').read_text(encoding='utf-8'))
    ns = {'display': lambda *a, **k: None}
    with contextlib.redirect_stdout(io.StringIO()):
        for i in [2,6,8,10,12,14,18,27,29,31,33]:
            exec(''.join(notebook['cells'][i]['source']), ns)
    train,test,yt,yv = [ns[x] for x in ['X_treino','X_teste','y_treino','y_teste']]
    original=json.loads((ROOT/'data/reference/dados_relatorio_entrega3.json').read_text(encoding='utf-8'))
    atual=json.loads((ROOT/'results/reports/resumo_experimentos.json').read_text(encoding='utf-8'))
    result={'numpy':np.__version__,'pandas':pd.__version__,'sklearn':sklearn.__version__,
            'csv_sha256':hashlib.sha256((ROOT/'data/raw/srag_pediatrico_filtrado.csv').read_bytes()).hexdigest(),
            'train_indices_sha256':digest(train.index), 'test_indices_sha256':digest(test.index),
            'threadpools':threadpool_info(),'runs':[]}
    # Mede empates na escolha do quinto vizinho sem alterar o método original.
    tie_stats = []
    original_calc = KNNImputer._calc_impute
    def audit_calc(self, dist, k, values, masks):
        if args.save_distances:
            folder=ROOT/'results/diagnostics/distances'
            folder.mkdir(parents=True,exist_ok=True)
            np.savez(folder/f'{len(tie_stats)}.npz',dist=dist,values=values,k=k)
        partition = np.argpartition(dist, k - 1, axis=1)[:, :k]
        stable = np.argsort(dist, axis=1, kind='stable')[:, :k]
        sorted_dist = np.sort(dist, axis=1)
        boundary = sorted_dist[:, k - 1]
        equal = dist == boundary[:, None]
        less = (dist < boundary[:, None]).sum(axis=1)
        crossing = equal.sum(axis=1) > (k - less)
        differing = []
        for row, mask in enumerate(equal):
            differing.append(bool(crossing[row] and np.unique(values[mask]).size > 1))
        different_means = np.abs(values[partition].mean(axis=1)-values[stable].mean(axis=1)) > 1e-12
        tie_stats.append({'missing_cells':int(len(dist)), 'boundary_ties':int(crossing.sum()),
                          'ties_with_different_values':sum(differing),
                          'different_imputation_with_stable_sort':int(different_means.sum())})
        return original_calc(self, dist, k, values, masks)
    KNNImputer._calc_impute = audit_calc
    try:
        ns['construir_pipeline_oficial'](DecisionTreeClassifier()).named_steps['preprocessor'].fit_transform(train, yt)
    finally:
        KNNImputer._calc_impute = original_calc
    result['imputation_ties'] = tie_stats
    for repetition in range(2):
        for source,report in [('original',original),('atual',atual)]:
            tree=next(r for r in report['teste_final'] if 'min_samples_leaf' in str(r['best_params']))
            pipe=ns['construir_pipeline_oficial'](DecisionTreeClassifier(random_state=42))
            pipe.set_params(**tree['best_params'])
            with warnings.catch_warnings(record=True) as captured:
                warnings.simplefilter('always')
                pipe.fit(train,yt)
            pre=pipe.named_steps['preprocessor'].transform(train)
            pred=pipe.predict(test)
            selector=pipe.named_steps['selector']
            run={'repeat':repetition,'tree_params':source,'f1':f1_score(yv,pred),
                 'confusion':confusion_matrix(yv,pred).tolist(),'pre_sha256':digest(pre),
                 'chi2':np.round(selector.scores_[selector.get_support()],2).tolist(),
                 'pred_sha256':digest(pred),'warnings':[str(w.message) for w in captured]}
            result['runs'].append(run)
            print(args.label,run,flush=True)
    params=original['hiperparametros']['Regressão Logística']
    lr=ns['construir_pipeline_oficial'](LogisticRegression(random_state=42)).set_params(**params)
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter('always')
        cv=cross_validate(lr,train,yt,cv=ns['cv_5fold'],scoring=ns['METRICAS'],return_estimator=True,n_jobs=1,error_score='raise')
        lr.fit(train,yt)
    result['logistic']={'n_iter_full':lr.named_steps['estimador'].n_iter_.tolist(),
        'n_iter_folds':[m.named_steps['estimador'].n_iter_.tolist() for m in cv['estimator']],
        'cv_f1':cv['test_f1'].tolist(),'test_f1':f1_score(yv,lr.predict(test)),
        'warnings':sorted(set(str(w.message) for w in captured))}
    if args.tree_search:
        from sklearn.model_selection import RandomizedSearchCV
        from joblib import parallel_config
        import ast
        # Reutiliza a grade original sem executar a chamada da célula.
        assignment=ast.parse(''.join(notebook['cells'][60]['source'])).body[0]
        grid=ast.literal_eval(assignment.value)
        search=RandomizedSearchCV(ns['construir_pipeline_oficial'](DecisionTreeClassifier(random_state=42)),
            {'estimador__'+k:v for k,v in grid.items()},n_iter=50,scoring=ns['METRICAS'],refit='f1',
            cv=ns['cv_5fold'],random_state=42,n_jobs=2,error_score='raise')
        print('Repeating tree search: 250 fits',flush=True)
        with parallel_config(backend='loky',inner_max_num_threads=1,max_nbytes=None):
            search.fit(train,yt)
        result['tree_search']={'best_params':search.best_params_,'cv_f1':search.best_score_,
            'test_f1':f1_score(yv,search.predict(test)),
            'confusion':confusion_matrix(yv,search.predict(test)).tolist()}
    out=ROOT/'results/diagnostics';out.mkdir(exist_ok=True)
    (out/f'{args.label}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print('SAVED',args.label,flush=True)


if __name__=='__main__':
    with threadpool_limits(limits=1):
        main()
