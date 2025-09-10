import base64

from flask import render_template, jsonify, request, redirect, session, g
from __init__ import create_app
from database import buscar_dados_usuario_por_email, buscar_usuario_por_id, execute_sql
from utils.criptografia_senhas import verificar_senha

app = create_app()


@app.before_request
def carregar_foto_usuario():
    usuario_id = session.get('usuario')
    if usuario_id:
        query = """
            SELECT foto FROM Usuario_Foto WHERE id_usuario = %s;
            """
        foto = execute_sql(query, (usuario_id,), fetch_one=True)

        if not foto:
            print('Nenhum resultado retornado pelo banco de dados')
            g.foto_url = None
            return

        foto_binario = foto[0]

        if isinstance(foto_binario, memoryview):
            print('Convertendo memoryview para bytes')
            foto_binario = foto_binario.tobytes()

        if not isinstance(foto_binario, bytes):
            print('Tipo inesperado: ', type(foto_binario))
            return

        foto_base64 = base64.b64encode(foto_binario).decode('utf-8')
        g.foto_url = f"data:image/jpeg;base64,{foto_base64}"
    else:
        print('Nenhum usuário logado')
        g.foto_url = None


@app.route('/', methods=['GET', 'POST'])
def login():
    if 'usuario' in session:
        return redirect('/inicio')
    else:
        if request.method == 'POST':
            email = request.form.get('email')
            senha = request.form.get('senha')

            usuario = buscar_dados_usuario_por_email(email.lower())  # [id, email, senha]
            # Verificar se o usuário existe no banco de dados
            # Se sim, verificar se a senha está correta
            # Se sim, redirecionar para a página inicial

            if usuario and verificar_senha(senha, usuario[2]):
                session['usuario'] = usuario[0]  # Salva o id do usuário na sessão
                return redirect('/inicio')
            elif not usuario:
                return jsonify({"erro": "Usuário não encontrado!"}), 404
            else:
                return jsonify({"erro": "Senha incorreta!"}), 401

    return render_template('login.html')


@app.context_processor
def inject_user():
    # Caso o usuário entre nessa página, com certeza ele estará logado.
    usuario_id = session.get('usuario')
    usuario = {"nome": "Usuário"}  # Valor padrão caso o usuário não seja encontrado
    if usuario_id:
        user_data = buscar_usuario_por_id(usuario_id)
        if user_data:
            usuario = {
                "id": user_data[0],
                "nome": user_data[1],
                "email": user_data[2],
            }

    return {'usuario': usuario}


@app.route('/inicio')
def inicio():
    if 'usuario' in session:
        return render_template('inicio.html')
    return redirect('/')


# Tela de cadastros e suas funcionalidades
@app.route('/cadastros')
def cadastro():
    return render_template('cadastros.html')


# Tela de consultas e suas funcionalidades
@app.route('/consultas')
def consultas():
    return render_template('consultas.html')


@app.route('/sair')
def sair():
    session.clear()  # Limpa a sessão
    return redirect('/')


# back-end

if __name__ == '__main__':
    app.run(debug=True)
