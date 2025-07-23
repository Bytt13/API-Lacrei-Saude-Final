FROM python:3.12-slim

# Definir variáveis de ambiente para evitar problemas comuns
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Definir o diretório de trabalho dentro do contentor
WORKDIR /code

# Instalar o Poetry (gerenciador de dependências)
RUN pip install poetry

# Copiar os ficheiros de dependência primeiro para aproveitar o cache do Docker
COPY poetry.lock pyproject.toml /code/

# Instalar as dependências do projeto, incluindo gunicorn
RUN poetry config virtualenvs.create false && poetry install --without dev --no-interaction --no-ansi --no-root
# Copiar o resto do código do projeto para o diretório de trabalho
COPY . /code/

# Informar ao Docker que a nossa aplicação usa a porta 8000
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]