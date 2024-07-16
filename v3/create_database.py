from core.configs import DBBaseModel, settings
from core.database import engine
from sqlalchemy_utils import create_database, database_exists


def create_tables() -> None:
    if not database_exists(settings.DB_URL):
        print('Criando banco de dados...')
        create_database(settings.DB_URL)

        import models.__allmodels__
        print('Criando as tabelas no banco de dados...')

        with engine.begin() as conn:
            DBBaseModel.metadata.drop_all(conn)
            DBBaseModel.metadata.create_all(conn)
        print('Tabelas criadas com sucesso.')


if __name__ == '__main__':
    create_tables()
