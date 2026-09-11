"""Reaplica argpartition às mesmas distâncias locais, sem recalculá-las."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np

parser=argparse.ArgumentParser()
parser.add_argument('--label',required=True)
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]/'results/diagnostics'
means=[]
hashes=[]
for file in sorted((root/'distances').glob('*.npz')):
    data=np.load(file)
    dist,values,k=data['dist'],data['values'],int(data['k'])
    hashes.append(hashlib.sha256(dist.tobytes()).hexdigest())
    selected=np.argpartition(dist,k-1,axis=1)[:,:k]
    means.extend(values[selected].mean(axis=1).tolist())
if not means:
    raise RuntimeError('Execute investigar_reprodutibilidade.py --save-distances primeiro.')
(root/f'ties_{args.label}.json').write_text(json.dumps({'distance_hashes':hashes,'means':means}),encoding='utf-8')
print('Saved',args.label,len(means))
