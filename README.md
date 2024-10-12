# Ingestão de Dados por API em ambiente Cloud (GCP) - Camada RAW

O objetivo deste projeto é desenvolver uma automação que colete dados relacionado as moedas por meio de uma API e armazene esses dados em uma camada raw, visando uma evolução para aspectos analíticos (será explorado nos futuros projetos). 

A API que iremos utilizar será a [Free Currency Conversion API](https://freecurrencyapi.com). Essa API é privada (ou seja, será necessário cadastro de uma conta), mas possui 5k requisições gratuitas por mês, envolvendo mais de 32 moedas e tendo atualização diária.

Devemos, diariamente, verificar o valor do REAL BRASILEIRO perante as outras 31 moedas mundiais. Vamos visar que nos futuros projetos desejamos ter uma área analítica para desenvolvimento de paínes para análises relacionados aos aspectos financeiros do Brasil. Por isso, precisamos inicialmente coletar esses dados e armazenar na camada RAW dentro de um Cloud Storage na nuvem da Google Cloud.

Será utilizado Cloud Functions como local de execução do código, que será desenvolvido em Python, seguindo os princípios da programação orientada a objetos (POO) e as melhores práticas de programação.

O gatilho de execução será configurado por meio do Cloud Scheduler. Toda a infraestrutura será provisionada utilizando o Terraform, que permite a criação da infraestrutura como código. 

## Tecnologias Utilizadas
- Python: Linguagem de programação utilizada para o desenvolvimento da pipeline.
- Cloud Functions: O ambiente na nuvem que executará o código Python, fornecendo escalabilidade e flexibilidade.
- Cloud Storage: Um ambiente na nuvem que permitirá armazenar os arquivos JSON, incluindo as respostas da API de forma segura e escalável.
- Cloud Scheduler: Uma ferramenta na nuvem que permite agendar a execução das Cloud Functions, possibilitando automação e programação de tarefas.
- Secret Manager: A ferramenta que irá auxiliar no armazenamento de dados sensíveis, como tokens.
- Terraform: Uma ferramenta que possibilita a provisionamento eficiente de toda a infraestrutura necessária, seguindo a metodologia de infraestrutura como código (IaC).

## Arquitetura
![Arquitetura do projeto que será construído](imagens/arquitetura_ingestao_por_api_cloud.png)