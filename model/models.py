from sqlmodel import Field, SQLModel, create_engine, Relationship
from typing import Optional
from datetime import date
from decimal import Decimal


# Estruturando a tabela do banco como sendo uma Subscription
class Subscription(SQLModel, table=True):
    id: int = Field(primary_key=True)
    empresa: str
    site: Optional[str]=None
    date_assinatura: date
    valor: Decimal

class Payments(SQLModel, table=True):
    id: int = Field(primary_key=True)
    subs: Subscription = Relationship() 
    subs_id: int = Field(foreign_key = 'subscription.id') # foreign_key = 'nome da tabela minusculo', nao o da variavel
    date: date
