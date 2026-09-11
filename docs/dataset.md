# Dados utilizados

Utilizo `srag_pediatrico_filtrado.csv` como entrada do estudo. Ele é um recorte derivado da base pública de SRAG/SIVEP-Gripe do Ministério da Saúde, disponibilizada no portal OpenDataSUS.

## Preparação e conferência

Reconstruí o recorte a partir do arquivo local `INFLUD19_PE.csv` e da preparação registrada na Entrega 1. Dos 2.628 registros da entrada, obtive 2.133 registros e 197 colunas, na mesma ordem do CSV pediátrico.

- Converto idade em meses para anos dividindo por 12 e idade em dias dividindo por 365; mantenho idade já informada em anos.
- Mantenho idade até 12 anos e valores conhecidos de UTI (1 ou 2).
- Defino `UTI_BIN=1` para `UTI=1` e `UTI_BIN=0` para `UTI=2`.
- Uso a lista de municípios da RMR da Entrega 1 para definir `REGIAO`; classifico os demais como `Interior de PE`. Reconheço que essa regra não verifica isoladamente a UF dos municípios fora da lista.

Conferi igualdade nas 196 colunas diferentes de idade, após normalização para texto, e igualdade de idade com tolerância de ponto flutuante. Não encontrei números de notificação duplicados.

## Características da entrada

Encontrei 2.030 registros com alvo zero e 103 com alvo um. Nas datas de notificação, identifiquei 2.119 registros de 2019 e 14 de 2020. Não interpreto o nome INFLUD19 como garantia de que todas as notificações sejam de 2019.

Identifiquei números de notificação, datas de nascimento e atendimento e campos de localização. Por isso, não trato a inspeção estrutural como anonimização. `TEM_CPF` é um indicador e não comprova, pelo nome, a presença de números de CPF.

## Origem, licença e disponibilidade

A fonte declarada é o Ministério da Saúde — [OpenDataSUS, SIVEP-Gripe / SRAG](https://dadosabertos.saude.gov.br/dataset/srag-2019-a-2026). O portal disponibiliza os dados abertos para download, inclusive em CSV, e informa que as bases publicadas passam por anonimização em conformidade com a LGPD. A página da base indica licença Creative Commons Atribuição; a redistribuição deve manter essa atribuição e o link para a fonte oficial.

O arquivo deste repositório não é o bruto baixado do portal: é o recorte `srag_pediatrico_filtrado.csv`, preparado a partir de `INFLUD19_PE.csv` conforme os filtros descritos acima. Não adicionei informações identificáveis ao recorte.

**Atribuição:** Ministério da Saúde — OpenDataSUS, Sistema de Informação da Vigilância Epidemiológica da Gripe (SIVEP-Gripe), base de Síndrome Respiratória Aguda Grave (SRAG). Disponível em: https://dadosabertos.saude.gov.br/dataset/srag-2019-a-2026.

Registro o SHA-256 do CSV pediátrico como `bd6ae623ddc8370bd8d2933c2d888ad360beff2c24a88209572979fc42f8c2a9` e o de `INFLUD19_PE.csv` como `5b2c6fda9f38b2d5244ba7f035cc1bf99f94c73e54ed867886808c96390181d7`.

Utilizo `scripts/verificar_origem.py --source CAMINHO/INFLUD19_PE.csv` para repetir a conferência local. Descrevo as colunas exigidas em [data/README.md](../data/README.md).
