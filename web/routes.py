from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from web.models import db, Cliente, Usuario, Divida, Pagamento
from datetime import datetime, date, timedelta

def register_routes(app):
    bp = Blueprint('main', __name__)

    @bp.route('/')
    def index():
        return redirect(url_for('main.listar_clientes'))

    # ---------------- Clientes ----------------
    @bp.route('/clientes')
    def listar_clientes():
        clientes = Cliente.query.all()
        return render_template('clientes_list.html', clientes=clientes)

    @bp.route('/clientes/novo', methods=['GET', 'POST'])
    def novo_cliente():
        if request.method == 'POST':
            nome = request.form.get('nome')
            cpf = request.form.get('cpf')
            celular = request.form.get('celular')
            endereco = request.form.get('endereco')
            nivel = request.form.get('nivel') or 'Novo'
            limite = float(request.form.get('limite') or 200.0)

            cliente = Cliente(nome=nome, cpf=cpf, celular=celular, endereco=endereco, nivel_confianca=nivel, limite_credito=limite)
            db.session.add(cliente)
            db.session.commit()
            flash('Cliente cadastrado com sucesso.')
            return redirect(url_for('main.listar_clientes'))

        return render_template('clientes_form.html')

    # ---------------- Usuários ----------------
    @bp.route('/usuarios')
    def listar_usuarios():
        usuarios = Usuario.query.all()
        return render_template('usuarios_list.html', usuarios=usuarios)

    @bp.route('/usuarios/novo', methods=['GET', 'POST'])
    def novo_usuario():
        from werkzeug.security import generate_password_hash
        if request.method == 'POST':
            nome = request.form.get('nome')
            cpf = request.form.get('cpf')
            email = request.form.get('email')
            tipo = request.form.get('tipo') or 'Caixa'
            senha = request.form.get('senha')
            senha_hash = generate_password_hash(senha or '')

            usuario = Usuario(nome=nome, cpf=cpf, email=email, tipo=tipo, senha_hash=senha_hash)
            db.session.add(usuario)
            db.session.commit()
            flash('Usuário cadastrado com sucesso.')
            return redirect(url_for('main.listar_usuarios'))

        return render_template('usuarios_form.html')

    # ---------------- Dívidas / Financeiro ----------------
    @bp.route('/dividas')
    def listar_dividas():
        dividas = Divida.query.all()
        return render_template('dividas_list.html', dividas=dividas)

    @bp.route('/dividas/novo', methods=['GET', 'POST'])
    def novo_divida():
        clientes = Cliente.query.all()
        if request.method == 'POST':
            cliente_id = int(request.form.get('cliente_id'))
            valor = float(request.form.get('valor'))
            descricao = request.form.get('descricao') or ''
            prazo = int(request.form.get('prazo') or 0)

            cliente = Cliente.query.get(cliente_id)
            if not cliente:
                flash('Cliente não encontrado.')
                return redirect(url_for('main.novo_divida'))

            data_venc = date.today() + timedelta(days=prazo)
            divida = Divida(cliente_id=cliente.id, valor_original=valor, saldo_devedor=valor, data_vencimento=data_venc, descricao=descricao)
            db.session.add(divida)
            db.session.commit()
            flash('Dívida registrada com sucesso.')
            return redirect(url_for('main.listar_dividas'))

        return render_template('dividas_form.html', clientes=clientes)

    @bp.route('/dividas/<int:divida_id>/pagar', methods=['GET', 'POST'])
    def pagar_divida(divida_id):
        divida = Divida.query.get_or_404(divida_id)
        if request.method == 'POST':
            valor = float(request.form.get('valor'))
            meio = request.form.get('meio')
            usuario = request.form.get('usuario') or 'Operador'

            pagamento = Pagamento(divida_id=divida.id, valor=valor, meio_pagamento=meio, usuario_responsavel=usuario)
            divida.aplicar_pagamento(pagamento)
            db.session.add(pagamento)
            db.session.commit()
            flash('Pagamento registrado.')
            return redirect(url_for('main.listar_dividas'))

        return render_template('pagar_form.html', divida=divida)

    # ---------------- Relatórios ----------------
    @bp.route('/relatorios/dashboard')
    def relatorio_dashboard():
        dividas = Divida.query.all()
        hoje = date.today()
        total_a_receber = sum(d.saldo_devedor for d in dividas if d.status != 'Paga')
        total_vencido = sum(d.saldo_devedor for d in dividas if d.status != 'Paga' and d.data_vencimento < hoje)
        qtd_pagas = sum(1 for d in dividas if d.status == 'Paga')

        ranking = {}
        for d in dividas:
            if d.status == 'Paga':
                continue
            nome = d.cliente.nome
            ranking[nome] = ranking.get(nome, 0) + d.saldo_devedor

        ranking_ordenado = sorted(ranking.items(), key=lambda x: x[1], reverse=True)

        return render_template('relatorios_dashboard.html', total_a_receber=total_a_receber, total_vencido=total_vencido, qtd_pagas=qtd_pagas, ranking=ranking_ordenado[:5])

    @bp.route('/relatorios/extrato', methods=['GET', 'POST'])
    def relatorio_extrato():
        cliente = None
        dividas_cliente = []
        total = 0.0
        if request.method == 'POST':
            termo = request.form.get('termo')
            if termo.isdigit():
                cliente = Cliente.query.get(int(termo))
            else:
                cliente = Cliente.query.filter(Cliente.nome.ilike(f"%{termo}%")).first()

            if cliente:
                dividas_cliente = Divida.query.filter_by(cliente_id=cliente.id).all()
                total = sum(d.saldo_devedor for d in dividas_cliente)

        return render_template('relatorios_extrato.html', cliente=cliente, dividas=dividas_cliente, total=total)

    app.register_blueprint(bp)
