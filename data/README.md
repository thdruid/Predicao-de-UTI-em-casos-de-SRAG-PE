# Dados locais

Organizo meus arquivos de dados em `raw/` (entrada), `processed/` (base limpa opcional) e `reference/` (referências históricas). O recorte `raw/srag_pediatrico_filtrado.csv` é versionado com o código; outras bases e exportações permanecem ignoradas. Documento a procedência disponível em [docs/dataset.md](../docs/dataset.md).

## Entrada esperada

Leio `raw/srag_pediatrico_filtrado.csv` com separador de vírgulas. Utilizo estas colunas:

- Limpeza e alvo: `UTI`, `SUPORT_VEN`, `EVOLUCAO`, `UTI_BIN`.
- Demografia: `IDADE_ANOS`, `CS_SEXO`, `REGIAO`.
- Sintomas: `FEBRE`, `TOSSE`, `GARGANTA`, `DISPNEIA`, `DESC_RESP`, `SATURACAO`, `DIARREIA`, `VOMITO`.
- Comorbidades: `CARDIOPATI`, `ASMA`, `DIABETES`, `NEUROLOGIC`, `SIND_DOWN`, `HEMATOLOGI`, `HEPATICA`, `PNEUMOPATI`, `IMUNODEPRE`, `RENAL`, `OBESIDADE`.

Espero alvo 0/1, sexo F/M e sintomas 1/2/9, que recodifico para 1/0/ausente. Nas comorbidades, recodifico apenas 1 como presença. Registro essas expectativas como comportamento do código, não como dicionário oficial da fonte.

Mantenho bases brutas, exportações e arquivos não autorizados ignorados pelo Git, com documentação separada. O recorte público deste projeto possui uma exceção explícita no `.gitignore`.
