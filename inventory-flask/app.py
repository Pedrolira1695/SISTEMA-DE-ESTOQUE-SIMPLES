from flask import Flask, render_template, request, redirect, url_for, session, flash
from controllers.auth_controller import AuthController
from controllers.inventory_controller import InventoryController
import socket

app = Flask(__name__)
app.secret_key = "supersecretkey"

auth_controller = AuthController()
inventory_controller = InventoryController()
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("Você precisa estar logado.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def index():
    items = inventory_controller.get_all_items()
    return render_template("index.html", items=items, username=session["username"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if auth_controller.login(username, password):
            session["username"] = username
            flash("Login efetuado!")
            return redirect(url_for("index"))
        else:
            flash("Usuário ou senha incorretos.")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if auth_controller.register(username, password):
            flash("Usuário registrado! Faça login.")
            return redirect(url_for("login"))
        else:
            flash("Usuário já existe.")
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    session.pop("username", None)
    flash("Você saiu do sistema.")
    return redirect(url_for("login"))

@app.route("/add_item", methods=["POST"])
@login_required
def add_item():
    try:
        item_id = int(request.form["item_id"])
        name = request.form["name"]
        quantity = int(request.form["quantity"])
        inventory_controller.add_item(item_id, name, quantity, session["username"])
        flash("Item adicionado!")
    except ValueError:
        flash("Dados inválidos.")
    return redirect(url_for("index"))

@app.route("/remove_item", methods=["POST"])
@login_required
def remove_item():
    try:
        item_id = int(request.form["item_id"])
        inventory_controller.remove_item(item_id, session["username"])
        flash("Item removido!")
    except ValueError:
        flash("ID inválido.")
    return redirect(url_for("index"))

@app.route("/update_quantity", methods=["POST"])
@login_required
def update_quantity():
    try:
        item_id = int(request.form["item_id"])
        amount = int(request.form["amount"])
        inventory_controller.update_quantity(item_id, amount, session["username"])
        flash("Quantidade atualizada!")
    except ValueError:
        flash("Dados inválidos.")
    return redirect(url_for("index"))

@app.route("/movimentacoes")
@login_required
def movimentacoes():
    logs = inventory_controller.get_movimentacoes()
    return render_template("movimentacoes.html", logs=logs)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)