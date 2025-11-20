import hashlib
from modelos.pessoas import Usuario
from utils.utils import limpar_tela, pausar_tela

banco_usuarios = []

def criptografar_senha(senha_texto_plano):
    return hashlib.sha256(senha_texto_plano.encode()).hexdigest()

def cadastrar_usuario():
    limpar_tela()
    print("\n--- NOVO CADASTRO DE USUÁRIO ---")
    nome = input("Nome completo: ")
    cpf = input("CPF: ")
    email = input("Email: ")
    
    print("Tipos: 1-Administrador, 2-Caixa")
    tipo = "Administrador" if input("Selecione: ") == "1" else "Caixa"
    
    senha = criptografar_senha(input("Senha: "))
    
    novo_id = len(banco_usuarios) + 1
    usuario = Usuario(novo_id, nome, cpf, email, senha, tipo)
    
    banco_usuarios.append(usuario)
    print(f"Sucesso! Usuário {nome} (ID: {novo_id}) cadastrado.")

    pausar_tela()

def listar_usuarios():
    limpar_tela()
    print("\n--- LISTA DE USUÁRIOS ---")
    for u in banco_usuarios:
        print(f"ID: {u.id_usuario} | {u.nome} | {u.tipo}")
    
    pausar_tela()