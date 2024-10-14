# SISTEMA PARA APROVAÇÃO DE PROJETOS URBANOS EM CANELA
#### v0.1
## Introdução
Sob o contexto de uma suposta ausência de critério para compensação ambiental em ambientes urbanos, a proposta do trabalho a seguir é descrever a metodologia do desenvolvimento de um sistema para aprovação de projetos na cidade de Canela. O presente artigo busca apresentar a situação atual do trabalho corrente, servindo como recurso para consulta e atualização durante a construção do sistema.

## Materiais e métodos
### Heat Mitigation Index
O Heat Mitigation Index (HMI) do modelo InVEST (Integrated Valuation of Ecosystem Services and Tradeoffs) é uma ferramenta que avalia a capacidade das áreas verdes e do solo em mitigar o calor urbano. Esse índice é útil para o planejamento urbano sustentável, ao identificar áreas de maior necessidade de vegetação para redução de ilhas de calor. 
O indicador do HMI é um valor entre 0 a 1, estando os valores positivos atrelados a magnitude do impacto em cada pixel relativo às massas vegetadas próximas, e negativos o quanto mais distantes dessas massas vegetadas.
Os parâmetros para execução do modelo dependem de 4 dados de entrada, sendo o mapa de uso do solo em formato TIF, evapotranspiração (TIF), área de interesse (SHP) e tabela biofísica (CSV), onde serão determinados os pesos de cada classe de uso do solo para cada condicional, sendo elas:
* **lucode**: *int* – Código da classe de uso do solo
* **kc**: *float* – Coeficiente de colheita (razão de evapotranspiração para o tipo de vegetação)
* **green_area**: *int* – Valor booleano de identificação se classe é **vegetação** (1) ou **não-vegetação** (0)
* **shade**: *float* – Proporção de área da classe coberta por dossel de árvores de pelo menos 2 metros de altura
* **albedo**: *float* – Proporção de radiação solar refletida pela superfície da classe de uso do solo
* **building_intensity**: *float* – Razão de área construída pela área total


Essas condicionais devem ser avaliados de acordo com cada classe de uso do solo. A classificação do uso do solo deve especificar suas classes considerando essas condicionais como fator de impacto. Agregado à esses dados de entrada, complementa-se ao modelo dados de referência das condições meteorológicas da área de estudo, sendo elas:
* **Reference Air Temperature** (ºC) - Temperatura média  de referência em área rural, onde o efeito de ilha de calor urbana não é observado
* **UHI Effect** (ºC) - Urban Heat Island. Diferença entre  temperatura média de áreas rurais e temperatura máxima observada em áreas urbanas.
* **Air Blending Distance** (m) - Raio sobre o qual se calcula a média das temperaturas do ar para contabilizar a mistura do ar.
* **Maximum Cooling Distance** (m) - Distância sobre quais áreas verdes maiores que 2 ha possuem efeito de resfriamento
* **Cooling Capacity Method** (booleano) - Método de predição da temperatura do ar. Daytime x Nighttime

### NDVI
### Classificação não-supervisionada de Uso do Solo
Visto os problemas de classificação generalizada do MapBiomas, optou-se pela classificação do uso e superfície do solo a partir da Ortofoto disponível na plataforma [SIGWEB](https://canela.ctmgeo.com.br) de Canela.
### Fluxograma do processo
![alt text](<NTU - Dashboard Canela - Quadro 3.jpg>)

![alt text](<NTU - Dashboard Canela - Quadro 4.jpg>)
