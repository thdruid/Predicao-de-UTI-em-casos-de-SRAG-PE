# Execução e resultados

Apresento os resultados obtidos na avaliação dos modelos. Registro as versões do ambiente em [config/environment](../config/environment/README.md).

## Dados e avaliação

Utilizei 2.050 registros após a limpeza, divididos em 1.640 para treino e 410 para teste. O treino contém 82 positivos; o teste, 21. Mantive a semente 42 e a divisão estratificada.

## Resultados no teste

| Modelo | F1 | Recall | Precisão | Acurácia |
| --- | --- | --- | --- | --- |
| Árvore de Decisão | 0,2198 | 0,4762 | 0,1429 | 0,8268 |
| SVM | 0,1739 | 0,9524 | 0,0957 | 0,5366 |
| Regressão Logística | 0,1579 | 0,8571 | 0,0870 | 0,5317 |
| Rede Neural — MLP | 0,1238 | 0,6190 | 0,0688 | 0,5512 |
| KNN — pipeline Entrega 2 | 0,1176 | 0,1429 | 0,1000 | 0,8902 |
| Naive Bayes | 0,1176 | 0,0952 | 0,1538 | 0,9268 |
| Baseline — classe majoritária | 0,0000 | 0,0000 | 0,0000 | 0,9488 |

## Árvore de Decisão

Na busca, obtive `criterion=gini`, `max_depth=5`, `min_samples_split=20`, `min_samples_leaf=10` e `class_weight=None`. Na validação, obtive F1 médio de 0,1355 e desvio-padrão de 0,0243.

No teste, obtive TN=329, FP=60, FN=11 e TP=10. Por isso, interpreto o F1 de 0,2198 junto da precisão de 0,1429 e do recall de 0,4762, considerando os poucos positivos e os falsos alertas.

## Referências históricas

Mantenho o KNN da Entrega 2 como referência histórica: F1 de validação 0,1494 ± 0,0913. Não uso essa referência para afirmar que ele venceu uma comparação controlada no mesmo treino dos demais modelos.
