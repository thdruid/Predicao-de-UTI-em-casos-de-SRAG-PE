# Execução e diagnósticos

Com o ambiente virtual ativo, executo o notebook pela raiz:

```powershell
python scripts/executar_notebook.py
```

Salvo a cópia com saídas em `results/reports/predicao_uti_pediatrica_executado.ipynb`. Preservo a execução parcial em caso de erro e mantenho o notebook de origem sem saídas.

Para investigar diferenças, utilizo:

- `investigar_reprodutibilidade.py`: repito ajustes, verifico convergência e meço empates; com `--tree-search`, repito a busca da Árvore.
- `comparar_desempates.py`: reaplico a seleção de vizinhos às distâncias geradas com `--save-distances`.
- `verificar_origem.py --source CAMINHO`: confiro a reconstrução do recorte a partir de `INFLUD19_PE.csv`.

Guardo os diagnósticos em `results/diagnostics/`.
