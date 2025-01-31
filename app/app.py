from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Simulação de dados vindos do banco de dados
pacientes = [
    {"nome": "Marley (Ana Luiza Campos)"},
    {"nome": "Catherine (Célio Eduardo Júnior)"},
    {"nome": "Thor (João Pedro Souza)"},
    {"nome": "Mel (Fernanda Oliveira)"},
    {"nome": "Rex (Carlos Eduardo Santos)"}
]


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/inicio")
def inicio():
    return render_template("inicio.html")


@app.route("/cadastros")
def cadastro():
    return render_template("cadastros.html")


@app.route("/pacientes")
def pacientes_page():
    return render_template('pacientes.html', pacientes=pacientes)


@app.route('/api/pacientes')
def get_pacientes():
    return jsonify(pacientes)


if __name__ == "__main__":
    app.run(debug=True)
