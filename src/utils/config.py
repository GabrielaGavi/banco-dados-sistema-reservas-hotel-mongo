MENU_PRINCIPAL = """Menu Principal
1 - Relatórios
2 - Inserir Registros
3 - Atualizar Registros
4 - Remover Registros
5 - Sair
"""

MENU_RELATORIOS = """Relatórios
1 - Reservas por Status
2 - Reservas Detalhadas
3 - Reservas por Mês
4 - Listagem de Hóspedes
0 - Voltar
"""

MENU_ENTIDADES = """Entidades
1 - HÓSPEDES
2 - QUARTOS
3 - RESERVAS
0 - Voltar
"""


QUERY_COUNT = "SELECT COUNT(1) AS total_{tabela} FROM {tabela}"

def clear_console(wait_time: int = 3):
    """
    Limpa a tela após alguns segundos
    wait_time: tempo de espera (em segundos)
    """
    import os
    from time import sleep
    sleep(wait_time)
    
    if (os.name == 'nt'):
        os.system('cls')
    else:
        os.system('clear')
