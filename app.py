from flask import Flask, request, url_for
import dictionary

app = Flask(__name__)
dictionary.load_data()  # load saved data on startup

# ---------- HOME ----------
@app.route("/")
def home():
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
        <h1>Store Tracker</h1>
        <p style="text-align:center; color:#555;">
            Simple stock and sales tracking system
        </p>
    </div>
    </body>
    </html>
    """

# ---------- PRODUCTS ----------
@app.route("/products")
def view_products():
    html = f"""
    <html>
    <head>
        <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
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
    if request.method == "POST":
        dictionary.add_product(
            request.form["name"],
            float(request.form["price"]),
            int(request.form["stock"])
        )
        return "✅ Product added!"
    return f"""
    <html>
    <head>
        <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
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
    if request.method == "POST":
        return dictionary.sell_product(
            request.form["name"],
            int(request.form["quantity"])
        )
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

if __name__ == "__main__":
    # Host 0.0.0.0 so cloud can access it
    app.run(host="0.0.0.0", port=5000)
