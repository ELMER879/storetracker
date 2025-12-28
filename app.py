from flask import Flask, request, url_for, redirect
import dictionary

app = Flask(__name__)
dictionary.load_data()  # Load saved data on startup

# ---------- HOME ----------
@app.route("/")
def home():
    """Home page of the store"""
    return f"""
    <html>
    <head>
        <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
    <div class="container">
        <!-- Navigation (only main app links) -->
        <div class="nav">
            <a href="/">Home</a>
            <a href="/products">Products</a>
            <a href="/add">Add</a>
            <a href="/sell">Sell</a>
        </div>
        <h1>Store Tracker</h1>
        <p style="text-align:center; color:#555;">
            Simple stock and sales tracking system
        </p>
    </div>
    </body>
    </html>
    """

# ---------- VIEW PRODUCTS ----------
@app.route("/products")
def view_products():
    """Show all products with total sales"""
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
    if request.method == "POST":
        dictionary.add_product(
            request.form["name"],
            float(request.form["price"]),
            int(request.form["stock"])
        )
        return redirect("/products")  # redirect to products after adding
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
    if request.method == "POST":
        dictionary.sell_product(
            request.form["name"],
            int(request.form["quantity"])
        )
        return redirect("/products")  # redirect to products after selling
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
    """User registration page (separate, not in main nav)"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        message = dictionary.signup(username, password)
        if message.startswith("✅"):
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
    """User login page (separate, not in main nav)"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        message = dictionary.login(username, password)
        if message.startswith("✅"):
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

if __name__ == "__main__":
    # Cloud-ready: accessible externally
    app.run(host="0.0.0.0", port=5000)
