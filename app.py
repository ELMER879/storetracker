from flask import Flask, request, url_for, redirect, session
import dictionary
import database
database.init_db()


app = Flask(__name__)
app.secret_key = "supersecretkey"
dictionary.load_data()


# ---------- NAVIGATION GENERATOR ----------
def generate_nav():
    if "username" in session:
        # logged-in user
        nav = f"""
        <a href="/">Home</a>
        <a href="/products">Products</a>
        <a href="/add">Add</a>
        <a href="/sell">Sell</a>
        """
        if dictionary.users[session['username']].get("is_admin", False):
            nav += "<a href='/admin'>Admin</a>"
        nav += "<a href='/logout'>Logout</a>"
    else:
        # guest
        nav = """
        <a href="/">Home</a>
        <a href="/signup">Sign Up</a>
        <a href="/login">Login</a>
        """
    return f'<div class="nav">{nav}</div>'


# ---------- HOME ----------
@app.route("/")
def home():
    nav_html = generate_nav()
    if "username" in session:
        username = session["username"]
        return f"""
        <html>
        <head>
            <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
        <div class="container">
            {nav_html}
            <h1>Welcome, {username}!</h1>
            <p style="text-align:center; color:#555;">Use the navigation to view products, add or sell items.</p>
        </div>
        </body>
        </html>
        """
    else:
        return f"""
        <html>
        <head>
            <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
        <div class="container">
            {nav_html}
            <h1>Welcome to Store Tracker</h1>
            <p style="text-align:center; color:#555;">Please Sign Up or Login to access the store.</p>
        </div>
        </body>
        </html>
        """


# ---------- PRODUCTS ----------
@app.route("/products")
def products_page():
    if "username" not in session:
        return redirect("/")
    nav_html = generate_nav()
    products_html = ""
    for name, info in dictionary.get.products.items():
        products_html += f"<div class='product'>{name} - ₱{info['price']} | Stock: {info['stock']}</div>"

    return f"""
    <html>
    <head>
            <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
    <body>
        <div class="container">
            {nav_html}
            <h2>Products</h2>
            {products_html}
            <p style="text-align:center; font-weight:bold;">Total Sales: ₱{dictionary.total_sales}</p>
        </div>
    </body>
    </html>
    """


# ---------- ADD PRODUCT ----------
@app.route("/add", methods=["GET", "POST"])
def add_page():
    if "username" not in session:
        return redirect("/")
    nav_html = generate_nav()
    if request.method == "POST":
        dictionary.add_product(
            request.form["name"],
            float(request.form["price"]),
            int(request.form["stock"])
        )
        return redirect("/products")
    return f"""
    <html>
    <head>
            <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
    <body>
        <div class="container">
            {nav_html}
            <h2>Add Product</h2>
            <form method="post">
                <input name="name" placeholder="Product name" required>
                <input name="price" placeholder="Price" required>
                <input name="stock" placeholder="Stock" required>
                <button>Add Product</button>
            </form>
        </div>
    </body>
    </html>
    """


# ---------- SELL PRODUCT ----------
@app.route("/sell", methods=["GET", "POST"])
def sell_page():
    if "username" not in session:
        return redirect("/")
    nav_html = generate_nav()
    if request.method == "POST":
        dictionary.sell_product(
            request.form["name"],
            int(request.form["quantity"])
        )
        return redirect("/products")
    return f"""
    <html>
         <head>
            <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
    <body>
        <div class="container">
            {nav_html}
            <h2>Sell Product</h2>
            <form method="post">
                <input name="name" placeholder="Product name" required>
                <input name="quantity" type="number" placeholder="Quantity" required>
                <button>Sell Product</button>
            </form>
        </div>
    </body>
    </html>
    """


# ---------- SIGNUP ----------
@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    nav_html = generate_nav()
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        message = dictionary.signup(username, password)
        return message
    return f"""
    <html>
        <head>
            <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
    <body>
        <div class="container">
            {nav_html}
            <h2>Sign Up</h2>
            <form method="post">
                <input name="username" placeholder="Username" required>
                <input name="password" type="password" placeholder="Password" required>
                <button>Sign Up</button>
            </form>
            <p>Already have an account? <a href="/login">Login</a></p>
        </div>
    </body>
    </html>
    """


# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login_page():
    nav_html = generate_nav()
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        message = dictionary.login(username, password)
        if message.startswith("✅"):
            session["username"] = username
            return redirect("/")
        else:
            return message
    return f"""
    <html>
        <head>
            <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
    <body>
        <div class="container">
            {nav_html}
            <h2>Login</h2>
            <form method="post">
                <input name="username" placeholder="Username" required>
                <input name="password" type="password" placeholder="Password" required>
                <button>Login</button>
            </form>
            <p>Don't have an account? <a href="/signup">Sign Up</a></p>
        </div>
    </body>
    </html>
    """


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")


# ---------- ADMIN PANEL ----------
@app.route("/admin", methods=["GET", "POST"])
def admin_page():
    if "username" not in session:
        return "❌ Access denied"
    current_user = session["username"]
    if not dictionary.get.users.get(current_user, {}).get("is_admin", False):
        return "❌ Access denied"
    nav_html = generate_nav()

    # Approve users
    if request.method == "POST":
        approve_user = request.form["approve"]
        if approve_user in dictionary.users:
            dictionary.get.users[approve_user]["approved"] = True
            dictionary.save_data()

    users_html = ""
    for username, info in dictionary.users.items():
        if info.get("is_admin"):
            continue
        status = "✅ Approved" if info["approved"] else "❌ Pending"
        approve_button = "" if info["approved"] else f"""
            <form method='post' style='display:inline;'>
                <input type='hidden' name='approve' value='{username}'>
                <button>Approve</button>
            </form>
        """
        users_html += f"<div>{username} - {status} {approve_button}</div>"

    return f"""
    <html>
        <head>
            <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
    <body>
        <div class="container">
            {nav_html}
            <h2>Admin Panel - Approve Users</h2>
            <p>Logged in as admin: {current_user}</p>
            {users_html}
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
