from modelos.pessoas import Cliente
from utils.utils import limpar_tela, pausar_tela

banco_clientes = []

def cadastrar_cliente():
    limpar_tela()
    print("\n--- CADASTRO DE CLIENTE (DEVEDOR) ---")
    
    nome = input("Nome Completo: ")
    cpf = input("CPF: ")
    celular = input("Celular (WhatsApp): ")
    endereco = input("Endereço Completo: ") # 
    
    print("\nDefina o Nível de Confiança[cite: 36]:")
    print("1 - Novo (Padrão)")
    print("2 - Bom Pagador")
    print("3 - Atraso Frequente")
    print("4 - Bloqueado")
    op_nivel = input("Escolha: ")
    
    nivel = "Novo"
    if op_nivel == "2": nivel = "Bom Pagador"
    elif op_nivel == "3": nivel = "Atraso Frequente"
    elif op_nivel == "4": nivel = "Bloqueado"
    
    try:
        limite_input = input("Limite de Crédito (Enter para R$200.00): ")
        if limite_input == "":
            limite = 200.00
        else:
            limite = float(limite_input)
    except ValueError:
        print("Valor inválido. Usando padrão de R$ 200.00")
        limite = 200.00
    
    novo_id = len(banco_clientes) + 1
    novo_cliente = Cliente(novo_id, nome, cpf, celular, endereco, nivel, limite)
    
    banco_clientes.append(novo_cliente)
    print(f"Cliente {nome} cadastrado! Limite: R${limite:.2f}")
    pausar_tela()

def listar_clientes():
    limpar_tela()
    print("\n--- LISTA DE CLIENTES ---")
    if not banco_clientes:
        print("Nenhum cliente cadastrado.")
    else:
        for c in banco_clientes:
            print(f"ID: {c.id_cliente:03d} | {c.nome} | {c.nivel_confianca} | Limite: R${c.limite_credito}")
            print(f"   Endereço: {c.endereco}")
            print("-" * 30)
    
    pausar_tela()