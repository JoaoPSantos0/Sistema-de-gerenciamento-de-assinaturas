from sqlmodel import Field, SQLModel, create_engine

from model import models

sqlite_file_name = 'database.db'
sqlite_url = f'sqlite:///{sqlite_file_name}' #path para raiz do database

# Criar uma engine (engine = conexao entre o banco de dados e o python)
engine = create_engine(sqlite_url, echo=False) # echo serve para mostrar informaçoes do bd no terminal

# essa linha so vai ser executada se o arquivo em si for executado no terminal
if __name__ == '__main__':
    SQLModel.metadata.create_all(engine)