# Minumtium Postgres

A postgres database adapter for the [minumtium](https://github.com/danodic-dev/minumtium) library. It uses SQL Alchemy
as its abstraction library alongside with pg8000 as the connection driver.

### What can I use it for?

It is used to provide access to data stored in postgres instances using
the [minumtium](https://github.com/danodic-dev/minumtium) library.

## Usage

Install it using your favorite package manager:

```commandline
pip install minumtium-postgres
```

```commandline
pipenv install minumtium-postgres
```

```commandline
poetry install minumtium-postgres
```

Then, provide it to your minumtium Services:

```python
from minumtium.modules.idm import IdmService, UserRepository
from minumtium_simple_jwt_auth import SimpleJwtAuthentication

from minumtium_postgres import MinumtiumPostgresAdapter, MinumtiumPostgresAdapterConfig

config = MinumtiumPostgresAdapterConfig(
    username='minumtium',
    password='samplepassword',
    host='localhost',
    port=5432,
    dbname='minumtium',
    schema_name='minumtium')

db_adapter = SqlAlchemyAdapter({config, 'posts')
auth_adapter = SimpleJwtAuthentication(configuration={
    'jwt_key': 'not a reliable key, change that quickly',
    'session_duration_hours': 1})

users_repository = UserRepository(db_adapter)
idm_service = IdmService(auth_adapter, users_repository)

idm_service.authenticate('jao', 'batata')
```