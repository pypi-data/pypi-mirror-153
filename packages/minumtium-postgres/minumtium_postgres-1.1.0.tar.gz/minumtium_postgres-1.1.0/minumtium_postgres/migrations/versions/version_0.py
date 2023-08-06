from sqlalchemy import MetaData, Table, Column, Integer
from sqlalchemy.orm import sessionmaker

from .. import MigrationVersion

MIGRATION_TABLE_NAME = 'minumtium_sqlalchemy_version'


class Version0(MigrationVersion):
    @staticmethod
    def migration_table_name(table_prefix: str = None) -> str:
        if table_prefix:
            return f'{table_prefix}_{MIGRATION_TABLE_NAME}'
        return MIGRATION_TABLE_NAME

    def get_version(self) -> int:
        return 0

    def do(self, engine, table_prefix=None, schema=None) -> None:
        meta = MetaData(schema=schema)
        table = Table(
            self.migration_table_name(table_prefix), meta,
            Column('version', Integer)
        )
        meta.create_all(engine)

        session = sessionmaker(bind=engine)()
        session.execute(table.insert().values({'version': 0}))
        session.commit()

    def undo(self, engine, table_prefix=None, schema=None) -> None:
        meta = MetaData()
        meta.drop_all(bind=engine, tables=[self.migration_table_name(table_prefix)])
