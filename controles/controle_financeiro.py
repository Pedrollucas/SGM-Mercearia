from datetime import date, timedelta
from modelos.financeiro import Divida, Pagamento
from controles.controle_clientes import banco_clientes
from utils.utils import limpar_tela, pausar_tela

banco_dividas = []

def buscar_cliente_por_id(id_busca):
    """Função auxiliar para encontrar um cliente na lista."""
    for cliente in banco_clientes:
        if str(cliente.id_cliente) == str(id_busca):
            return cliente
    return None

def lancar_divida():
    limpar_tela()
    print("\n--- LANÇAMENTO DE NOVA DÍVIDA ---")
    
    if not banco_clientes:
        print("Erro: Não há clientes cadastrados. Cadastre um cliente primeiro.")
        pausar_tela()
        return

    id_cliente = input("Digite o ID do Cliente: ")
    cliente = buscar_cliente_por_id(id_cliente)
    
    if not cliente:
        print("Cliente não encontrado!")
        pausar_tela()
        return

    print(f"Cliente selecionado: {cliente.nome} (Limite: R${cliente.limite_credito:.2f})")

    try:
        valor = float(input("Valor da compra (R$): "))
        descricao = input("Descrição (ex: Cesta Básica, Carnes): ")
        prazo_dias = int(input("Vencimento em quantos dias? (ex: 5, 30): "))
    except ValueError:
        print("Erro: Digite apenas números para Valor e Dias.")
        pausar_tela()
        return

    if valor > cliente.limite_credito:
        print(f"\ALERTA: Esta compra (R${valor}) excede o limite definido (R${cliente.limite_credito})!")
        confirmar = input("Deseja autorizar mesmo assim? (S/N): ").upper()
        if confirmar != "S":
            print("Operação cancelada.")
            pausar_tela()
            return

    data_vencimento = date.today() + timedelta(days=prazo_dias)

    novo_id_divida = len(banco_dividas) + 1
    nova_divida = Divida(novo_id_divida, cliente, valor, data_vencimento, descricao)
    
    banco_dividas.append(nova_divida)
    
    print("\nDívida Registrada com Sucesso!")
    print(f"   ID Dívida: {novo_id_divida}")
    print(f"   Vencimento: {data_vencimento.strftime('%d/%m/%Y')} (Daqui a {prazo_dias} dias)")
    pausar_tela()

def listar_dividas():
    limpar_tela()
    print("\n--- RELATÓRIO DE DÍVIDAS ---")
    if not banco_dividas:
        print("Nenhuma dívida registrada.")
    else:
        for d in banco_dividas:
            print(f"ID: {d.id_divida} | Cliente: {d.cliente.nome}")
            print(f"Valor: R${d.valor_original:.2f} | Saldo: R${d.saldo_devedor:.2f}")
            print(f"Vence em: {d.data_vencimento} | Status: {d.status}")
            print("-" * 30)
    pausar_tela()

def registrar_pagamento():
    limpar_tela()
    print("\n--- REGISTRAR PAGAMENTO (BAIXA) ---")
    
    id_cliente_input = input("Digite o ID do Cliente que vai pagar: ")
    
    dividas_deste_cliente = []
    for d in banco_dividas:
        if str(d.cliente.id_cliente) == id_cliente_input:
            dividas_deste_cliente.append(d)
            
    if not dividas_deste_cliente:
        print("Nenhuma dívida encontrada para este cliente.")
        pausar_tela()
        return

    print(f"\n--- Dívidas de {dividas_deste_cliente[0].cliente.nome} ---")
    for d in dividas_deste_cliente:
        print(f"ID: {d.id_divida} | Vencimento: {d.data_vencimento} | Valor Original: R${d.valor_original:.2f} | SALDO A PAGAR: R${d.saldo_devedor:.2f} ({d.status})")
    
    try:
        id_divida_escolhida = int(input("\nDigite o ID da Dívida para dar baixa: "))
    except ValueError:
        print("ID inválido.")
        pausar_tela()
        return

    divida_alvo = None
    for d in banco_dividas:
        if d.id_divida == id_divida_escolhida:
            divida_alvo = d
            break
            
    if not divida_alvo:
        print("Dívida não encontrada.")
        pausar_tela()
        return

    if divida_alvo.status == "Paga":
        print("Esta dívida já está quitada!")
        pausar_tela()
        return

    print(f"\n>> Pagando dívida de R${divida_alvo.saldo_devedor:.2f}")
    try:
        valor_pagamento = float(input("Qual o valor do pagamento? R$ "))
    except ValueError:
        print("Valor inválido.")
        pausar_tela()
        return

    if valor_pagamento <= 0:
        print("O valor deve ser positivo.")
        pausar_tela()
        return

    meio = input("Meio de pagamento (Pix, Dinheiro, Cartão): ")
    
    usuario_atual = "Admin" 

    novo_id_pagto = len(divida_alvo.historico_pagamentos) + 1
    
    novo_pagamento = Pagamento(novo_id_pagto, divida_alvo, valor_pagamento, meio, usuario_atual)
    
    divida_alvo.aplicar_pagamento(novo_pagamento)
    
    print("\nPagamento registrado com sucesso!")
    print(f"Novo Saldo Devedor: R${divida_alvo.saldo_devedor:.2f}")
    print(f"Status da Dívida: {divida_alvo.status}")
    pausar_tela()

def realizar_renegociacao():
    print("\n--- RENEGOCIAÇÃO DE DÍVIDA ---")
    
    try:
        id_divida = int(input("Digite o ID da Dívida a renegociar: "))
    except ValueError:
        print("ID inválido.")
        pausar_tela()
        return

    divida_alvo = None
    for d in banco_dividas:
        if d.id_divida == id_divida:
            divida_alvo = d
            break
            
    if not divida_alvo:
        print("Dívida não encontrada.")
        pausar_tela()
        return
        
    if divida_alvo.status == "Paga":
        print("Não é possível renegociar uma dívida já paga.")
        return

    print(f"Cliente: {divida_alvo.cliente.nome}")
    print(f"Vencimento Atual: {divida_alvo.data_vencimento}")
    print(f"Valor Atual: R${divida_alvo.saldo_devedor:.2f}")

    try:
        dias_novo_prazo = int(input("Novo prazo (em dias a partir de hoje): "))
        juros = float(input("Juros de renegociação (%) (ex: 10 para 10%): "))
    except ValueError:
        print("Dados inválidos.")
        pausar_tela()
        return

    nova_data = date.today() + timedelta(days=dias_novo_prazo)
    
    usuario_atual = "Dono" 
    
    divida_alvo.renegociar(nova_data, juros, usuario_atual)