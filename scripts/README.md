# Execução e conferência dos dados

Com o ambiente virtual ativo, executo o notebook pela raiz:

```powershell
python scripts/executar_notebook.py
```

Salvo a cópia com saídas em `results/reports/predicao_uti_pediatrica_executado.ipynb`. Preservo a execução parcial em caso de erro e mantenho o notebook de origem sem saídas.

Antes da execução, mantenho `srag_pediatrico_filtrado.csv` em `data/raw/`. Não distribuo essa base com o código.

## Conferência opcional da origem

Quando disponho também de `INFLUD19_PE.csv`, utilizo:

```powershell
python scripts/verificar_origem.py --source "CAMINHO/INFLUD19_PE.csv"
```

Esse comando requer os dois CSVs locais: o arquivo de origem indicado por `--source` e o recorte em `data/raw/`. Guardo o relatório agregado em `results/diagnostics/`. Essa conferência é opcional e não integra o treinamento do notebook.
