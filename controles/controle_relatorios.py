from datetime import date
from controles.controle_financeiro import banco_dividas
from controles.controle_clientes import banco_clientes
from utils.utils import limpar_tela, pausar_tela

def exibir_dashboard():
    limpar_tela()
    print("\n=== DASHBOARD FINANCEIRO (VISÃO DO DONO) ===")
    
    total_a_receber = 0.0
    total_vencido = 0.0
    qtd_dividas_pagas = 0
    
    ranking_devedores = {}
    
    hoje = date.today()

    for divida in banco_dividas:
        if divida.status == "Paga":
            qtd_dividas_pagas += 1
            continue 

        total_a_receber += divida.saldo_devedor
        
        if divida.data_vencimento < hoje:
            total_vencido += divida.saldo_devedor
        
        nome = divida.cliente.nome
        if nome not in ranking_devedores:
            ranking_devedores[nome] = 0.0
        ranking_devedores[nome] += divida.saldo_devedor

    print(f"\nValor Total a Receber: R$ {total_a_receber:.2f}")
    print(f"Valor Total VENCIDO:   R$ {total_vencido:.2f}")
    print(f"Dívidas Quitadas:      {qtd_dividas_pagas}")

    print("\nTOP 5 MAIORES DEVEDORES:")
    if not ranking_devedores:
        print("   (Nenhum devedor no momento)")
    else:
        # key=lambda x: x[1] diz ao Python para ordenar pelo valor, não pelo nome
        ranking_ordenado = sorted(ranking_devedores.items(), key=lambda x: x[1], reverse=True)
        
        for i, (nome, valor) in enumerate(ranking_ordenado[:5]):
            print(f"   {i+1}º {nome}: R$ {valor:.2f}")

    pausar_tela()

def gerar_extrato_cliente():
    limpar_tela()
    print("\n--- EXTRATO DETALHADO DO CLIENTE ---")
    
    termo = input("Digite o Nome ou ID do cliente: ").lower()
    
    cliente_encontrado = None
    for c in banco_clientes:
        if str(c.id_cliente) == termo or termo in c.nome.lower():
            cliente_encontrado = c
            break
            
    if not cliente_encontrado:
        print("Cliente não encontrado.")
        return

    print(f"\nCliente: {cliente_encontrado.nome} | CPF: {cliente_encontrado.cpf}")
    print(f"Endereço: {cliente_encontrado.endereco}")
    print("="*50)
    
    dividas_cliente = [d for d in banco_dividas if d.cliente.id_cliente == cliente_encontrado.id_cliente]
    
    if not dividas_cliente:
        print("Este cliente não possui histórico de compras.")
        return

    total_devido = 0
    
    for d in dividas_cliente:
        print(f"\n COMPRA (ID: {d.id_divida}) - {d.data_venda}")
        print(f"   Item: {d.descricao}")
        print(f"   Valor Original: R$ {d.valor_original:.2f}")
        print(f"   Vencimento: {d.data_vencimento} | Status: {d.status}")
        
        if d.historico_pagamentos:
            print("   --- Pagamentos Efetuados ---")
            for p in d.historico_pagamentos:
                print(f"{p.data_pagamento}: R$ {p.valor:.2f} ({p.meio_pagamento})")
        
        if d.saldo_devedor > 0:
            print(f"   >> RESTA PAGAR: R$ {d.saldo_devedor:.2f}")
            total_devido += d.saldo_devedor
            
        print("-" * 50)
        
    print(f"\nTOTAL GERAL DEVIDO: R$ {total_devido:.2f}")

    pausar_tela()