from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorios
from controller.controller_hospede import Controller_Hospede
from controller.controller_quarto import Controller_Quarto
from controller.controller_reserva import Controller_Reserva


tela_inicial = SplashScreen()
relatorio = Relatorios()
ctrl_hospede = Controller_Hospede()
ctrl_quarto = Controller_Quarto()
ctrl_reserva = Controller_Reserva()

def reports(opcao_relatorio: int = 0):
    if opcao_relatorio == 1:
        relatorio.relatorio_reservas_por_status()
    elif opcao_relatorio == 2:
        relatorio.relatorio_reservas_detalhado()
    elif opcao_relatorio == 3:
        relatorio.relatorio_reservas_por_mes()
    elif opcao_relatorio == 4:
        relatorio.relatorio_hospedes()

def inserir(opcao_inserir: int = 0):
    
    current = opcao_inserir
    while True:
        if current == 1:
            ctrl_hospede.inserir_hospede()
        elif current == 2:
            ctrl_quarto.inserir_quarto()
        elif current == 3:
            ctrl_reserva.inserir_reserva()
        else:
            print("Opção de entidade inválida.")

        resp = input("\nDeseja inserir mais algum registro? (S/N): ").strip().upper()
        if resp != 'S':
            break

        
        resp2 = input("Continuar na mesma entidade? (S para sim / N para escolher outra): ").strip().upper()
        if resp2 == 'S':
            continue
        else:
            print(config.MENU_ENTIDADES)
            try:
                current = int(input("Escolha uma opção [1-3]: "))
            except ValueError:
                print("Opção inválida. Voltando ao menu principal.")
                break

def atualizar(opcao_atualizar: int = 0):
    
    current = opcao_atualizar
    while True:
        if current == 1:
            ctrl_hospede.atualizar_hospede_interactive()
        elif current == 2:
            ctrl_quarto.atualizar_quarto_interactive()
        elif current == 3:
            ctrl_reserva.atualizar_reserva_interactive()
        else:
            print("Opção de entidade inválida.")

        resp = input("\nDeseja atualizar mais algum registro? (S/N): ").strip().upper()
        if resp != 'S':
            break

        resp2 = input("Continuar na mesma entidade? (S para sim / N para escolher outra): ").strip().upper()
        if resp2 == 'S':
            continue
        else:
            print(config.MENU_ENTIDADES)
            try:
                current = int(input("Escolha uma opção [1-3]: "))
            except ValueError:
                print("Opção inválida. Voltando ao menu principal.")
                break

def excluir(opcao_excluir: int = 0):
    
    current = opcao_excluir
    while True:
        if current == 1:
            ctrl_hospede.excluir_hospede_interactive()
        elif current == 2:
            ctrl_quarto.excluir_quarto_interactive()
        elif current == 3:
            ctrl_reserva.excluir_reserva_interactive()
        else:
            print("Opção de entidade inválida.")

        resp = input("\nDeseja excluir mais algum registro? (S/N): ").strip().upper()
        if resp != 'S':
            break

        resp2 = input("Continuar na mesma entidade? (S para sim / N para escolher outra): ").strip().upper()
        if resp2 == 'S':
            continue
        else:
            print(config.MENU_ENTIDADES)
            try:
                current = int(input("Escolha uma opção [1-3]: "))
            except ValueError:
                print("Opção inválida. Voltando ao menu principal.")
                break

def run():
    
    print(tela_inicial.get_updated_screen())
    input("\nPressione Enter para continuar...")
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        try:
            opcao = int(input("Escolha uma opção [1-5]: "))
        except ValueError:
            print("Opção inválida. Digite apenas números.")
            continue
        
        config.clear_console(1)

        if opcao == 1:  
            print(config.MENU_RELATORIOS)
            opcao_relatorio = int(input("Escolha uma opção [0-4]: "))
            config.clear_console(1)
            reports(opcao_relatorio)
            
            config.clear_console()

        elif opcao == 2:  
            print(config.MENU_ENTIDADES)
            opcao_inserir = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)
            inserir(opcao_inserir)
            input("\nPressione Enter para voltar ao menu principal...")
            config.clear_console()

        elif opcao == 3:  
            print(config.MENU_ENTIDADES)
            opcao_atualizar = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)
            atualizar(opcao_atualizar)
            input("\nPressione Enter para voltar ao menu principal...")
            config.clear_console()

        elif opcao == 4:  
            print(config.MENU_ENTIDADES)
            opcao_excluir = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)
            excluir(opcao_excluir)
            input("\nPressione Enter para voltar ao menu principal...")
            config.clear_console()

        elif opcao == 5:
            print("Obrigado por utilizar o nosso sistema.")
            break

        else:
            print("Opção incorreta. Tente novamente.")
            input("\nPressione Enter para voltar ao menu principal...")
            config.clear_console()

if __name__ == "__main__":
    run()
