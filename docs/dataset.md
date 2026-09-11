# Dados utilizados

Utilizo `srag_pediatrico_filtrado.csv` como entrada do estudo. Preparei essa versão a partir dos dados de SRAG, com filtragem e tratamento de problemas dos dados. Não a apresento como cópia intacta do arquivo oficial e não a distribuo com o código.

## Preparação e conferência

Reconstruí o recorte a partir do arquivo local `INFLUD19_PE.csv` e da preparação registrada na Entrega 1. Dos 2.628 registros da entrada, obtive 2.133 registros e 197 colunas, na mesma ordem do CSV pediátrico.

- Converto idade em meses para anos dividindo por 12 e idade em dias dividindo por 365; mantenho idade já informada em anos.
- Mantenho idade até 12 anos e valores conhecidos de UTI (1 ou 2).
- Defino `UTI_BIN=1` para `UTI=1` e `UTI_BIN=0` para `UTI=2`.
- Uso a lista de municípios da RMR da Entrega 1 para definir `REGIAO`; classifico os demais como `Interior de PE`. Reconheço que essa regra não verifica isoladamente a UF dos municípios fora da lista.

Na versão utilizada nos experimentos, conferi a correspondência desse recorte com o arquivo local de origem. Essa conferência não estabelece igualdade com a versão atualmente disponível no portal. Não encontrei números de notificação duplicados.

Também trabalhei no tratamento de valores ausentes e de outros problemas ao longo da preparação e da modelagem. Distingo o CSV de entrada da matriz usada pelos modelos: o CSV ainda contém valores ausentes, que trato no pipeline. Nos sintomas, recodifico 1 para presença, 2 para ausência e 9 para ausente; preservo campos vazios para imputação. Nas comorbidades, recodifico apenas 1 como presença e os demais valores como zero. Ajusto a imputação durante o treino de cada fold, conforme o notebook.

## Características da entrada

Encontrei 2.030 registros com alvo zero e 103 com alvo um. Nas datas de notificação, identifiquei 2.119 registros de 2019 e 14 de 2020. Não interpreto o nome INFLUD19 como garantia de que todas as notificações sejam de 2019.

Identifiquei números de notificação, datas de nascimento e atendimento e campos de localização. Por isso, não trato a inspeção estrutural como anonimização. `TEM_CPF` é um indicador e não comprova, pelo nome, a presença de números de CPF.

## Origem, licença e disponibilidade

A fonte informada para o trabalho é o Ministério da Saúde — [OpenDataSUS, SIVEP-Gripe / SRAG](https://dadosabertos.saude.gov.br/dataset/srag-2019-a-2026). O portal disponibiliza dados para download e informa que suas bases passam por anonimização. Não uso essa informação como certificação da versão que preparei.

Não confirmei uma licença específica aplicável à redistribuição desta versão derivada. Por isso, mantenho o CSV apenas localmente e disponibilizo o código, os resultados agregados e a descrição das transformações. Não atribuo automaticamente ao dataset a licença indicada para o conteúdo do site.

Para executar o notebook, utilizo uma cópia local em `data/raw/srag_pediatrico_filtrado.csv`, com o formato descrito em [data/README.md](../data/README.md). O link do portal identifica a fonte informada; não garante que um download atual corresponda exatamente à versão dos experimentos.

**Atribuição:** Ministério da Saúde — OpenDataSUS, Sistema de Informação da Vigilância Epidemiológica da Gripe (SIVEP-Gripe), base de Síndrome Respiratória Aguda Grave (SRAG). Disponível em: https://dadosabertos.saude.gov.br/dataset/srag-2019-a-2026.

Registro o SHA-256 do CSV pediátrico como `bd6ae623ddc8370bd8d2933c2d888ad360beff2c24a88209572979fc42f8c2a9` e o de `INFLUD19_PE.csv` como `5b2c6fda9f38b2d5244ba7f035cc1bf99f94c73e54ed867886808c96390181d7`.

Utilizo `scripts/verificar_origem.py --source CAMINHO/INFLUD19_PE.csv` para repetir a conferência local. Descrevo as colunas exigidas em [data/README.md](../data/README.md).
