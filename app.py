from flask import Flask, request, url_for, redirect, session
import dictionary

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session management
dictionary.load_data()

# ---------- HOME ----------
@app.route("/")
def home():
    """Home page"""
    # Auth links for not logged-in users
    auth_links = ''
    if "username" not in session:
        auth_links = '<p style="text-align:center;"><a href="/signup">Sign Up</a> | <a href="/login">Login</a></p>'

    # Logout link for logged-in users
    logout_link = ''
    if "username" in session:
        logout_link = '<a href="/logout">Logout</a>'

    return f"""
    <html>
    <head>
        <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
    <div class="container">
        <div class="nav">
            <a href="/">Home</a>
            <a href="/products">Products</a>
            <a href="/add">Add</a>
            <a href="/sell">Sell</a>
            {logout_link}
        </div>
        <h1>Store Tracker</h1>
        <p style="text-align:center; color:#555;">
            Simple stock and sales tracking system
        </p>
        {auth_links}
    </div>
    </body>
    </html>
    """

# ---------- VIEW PRODUCTS ----------
@app.route("/products")
def view_products():
    """Show all products with total sales"""
    logout_link = ''
    if "username" in session:
        logout_link = '<a href="/logout">Logout</a>'

    html = f"""
    <html>
    <head>
        <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
    <div class="container">
        <div class="nav">
            <a href="/">Home</a>
            <a href="/products">Products</a>
            <a href="/add">Add</a>
            <a href="/sell">Sell</a>
            {logout_link}
        </div>
        <p style="text-align:center; font-weight:bold;">
            Total Sales: ₱{dictionary.total_sales}
        </p>
        <h2>Products</h2>
    """
    for name, info in dictionary.products.items():
        html += f"""
        <div class="product">
            {name} - ₱{info['price']} | Stock: {info['stock']}
        </div>
        """
    html += """
    </div>
    </body>
    </html>
    """
    return html

# ---------- ADD PRODUCT ----------
@app.route("/add", methods=["GET", "POST"])
def add():
    """Add a new product"""
    logout_link = ''
    if "username" in session:
        logout_link = '<a href="/logout">Logout</a>'

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
        <div class="nav">
            <a href="/">Home</a>
            <a href="/products">Products</a>
            <a href="/add">Add</a>
            <a href="/sell">Sell</a>
            {logout_link}
        </div>
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
def sell():
    """Sell a product"""
    logout_link = ''
    if "username" in session:
        logout_link = '<a href="/logout">Logout</a>'

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
        <div class="nav">
            <a href="/">Home</a>
            <a href="/products">Products</a>
            <a href="/add">Add</a>
            <a href="/sell">Sell</a>
            {logout_link}
        </div>
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

# ---------- SIGN UP ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Sign up page (separate, not in main nav)"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        message = dictionary.signup(username, password)
        if message.startswith("✅"):
            session["username"] = username
            return redirect("/")  # redirect to main app after signup
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
def login():
    """Login page (separate, not in main nav)"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        message = dictionary.login(username, password)
        if message.startswith("✅"):
            session["username"] = username
            return redirect("/")  # redirect to main app after login
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
    """Log the user out"""
    session.pop("username", None)
    return redirect("/")
    
if __name__ == "__main__":
    # Cloud-ready
    app.run(host="0.0.0.0", port=5000)
