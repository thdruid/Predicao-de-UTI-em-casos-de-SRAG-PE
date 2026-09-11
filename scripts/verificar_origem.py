"""Confere o recorte local com a preparação identificada na Entrega 1."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

parser=argparse.ArgumentParser()
parser.add_argument('--source', required=True, type=Path)
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
source=pd.read_csv(args.source,sep=';',encoding='latin1',low_memory=False)
cut=pd.read_csv(root/'data/raw/srag_pediatrico_filtrado.csv',low_memory=False)
age=np.select([source.TP_IDADE==3,source.TP_IDADE==2,source.TP_IDADE==1],
              [source.NU_IDADE_N,source.NU_IDADE_N/12,source.NU_IDADE_N/365],default=np.nan)
source=source.assign(IDADE_ANOS=age)
expected=source.loc[(source.IDADE_ANOS<=12)&source.UTI.isin([1,2])].copy().reset_index(drop=True)
expected['UTI_BIN']=(expected.UTI==1).astype(int)
rmr=['RECIFE','JABOATAO DOS GUARARAPES','OLINDA','PAULISTA','CAMARAGIBE',
     'CABO DE SANTO AGOSTINHO','SAO LOURENCO DA MATA','IGARASSU','ABREU E LIMA',
     'IPOJUCA','ARACOIABA','ITAPISSUMA','ILHA DE ITAMARACA','MORENO']
expected['REGIAO']=expected.ID_MN_RESI.map(lambda x:'RMR' if str(x).upper().strip() in rmr else 'Interior de PE')
cols=[c for c in cut if c!='IDADE_ANOS']
same=(expected[cols].fillna('<NA>').astype(str)==cut[cols].fillna('<NA>').astype(str))
result={'source_file':args.source.name,'source_sha256':hashlib.sha256(args.source.read_bytes()).hexdigest(),
        'source_rows':len(source),'cut_rows':len(cut),'columns':len(cut.columns),
        'other_columns_equal_in_order':bool(same.all().all()),
        'age_equal_with_float_tolerance':bool(np.allclose(expected.IDADE_ANOS,cut.IDADE_ANOS)),
        'different_cells_excluding_age':int((~same).sum().sum()),
        'duplicate_notification_ids':int(cut.NU_NOTIFIC.duplicated().sum()),
        'notification_years':{str(k):int(v) for k,v in pd.to_datetime(cut.DT_NOTIFIC).dt.year.value_counts().items()}}
out=root/'results/diagnostics';out.mkdir(exist_ok=True)
(out/'origem.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
assert result['other_columns_equal_in_order'] and result['age_equal_with_float_tolerance']
