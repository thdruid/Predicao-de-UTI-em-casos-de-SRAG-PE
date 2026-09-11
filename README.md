# Predição de UTI pediátrica em casos de SRAG-PE

Neste projeto, estudo a classificação do registro de internação em UTI (`UTI_BIN`) em casos pediátricos de SRAG em Pernambuco. Desenvolvi o trabalho na disciplina de **Aprendizado de Máquinas e Ciência de Dados**, em **grupo de cinco pessoas**.

Apresento os resultados obtidos neste estudo acadêmico exploratório. Não validei o modelo para uso clínico.

## Minha contribuição

- Realizei a limpeza para tratar vazamento de dados (*data leakage*).
- Tratei os valores nulos.
- Executei o baseline.
- Desenvolvi a etapa de Árvore de Decisão.

## Dados

Utilizo o arquivo `srag_pediatrico_filtrado.csv`, derivado do arquivo local `INFLUD19_PE.csv`. Na preparação da Entrega 1, usamos idade até 12 anos e mantivemos os registros com UTI conhecida. Reconstruí esse recorte e conferi sua correspondência com os dados utilizados na análise.

Trabalho com 2.133 registros e 197 colunas na entrada. Após as regras de limpeza da Entrega 2, utilizo 2.050 registros e 22 atributos: 1.947 casos sem UTI e 103 com UTI. As datas de notificação do recorte incluem 2019 e 2020.

**Fonte dos dados:** Ministério da Saúde, [OpenDataSUS — SIVEP-Gripe / SRAG](https://dadosabertos.saude.gov.br/dataset/srag-2019-a-2026). O arquivo do projeto é um recorte derivado da base pública, preparado para este estudo. Os dados publicados no portal são disponibilizados como dados abertos e passam por processo de anonimização informado pelo Ministério da Saúde. Consulte [docs/dataset.md](docs/dataset.md) para a origem, os filtros, a atribuição e as colunas utilizadas.

## Metodologia

No trabalho em grupo, seguimos estas etapas:

1. Carregamos a base e verificamos as colunas esperadas.
2. Aplicamos as regras de exclusão da Entrega 2: suporte ventilatório invasivo sem UTI e óbito sem UTI.
3. Selecionamos idade, sexo, região, sintomas e comorbidades e recodificamos os indicadores.
4. Dividimos os dados em 80% treino e 20% teste, com estratificação e semente 42.
5. Utilizamos imputação e codificação → `SelectKBest(chi2, k=10)` → `SMOTE` → `RobustScaler` → classificador.
6. Buscamos hiperparâmetros com `RandomizedSearchCV` e validação cruzada estratificada de cinco folds no treino, priorizando F1.
7. Avaliamos os modelos no teste com F1, recall, precisão, acurácia e matrizes de confusão.

No pré-processamento, usamos `KNNImputer` nos blocos numérico e binário, moda para categorias ausentes e `OneHotEncoder` para região. Mantemos o SMOTE dentro do pipeline, aplicado ao treino de cada fold.

## Modelos utilizados no trabalho

| Modelo | Papel |
| --- | --- |
| DummyClassifier | Baseline de classe majoritária |
| KNeighborsClassifier | Referência da Entrega 2 e avaliação no teste |
| Regressão Logística | Comparação com busca de hiperparâmetros |
| Naive Bayes gaussiano | Comparação com busca de suavização |
| Árvore de Decisão | Comparação com busca de profundidade e parâmetros de divisão |
| SVM | Comparação de kernels linear e RBF |
| Rede Neural MLP | Comparação de arquiteturas e parâmetros de treinamento |

## Resultados

Obtive os valores abaixo no conjunto de teste, com 410 registros e 21 casos positivos:

| Modelo | F1 | Recall | Precisão | Acurácia |
| --- | --- | --- | --- | --- |
| Árvore de Decisão | 0,2198 | 0,4762 | 0,1429 | 0,8268 |
| SVM | 0,1739 | 0,9524 | 0,0957 | 0,5366 |
| Regressão Logística | 0,1579 | 0,8571 | 0,0870 | 0,5317 |
| Rede Neural — MLP | 0,1238 | 0,6190 | 0,0688 | 0,5512 |
| KNN — pipeline Entrega 2 | 0,1176 | 0,1429 | 0,1000 | 0,8902 |
| Naive Bayes | 0,1176 | 0,0952 | 0,1538 | 0,9268 |
| Baseline — classe majoritária | 0,0000 | 0,0000 | 0,0000 | 0,9488 |

A Árvore de Decisão apresentou o maior F1 observado no teste (**0,2198**). Ela identificou 10 dos 21 positivos e gerou 60 falsos positivos. Descrevo esse ranking como resultado da avaliação; não o interpreto como validação independente de uma escolha posterior de modelo.

Na validação cruzada, a Árvore obteve F1 médio de **0,1355 ± 0,0243**. Mantenho o KNN da Entrega 2 identificado como referência histórica, pois sua métrica não foi recalculada no mesmo particionamento dos demais experimentos.

Registro os hiperparâmetros e as métricas em [docs/execucao.md](docs/execucao.md).

## Limitações

- Predigo o registro de internação, não a necessidade clínica de UTI.
- Reconheço que excluir casos com base em ventilação e evolução pode introduzir viés de seleção.
- Não considero as referências históricas da Entrega 2 diretamente comparáveis à validação atual.
- Não realizei validação cruzada aninhada nem validação externa.
- Reconheço a incerteza decorrente de apenas 21 positivos no teste e a baixa precisão dos modelos.
- Mantenho como limitações a recodificação de comorbidades ausentes como zero e a interpolação de indicadores pelo SMOTE.
- Não garanto resultados idênticos entre ambientes apenas pela semente ou pelas versões dos pacotes.

## Organização

Organizei os arquivos por finalidade:

```text
README.md
requirements.txt
config/environment/       # versões e dependências
data/raw/                 # CSV de entrada e recorte dos dados públicos
data/processed/           # exportação opcional da base limpa
data/reference/           # referências históricas locais
docs/                     # autoria, dados e resultados
notebooks/modeling/       # notebook principal
scripts/                  # execução e diagnósticos
results/tables/           # tabelas geradas
results/reports/          # relatórios e cópias executadas
results/figures/          # figuras geradas
```

## Execução local

Para executar localmente com Python 3.12 no Windows, utilizo os comandos abaixo na raiz:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r config/environment/requirements-windows-py312.txt
python scripts/executar_notebook.py
```

Mantenho o CSV em `data/raw/srag_pediatrico_filtrado.csv`. Para execução interativa, uso `python -m jupyterlab` e abro `notebooks/modeling/predicao_uti_pediatrica.ipynb`.

Guardo a cópia executada e os arquivos gerados em `results/`, fora do Git. O notebook principal permanece sem saídas. Registro as versões utilizadas em [config/environment](config/environment/README.md).
