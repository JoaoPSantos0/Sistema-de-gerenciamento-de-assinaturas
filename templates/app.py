import __init__
from views.view import SubscriptionService
from model.database import engine
from datetime import datetime
from decimal import Decimal
from model.models import Subscription, Payments

class UI:
    def __init__(self):
        self.subs_service = SubscriptionService(engine)

    def start(self):
    
        while True: 
            print('''
            [1] -> Adicionar assinatura
            [2] -> Remover assinatura
            [3] -> Valor total   
            [4] -> Gastos ultimos 12 meses
            [5] -> Sair           
            ''')
            choice = int(input('Escolha uma opção: '))

            if choice == 1:
                self.add_subscription()
            elif choice == 2:
                self.remove_subscription()
            elif choice == 3:
                self.total_values()
            elif choice == 4:
                self.subs_service.gen_chart()
            else:
                break

    def add_subscription(self):
        empresa = input('Digite o nome da empresa: ')
        site = input('Digite o site: ')

        # Loop para garantir que o usuário insira uma data válida
        while True:
            data_input = input('Data da assinatura (DD/MM/AAAA): ')
            try:
                data_assinatura = datetime.strptime(data_input, '%d/%m/%Y')   
                break  # Sai do loop se a data for válida
            except ValueError:
                print("Formato de data inválido! Tente novamente.")

        valor = Decimal(input('Valor: '))     
        subs = Subscription(empresa=empresa, site=site, date_assinatura=data_assinatura, valor=valor)
        self.subs_service.create(subs)
        print("Assinatura adicionada com sucesso!")

    def remove_subscription(self):
        escolha = self.subs_service.list_all()
        print('Escolha qual assinatura deseja excluir')

        for i in escolha:
            print(f'[{i.id}] -> {i.empresa}')
        
        choice = int(input('Escolha a assinatra: '))
        self.subs_service.delete(choice)
        self.subs_service.delete_payment(choice)

    def total_values(self):
        print(f'Seu valor total em assinaturas é: {self.subs_service.total_values()}')

    

UI().start()