from datetime import datetime
from os.path import join as path_join
from flask import Flask, render_template, request

PASTA_CARTAS = "./cartas/"
MSG_TAMANHO_MAX_LINHA = 80

app = Flask(__name__)


def gerar_caminho_de_carta(remetente):
    now = datetime.now()
    id_carta = str(now.timestamp())
    nome_carta = 'Carta-{}-{}.txt'.format(remetente, id_carta)
    return path_join(PASTA_CARTAS, nome_carta)


def preparar_mensagem(msg):
    linhas = []
    current = ''

    i = 0
    for c in msg:
        current += c
        if i == MSG_TAMANHO_MAX_LINHA:
            linhas.append(current)
            current = ''
            i = 0
        i += 1
    
    return '\n'.join(linhas)


def salvar_carta(data, destinatario, msg, remetente):
    print("Salvando carta...")

    caminho_carta = gerar_caminho_de_carta(remetente)

    msg_preparada = preparar_mensagem(msg)
    print(msg_preparada)
    conteudo = '{}\n{}\n\n{}\n\n{}'.format(data, destinatario, msg_preparada, remetente)

    with open(caminho_carta, 'w') as carta_f:
        carta_f.write(conteudo)


def capturar_info_de_login():
    username = None
    password = None

    with open('./login.txt', 'r') as login_file:
        for line in login_file:
            if "Username:" in line:
                username = line.split(":")[1].strip()
            elif "Password:" in line:
                password = line.split(":")[1].strip()
    
    return (username, password)

username, password = capturar_info_de_login()


@app.route("/")
def cartas():
    return render_template("login.html")


@app.route("/", methods = ["POST"])
def login():
    if request.method == "POST":
        nome = request.form.get("nome")
        senha = request.form.get("senha")

        if (nome == username and senha == password) or request.form.get("logged") == "logged":
            return render_template("cartas.html")
        else:
            return render_template("incorreto.html")


@app.route("/send/", methods = ["POST"])
def enviar():
    data = request.form.get("data")
    dest = request.form.get("destinatario")
    msg = request.form.get("mensagem")
    remt = request.form.get("remetente")
    print("Nova carta recebida de: " + remt)
    salvar_carta(data, dest, msg, remt)
    return render_template("enviado.html")


app.run(port=8080)