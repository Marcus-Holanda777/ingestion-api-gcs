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

## [Ingestão dos dados](ingestion_api_gcs/ingestion.py) 🔗

A ingestão dos dados é feita por meio da classe `Ingestion` que é uma especialização da classe `ApiCurrencyRequests` que fornece métodos específicos para acessar endpoints da API [Free Currency](https://freecurrencyapi.com). Em essência, essa classe facilita a ingestão de dados relacionados a moedas, taxas de câmbio e históricos de variação cambial.

> [!IMPORTANT]
> Na classe `ApiCurrencyRequests` existe a função `headers` ela é essencial para definir os cabeçalhos HTTP. 
> Que autenticam e configuram corretamente as requisições à API. 
> Estes cabeçalhos contêm informações críticas que afetam o comportamento da API em relação ao cliente.

### Principais Responsabilidades e Métodos

### 1. Inicialização (`__init__`)
- A classe é inicializada com um `token` de autenticação para a API e um `endpoint` que define a URL base (por padrão, `'https://api.freecurrencyapi.com/v1'`).
- Ela chama o construtor da classe pai (`ApiCurrencyRequests`) para configurar esses parâmetros e preparar os cabeçalhos da requisição.

### 2. Métodos para Acessar Dados

- **`status`**: 
  - Retorna o status da API, útil para verificar se a API está operacional.
  - Faz uma requisição ao endpoint `/status`.

- **`lista_moedas`**: 
  - Lista as moedas disponíveis na API.
  - Opcionalmente, você pode filtrar por moedas específicas, passando uma lista de códigos de moedas (por exemplo, `['USD', 'EUR']`).
  - Utiliza o endpoint `/currencies`.

- **`taxa_cambio`**: 
  - Obtém as taxas de câmbio mais recentes com base em uma moeda específica (`base_currency`).
  - Também permite listar moedas específicas para comparar taxas.
  - Faz uma requisição ao endpoint `/latest`.

- **`historico`**: 
  - Retorna o histórico de taxas de câmbio para uma data específica (`date`).
  - Você pode especificar uma moeda base e uma lista de moedas para filtrar os dados.
  - Esse método faz uma requisição ao endpoint `/historical`.

### 3. Método Auxiliar

- **`list_join`**: 
  - Converte uma lista de moedas (por exemplo, `['USD', 'EUR']`) em uma string separada por vírgulas (`'USD,EUR'`).
  - Isso é útil para construir os parâmetros de consulta necessários para as requisições da API.

### Exemplo de Uso

Com a classe `Ingestion`, você pode facilmente obter informações de câmbio e manipular esses dados de forma programática. Por exemplo:

```python
# Criando uma instância da classe
api_ingestion = Ingestion(token='seu_token_api')

# Obtendo o status da API
status = api_ingestion.status

# Listando moedas
moedas = api_ingestion.lista_moedas(['USD', 'EUR', 'BRL'])

# Obtendo taxas de câmbio mais recentes para USD
taxas = api_ingestion.taxa_cambio(base_currency='USD', currencies=['EUR', 'BRL'])

# Consultando o histórico de câmbio para uma data específica
historico = api_ingestion.historico(date=datetime(2023, 1, 1), base_currency='USD', currencies=['EUR'])
```

## Acessando segredos e exportando os dados para o Storage do Google Cloud

Para acessar a API precisamos de um token. Esse token é fornecido logo após o cadastro feito na plataforma [Free Currency](https://freecurrencyapi.com). 
