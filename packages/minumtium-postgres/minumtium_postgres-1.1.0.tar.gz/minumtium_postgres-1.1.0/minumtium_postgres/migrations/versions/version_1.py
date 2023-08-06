from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, Unicode

from .. import MigrationVersion

USERS_TABLE_NAME = 'users'
POSTS_TABLE_NAME = 'posts'


class Version1(MigrationVersion):
    @staticmethod
    def users_table_name(table_prefix: str) -> str:
        if table_prefix:
            return f'{table_prefix}_{USERS_TABLE_NAME}'
        return USERS_TABLE_NAME

    @staticmethod
    def posts_table_name(table_prefix: str) -> str:
        if table_prefix:
            return f'{table_prefix}_{POSTS_TABLE_NAME}'
        return POSTS_TABLE_NAME

    def get_version(self) -> int:
        return 1

    def do(self, engine, table_prefix=None, schema=None) -> None:
        meta = MetaData(schema=schema)

        Table(
            self.users_table_name(table_prefix), meta,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('username', String(128), nullable=False),
            Column('encrypted_password', String(512), nullable=False)
        )

        Table(
            self.posts_table_name(table_prefix), meta,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('title', String(256), nullable=False),
            Column('author', String(128), nullable=False),
            Column('body', Unicode()),
            Column('timestamp', DateTime())
        )

        meta.create_all(engine)

    def undo(self, engine, table_prefix=None, schema=None) -> None:
        meta = MetaData(schema=schema)
        meta.drop_all(bind=engine,
                      tables=[self.users_table_name(table_prefix), self.posts_table_name(table_prefix)])
