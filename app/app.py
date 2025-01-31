from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def login():
    return render_template("./login.html")


@app.route("/inicio")
def inicio():
    return render_template("./inicio.html")


@app.route("/cadastros")
def cadastro():
    return render_template("./cadastros.html")


if __name__ == "__main__":
    app.run(debug=True)
