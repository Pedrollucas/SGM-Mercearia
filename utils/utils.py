import os

def limpar_tela():
    """
    Limpa o terminal tanto no Windows quanto no Linux/Mac.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar_tela():
    """
    Mantém a tela parada até o usuário decidir sair.
    """
    input("\nPressione [ENTER] para sair dessa tela...")