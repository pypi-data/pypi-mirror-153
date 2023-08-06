from __future__ import annotations

from sqlalchemy import text, inspect

from .versions import *
from .versions.version_0 import Version0


def has_version_table(engine, table_prefix=None):
    return inspect(engine).has_table(Version0.migration_table_name(table_prefix))


def get_database_version(engine, table_prefix=None):
    with engine.connect() as connection:
        with connection.begin():
            result = connection.execute(
                text(f"SELECT version from {Version0.migration_table_name(table_prefix)}")).mappings().first()
            return int(result['version'])


def run_migrations(migrations, engine, table_prefix, schema):
    for migration in migrations:
        migration.do(engine, table_prefix)


def update_database_version(engine, version: int, table_prefix=None):
    with engine.connect() as connection:
        with connection.begin():
            connection.execute(text(f"DELETE from {Version0.migration_table_name(table_prefix)}"))
            connection.execute(text(f"INSERT INTO {Version0.migration_table_name(table_prefix)} VALUES(:version)"), {'version': version})


def apply_migrations(engine, schema=None, migrations: List[MigrationVersion] = None, table_prefix=None):
    if not migrations:
        migrations = [Migration() for Migration in get_versions()]

    if not migrations:
        return

    migrations = sorted(migrations)

    if not has_version_table(engine):
        run_migrations(migrations, engine, table_prefix, schema)
        update_database_version(engine, migrations[-1].get_version(), table_prefix)
        return

    version = get_database_version(engine)
    to_run = migrations[version + 1:]
    if to_run:
        run_migrations(to_run, engine, table_prefix, schema)
        update_database_version(engine, to_run[-1].get_version(), table_prefix)
