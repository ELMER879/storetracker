from flask import Flask, request, redirect, session, url_for
import dictionary
import database

app = Flask(__name__)
app.secret_key = "supersecretkey"

database.init_db()


def nav():
    if "username" in session:
        links = """
        <a href="/">Home</a>
        <a href="/products">Products</a>
        <a href="/add">Add</a>
        <a href="/sell">Sell</a>
        """
        if dictionary.is_admin(session["username"]):
            links += '<a href="/admin">Admin</a>'
        links += '<a href="/logout">Logout</a>'
    else:
        links = """
        <a href="/">Home</a>
        <a href="/signup">Sign Up</a>
        <a href="/login">Login</a>
        """
    return f'<div class="nav">{links}</div>'


@app.route("/")
def home():
    return f"""
    <html>
    <head>
        <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
    </head>
    <body>
    <div class="container">
        {nav()}
        <h1>Store Tracker</h1>
        <p style="text-align:center;">Welcome!</p>
    </div>
    </body>
    </html>
    """


@app.route("/products")
def products():
    if "username" not in session:
        return redirect("/")
    rows = dictionary.get_products()
    items = "".join(
        f"<div class='product'>{n} - ₱{p} | Stock: {s}</div>"
        for n, p, s in rows
    )

    return f"""
    <html>
    <head><link rel="stylesheet" href="{url_for('static', filename='style.css')}"></head>
    <body>
    <div class="container">
        {nav()}
        <h2>Products</h2>
        {items}
        <p><b>Total Sales:</b> ₱{dictionary.total_sales()}</p>
    </div>
    </body>
    </html>
    """


@app.route("/add", methods=["GET", "POST"])
def add():
    if "username" not in session:
        return redirect("/")
    if request.method == "POST":
        dictionary.add_product(
            request.form["name"],
            float(request.form["price"]),
            int(request.form["stock"])
        )
        return redirect("/products")

    return f"""
    <html>
    <head><link rel="stylesheet" href="{url_for('static', filename='style.css')}"></head>
    <body>
    <div class="container">
        {nav()}
        <h2>Add Product</h2>
        <form method="post">
            <input name="name" required>
            <input name="price" required>
            <input name="stock" required>
            <button>Add</button>
        </form>
    </div>
    </body>
    </html>
    """


@app.route("/sell", methods=["GET", "POST"])
def sell():
    if "username" not in session:
        return redirect("/")
    if request.method == "POST":
        dictionary.sell_product(
            request.form["name"],
            int(request.form["quantity"])
        )
        return redirect("/products")

    return f"""
    <html>
    <head><link rel="stylesheet" href="{url_for('static', filename='style.css')}"></head>
    <body>
    <div class="container">
        {nav()}
        <h2>Sell Product</h2>
        <form method="post">
            <input name="name" required>
            <input name="quantity" type="number" required>
            <button>Sell</button>
        </form>
    </div>
    </body>
    </html>
    """


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        return dictionary.signup(
            request.form["username"],
            request.form["password"]
        )

    return f"""
    <html>
    <head><link rel="stylesheet" href="{url_for('static', filename='style.css')}"></head>
    <body>
    <div class="container">
        {nav()}
        <h2>Sign Up</h2>
        <form method="post">
            <input name="username" required>
            <input name="password" type="password" required>
            <button>Sign Up</button>
        </form>
    </div>
    </body>
    </html>
    """


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        msg = dictionary.login(
            request.form["username"],
            request.form["password"]
        )
        if msg.startswith("✅"):
            session["username"] = request.form["username"]
            return redirect("/")
        return msg

    return f"""
    <html>
    <head><link rel="stylesheet" href="{url_for('static', filename='style.css')}"></head>
    <body>
    <div class="container">
        {nav()}
        <h2>Login</h2>
        <form method="post">
            <input name="username" required>
            <input name="password" type="password" required>
            <button>Login</button>
        </form>
    </div>
    </body>
    </html>
    """


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "username" not in session or not dictionary.is_admin(session["username"]):
        return "❌ Access denied"

    if request.method == "POST":
        dictionary.approve_user(request.form["approve"])

    users = dictionary.get_users()
    rows = ""
    for u, approved, is_admin in users:
        if is_admin:
            continue
        rows += f"""
        <div>{u} - {'Approved' if approved else 'Pending'}
        {"<form method='post'><input type='hidden' name='approve' value='"+u+"'><button>Approve</button></form>" if not approved else ""}
        </div>
        """

    return f"""
    <html>
    <head><link rel="stylesheet" href="{url_for('static', filename='style.css')}"></head>
    <body>
    <div class="container">
        {nav()}
        <h2>Admin Panel</h2>
        {rows}
    </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
