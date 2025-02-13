import base64

from flask import render_template, jsonify, request, redirect, session, g
from app import create_app
from app.database import buscar_dados_usuario_por_email, buscar_usuario_por_id, execute_sql
from app.utils.criptografia_senhas import verificar_senha

app = create_app()


@app.before_request
def carregar_foto_usuario():
    usuario_id = session.get('usuario')
    if usuario_id:
        query = """
            SELECT foto FROM Usuario WHERE id_usuario = %s;
            """
        foto = execute_sql(query, (usuario_id,))
        if foto and foto[0]:
            foto_base64 = base64.b64encode(foto[0]).decode('utf-8')
            g.foto_url = f"data:image/jpeg;base64,{foto_base64}"
        else:
            g.foto_url = None
    else:
        g.foto = None

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
