import __init__
from model.database import engine
from model.models import Subscription, Payments
from sqlmodel import Session,select
from datetime import date, datetime


class SubscriptionService:
    def __init__(self, engine):
        self.engine = engine

# Session inicia uma conexao e a encerra apos o uso
    def create(self, subscription:Subscription):
        with Session(self.engine) as session:
            session.add(subscription) # adiciona a subs em uma camada intermediaria
            session.commit() # agr os dados sao salvos no bd
            return subscription
        
    def list_all(self):
        with Session(self.engine) as session:
            query = select(Subscription) # comando SQL salvo em query
            result = session.exec(query).all() # executa comando SQL e salva a tabela em result
            return result
    
    def delete(self, id):
        with Session(self.engine) as session:
            query = select(Subscription).where(Subscription.id == id)
            result_query = session.exec(query).one() # all retorna lista, one retorna um unico valor
            session.delete(result_query)
            session.commit()
    
    def delete_payment(self, id):
        with Session(self.engine) as session:
            query = select(Payments).where(Payments.subs_id == id)
            result_query = session.exec(query).one() # all retorna lista, one retorna um unico valor
            session.delete(result_query)
            session.commit()

    def pay(self, subscription: Subscription):
        with Session(self.engine) as session:
            query = select(Payments).join(Subscription).where(Subscription.empresa==subscription.empresa)
            result_query = session.exec(query).all()
            
            pago = False
            for results in result_query:
                if results.date.month == date.today().month:
                    pago = True
            if pago:
                print('Essa conta ja foi paga esse mês!')
            
            if pago == False:
                pay = Payments(subs_id=subscription.id, date=date.today())
                session.add(pay)
                session.commit()
    
    def total_values(self):
        with Session(self.engine) as session:
            query = select(Subscription)
            result_query = session.exec(query).all()

        valor_tot = 0
        for index in result_query:
             valor_tot = valor_tot+index.valor
            
        return float(valor_tot)

    def _get_last_one_year_(self):
        today = datetime.today()
        year = today.year
        month = today.month
        last_12_months = []
        
        for i in range(12):
            
            last_12_months.append((month,year))
            if month-1 == 0:
                year = year - 1
                month = 12
    
            
            month -= 1
            
        return last_12_months[::-1] # serve para inverter a ordem da lista
    
    def _get_values_in_the_last_12_months_(self, last_12_months):
        with Session(self.engine) as session:
            query = select(Payments)
            results = session.exec(query).all()

            values_for_months = []

            for i in last_12_months:
                value = 0
                for result in results:
                    if result.date.month == i[0] and result.date.year == i[1]:
                        value += float(result.subs.valor) 
                values_for_months.append(value)  
            return values_for_months

    def gen_chart(self):
        last_12_months = self._get_last_one_year_()
        values_for_month = self._get_values_in_the_last_12_months_(last_12_months)
        

        import matplotlib.pyplot as plt

        """ last_12_months2 = []
        for i in last_12_months:
            last_12_months2.append(i[0]) """
        last_12_months = list(map(lambda x: x[0],self._get_last_one_year_()))
        
        plt.plot(last_12_months,values_for_month)
        plt.show()


#ss = SubscriptionService(engine)
#print(ss.gen_chart())
""" assinaturas = ss.list_all()
#print(assinaturas)

# enumerate = i=index , s=self valor
for i, s in enumerate(assinaturas):
    print(f'[{i}]->{s.empresa}')

x = int(input(f'Qual conta voce quer pagar:'))
ss.pay(assinaturas[x]) """
