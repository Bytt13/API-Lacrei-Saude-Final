# API Lacrei Saúde

## 1. Visão Geral

A API Lacrei Saúde é uma plataforma para gerenciamento de profissionais de saúde e suas respectivas consultas. Ela foi desenvolvida para ser robusta, escalável e de fácil manutenção, utilizando tecnologias modernas de desenvolvimento web.

## 2. Tecnologias Utilizadas

- **Backend:** Python, Django, Django REST Framework
- **Gerenciador de Pacotes:** Poetry
- **Banco de Dados:** PostgreSQL (produção), SQLite (desenvolvimento)
- **Containerização:** Docker, Docker Compose
- **Servidor WSGI:** Gunicorn
- **CI/CD:** GitHub Actions
- **Hospedagem:** AWS Elastic Beanstalk
- **Documentação da API:** `drf-spectacular` (Swagger/OpenAPI)

## 3. Setup

### 3.1. Setup Local (Recomendado)

**Pré-requisitos:**
* Python 3.12+
* Poetry

**Passos:**

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/Bytt13/API-lacrei-saude
    cd API-lacrei-saude
    ```

2.  **Instale as dependências com Poetry:**
    ```bash
    poetry install
    ```

3.  **Configure as variáveis de ambiente:**
    Crie um arquivo `.env` na raiz do projeto e adicione a seguinte variável:
    ```
    SECRET_KEY='sua-chave-secreta-super-segura'
    ```
    *O banco de dados padrão é o `SQLite` para facilitar a configuração local.*

4.  **Execute as migrações e inicie o servidor:**
    ```bash
    poetry run python manage.py migrate
    poetry run python manage.py runserver
    ```

5.  **Acesse a API:**
    * **API:** `http://127.0.0.1:8000/api/`
    * **Documentação (Swagger):** `http://127.0.0.1:8000/api/docs/`

### 3.2. Setup com Docker

**Pré-requisitos:**
* Docker
* Docker Compose

**Passos:**

1.  Na raiz do projeto, execute:
    ```bash
    docker-compose up --build
    ```
    A aplicação estará disponível em `http://localhost:8000`.

## 4. Execução dos Testes

O projeto utiliza `pytest` e os testes cobrem os principais fluxos dos endpoints. Para executar a suíte de testes:

```bash
poetry run python manage.py test
```
Este comando é o mesmo utilizado no pipeline de CI para garantir a qualidade do código.

## 5. Fluxo de Deploy (CI/CD)

O pipeline de Integração e Entrega Contínua (CI/CD) é gerenciado pelo **GitHub Actions** (`.github/workflows/ci.yml`) e é acionado a cada `push` na branch `main`.

1.  **Job `build-and-test` (CI):**
    * Verifica o código com `flake8` (linting).
    * Executa a suíte de testes completa para garantir que novas alterações não quebrem a funcionalidade existente.

2.  **Job `deploy` (CD):**
    * É executado apenas se o job anterior for bem-sucedido.
    * Empacota a aplicação em um `deploy.zip`.
    * Realiza o deploy da nova versão no ambiente da **AWS Elastic Beanstalk** de forma automatizada.

## 6. Justificativas Técnicas

* **Django/DRF:** Escolhidos pela robustez, segurança "out-of-the-box" e ecossistema maduro, acelerando o desenvolvimento de APIs RESTful.
* **Poetry:** Para um gerenciamento de dependências determinístico, garantindo que os ambientes de desenvolvimento e produção sejam idênticos.
* **Docker:** Para criar ambientes padronizados e isolados, eliminando o "funciona na minha máquina" e simplificando o deploy.
* **AWS Elastic Beanstalk:** Abstrai a complexidade da infraestrutura na nuvem (EC2, Load Balancer, etc.), permitindo focar no código enquanto a AWS gerencia a escalabilidade e o deploy.
* **GitHub Actions:** Para automatizar todo o processo de teste e deploy, garantindo entregas rápidas e seguras.
* **`drf-spectacular`:** Para gerar documentação OpenAPI (Swagger) automaticamente a partir do código, mantendo a documentação sempre atualizada com a API.

## 7. Justificativa do Modelo de Código e Arquitetura

A estrutura do código foi pensada para seguir as melhores práticas de desenvolvimento com Django, priorizando a clareza, a organização e a facilidade de manutenção. A ideia é que qualquer pessoa desenvolvedora que entre no projeto consiga entender rapidamente como as coisas funcionam.

### 7.1. Padrão Model-View-Serializer (MVS)

O projeto segue o padrão **Model-View-Serializer**, que é a espinha dorsal do Django REST Framework.

* **Model (`models.py`):** É a "planta" dos nossos dados. Ele define, em um só lugar, como um `Profissional` ou uma `Consulta` devem ser, quais campos eles têm e como se relacionam. Isso garante que os dados sejam consistentes e íntegros no banco de dados.

* **Serializer (`serializers.py`):** Funciona como um "tradutor". Ele pega os dados complexos dos nossos `Models` (em Python) e os converte para um formato simples que a internet entende, como o JSON. Ele também faz o caminho inverso: pega um JSON enviado na requisição e o traduz de volta para um objeto que o Django pode salvar no banco de dados. Além disso, é a primeira camada de validação dos dados que chegam na API.

* **View (`views.py`):** É o "cérebro" da operação. A `View` recebe as requisições (GET, POST, PUT, DELETE), usa o `Serializer` para "traduzir" e validar os dados, e conversa com o `Model` para buscar ou salvar informações no banco de dados.

**Analogia:** Pense em um restaurante. O **Model** é a despensa com os ingredientes organizados. O **Serializer** é o chef que sabe quais ingredientes pegar e como prepará-los (o prato final). A **View** é o garçom, que anota o seu pedido (requisição HTTP), leva para o chef e depois te entrega o prato pronto (resposta JSON).

### 7.2. Uso de `ViewSets` e `Routers`

Em vez de criar uma função (ou classe) para cada operação (listar, criar, ver um, atualizar, deletar), utilizamos **`ModelViewSet`**.

* **Por quê?** Para seguir o princípio **DRY (Don't Repeat Yourself - Não se Repita)**. O `ModelViewSet` agrupa toda a lógica CRUD (Create, Retrieve, Update, Delete) para um `Model` em um único lugar. Com poucas linhas de código, temos todos os endpoints necessários para gerenciar um `Profissional` ou uma `Consulta`.

Junto com o `ModelViewSet`, o **`DefaultRouter`** (`urls.py`) trabalha para gerar as URLs da API automaticamente. Não precisamos definir manualmente `GET /profissionais/`, `POST /profissionais/`, `GET /profissionais/{id}/`, etc. O `Router` faz isso por nós, garantindo um padrão de URL consistente em toda a API.

**Benefício:** Isso acelera imensamente o desenvolvimento, reduz a chance de erros e torna a API previsível e fácil de usar.

### 7.3. Separação de Responsabilidades

O projeto é organizado de forma a separar claramente as responsabilidades:

* **App `api`:** Contém toda a lógica de negócio da aplicação (Models, Views, Serializers). Se no futuro precisarmos de um outro app, como um `blog`, ele seria criado separadamente, sem interferir na `api`.
* **Projeto `lacrei_saude`:** Contém as configurações globais do projeto (`settings.py`) e as definições de URL principais. Ele "orquestra" os diferentes apps.
* **Configuração de Ambiente (`.env`):** Segredos e configurações que mudam entre ambientes (desenvolvimento, produção) são mantidos em um arquivo `.env` e nunca são enviados para o repositório (`.gitignore`). Isso segue a prática número 3 do **The Twelve-Factor App**, tornando a aplicação mais segura e portável.

Essa estrutura modular torna o projeto mais fácil de navegar, testar e escalar. Se a API crescer, podemos facilmente adicionar novos apps ou quebrar o app `api` em apps menores e mais especializados.

## 8. Estratégia de Rollback Funcional

Manter a estabilidade da aplicação é crucial. Se uma nova versão introduz um bug crítico, precisamos de um plano para reverter para a versão anterior de forma rápida e segura. Abaixo estão detalhadas duas estratégias de rollback, da mais simples à mais robusta.

### Estratégia Escolhida: Blue/Green Deployment (O Padrão Ouro "Zero Downtime")

Esta é a abordagem mais profissional e segura, ideal para aplicações críticas onde o tempo de inatividade é inaceitável. Ela envolve manter dois ambientes de produção idênticos.

* **Ambiente Blue:** A versão estável atual que está recebendo 100% do tráfego dos usuários.
* **Ambiente Green:** Um ambiente idêntico, porém inativo, que serve como "palco" para a nova versão.

**Fluxo de Deploy:**

1.  **Deploy no Ambiente Green:** O pipeline de CI/CD, em vez de atualizar o ambiente Blue, implanta a nova versão do código no ambiente Green.
2.  **Testes em Produção (Seguros):** Com o ambiente Green no ar, mas sem receber tráfego de usuários, podemos rodar testes de fumaça (smoke tests) e testes de integração contra uma infraestrutura real (incluindo uma cópia recente do banco de dados de produção). Isso garante que a nova versão funciona no "mundo real".
3.  **Troca do Roteador (Swap de URL):** Se todos os testes passarem, a mágica acontece. O balanceador de carga (ou o próprio Elastic Beanstalk) é reconfigurado para redirecionar todo o tráfego do ambiente Blue para o Green. Isso é uma troca de ponteiro, uma operação quase instantânea.
4.  **Green se torna o novo Blue:** O ambiente Green agora é a nossa produção oficial. O ambiente Blue antigo fica em espera.

**Fluxo de Rollback (Instantâneo):**

Se, após a troca, a nova versão apresentar um bug que não foi pego nos testes, o rollback é trivial:
* **Basta reconfigurar o roteador para apontar o tráfego de volta para o ambiente Blue**, que ainda está rodando a versão estável anterior. A reversão leva segundos e é completamente transparente para o usuário.

**Vantagens:**
* **Zero Downtime:** A troca entre ambientes é instantânea.
* **Rollback Imediato:** Reverter uma versão problemática é uma operação de segundos e baixo risco.
* **Testes Confiáveis:** Permite validar a nova versão em um ambiente de produção real antes de liberá-la.

**Desvantagens:**
* **Custo:** Manter dois ambientes de produção idênticos pode duplicar os custos de infraestrutura.
* **Complexidade:** Requer uma configuração mais avançada do balanceador de carga e do pipeline de deploy.

O AWS Elastic Beanstalk suporta nativamente o deploy Blue/Green.

## 9. Proposta de Integração com a Assas

Para integrar um sistema de pagamentos como o Assas, a arquitetura seria:

* **App `pagamentos` no Django:** Um novo app dedicado para isolar a lógica de pagamentos.
* **Model `Pagamento`:** Associado a uma `Consulta`, armazenaria o `id` da cobrança no Assas, status, valor, etc.
* **`AssasService`:** Uma classe de serviço para encapsular a comunicação com a API do Assas (criar cobrança, consultar status). Isso centraliza a lógica e facilita a troca de provedor no futuro.
* **Endpoint de Pagamento:** Um endpoint como `/api/consultas/{id}/pagar/` que, ao ser chamado:
    * Usa o `AssasService` para gerar a cobrança.
    * Retorna a URL de pagamento para o cliente (frontend).
* **Webhook:** Um endpoint para receber notificações do Assas (ex: pagamento confirmado). Este endpoint atualizaria o status do pagamento no nosso banco de dados.

## 10. Documentação da API e Deploy(Swagger)

A documentação da API é gerada automaticamente e está disponível de forma interativa. Acesse o seguinte endpoint, utilizando o link gerado pelo Deploy na AWS:

* **[http://lacrei-saude-api-env-2.eba-wkvpwp2y.sa-east-1.elasticbeanstalk.com/api/docs/](http://lacrei-saude-api-env-2.eba-wkvpwp2y.sa-east-1.elasticbeanstalk.com/api/docs)** *

**Para Acessar os outros endpoints, utilize eles, após o link do deploy**
http://lacrei-saude-api-env-2.eba-wkvpwp2y.sa-east-1.elasticbeanstalk.com


Nesta página, você pode visualizar todos os endpoints, modelos de dados e testar as requisições diretamente do seu navegador.
para ser autorizado, utilize o token: ef6319df50808891dee08f7caf539f43ca8aa62e

# 11. Pipeline CI/CD

O pipeline com o github actions foi feito para que toda vez que dessemos um "git push" para main, ele rodasse os testes e build de forma automática, além de fazer o Deploy.
É possível ver o arquivo .yml na pasta [.github/workflows](https://github.com/Bytt13/API-Lacrei-Saude-Final/blob/main/.github/workflows/main.yml) do projeto


## 12. Testes Feitos

* **API TEST CASE:**
* 
<img width="770" height="191" alt="Image" src="https://github.com/user-attachments/assets/521a5810-0f3c-418d-a118-e1820b42684a" />

* **CRIANDO SUPERUSER**
* 
<img width="870" height="146" alt="Image" src="https://github.com/user-attachments/assets/c47206e8-6c21-4f28-895d-e2624c74c5f4" />

* **GANHANDO TOKEN:**
* 
<img width="964" height="533" alt="Image" src="https://github.com/user-attachments/assets/9c4583a3-f90b-4bc5-8050-8530c11cad43" />

* **CRIANDO PROFISSIONAL:**
* 
<img width="641" height="581" alt="Image" src="https://github.com/user-attachments/assets/f435c2f9-4ffd-4e47-be2d-2aa61712068b" />

* **LISTANDO PROFISSIONAIS:**
* 
<img width="898" height="801" alt="Image" src="https://github.com/user-attachments/assets/9114bc41-72ce-4a2d-9816-a6a43d96e7e5" />

* **EDITANDO PROFISSIONAL:**
* 
<img width="814" height="707" alt="Image" src="https://github.com/user-attachments/assets/c7697aee-ccd6-4654-a519-ba8346497b76" />

* **DELETANDO PROFISSIONAL:**
* 
<img width="827" height="500" alt="Image" src="https://github.com/user-attachments/assets/1ce63551-efd0-493c-9729-f29c87edf915" />

* **CRIANDO CONSULTA:**
* 
<img width="719" height="636" alt="Image" src="https://github.com/user-attachments/assets/afd35d0a-6edb-48e6-812a-8d6f9ac359a5" />

* **BUSCANDO CONSULTA POR PROFISSIONAL:**

<img width="815" height="651" alt="Image" src="https://github.com/user-attachments/assets/46870488-d9d2-45f0-9b95-bbc8f96f8721" />

<img width="757" height="595" alt="Image" src="https://github.com/user-attachments/assets/ed8aaeb2-db59-409c-a754-403ef1350ab0" />
