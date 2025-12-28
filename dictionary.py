import database


# ---------- PRODUCTS ----------
def get_products():
    with database.get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT name, price, stock FROM products")
        return cur.fetchall()


def add_product(name, price, stock):
    with database.get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
        INSERT OR REPLACE INTO products (name, price, stock)
        VALUES (?, ?, ?)
        """, (name, price, stock))
        conn.commit()


def sell_product(name, quantity):
    with database.get_db() as conn:
        cur = conn.cursor()

        cur.execute("SELECT price, stock FROM products WHERE name=?", (name,))
        product = cur.fetchone()

        if not product:
            return "❌ Product not found"

        price, stock = product

        if stock < quantity:
            return "❌ Not enough stock"

        new_stock = stock - quantity
        total = price * quantity

        cur.execute("UPDATE products SET stock=? WHERE name=?", (new_stock, name))
        cur.execute("INSERT INTO sales (amount) VALUES (?)", (total,))
        conn.commit()

        return f"✅ Sale successful! Total: ₱{total}"


def total_sales():
    with database.get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT SUM(amount) FROM sales")
        result = cur.fetchone()[0]
        return result if result else 0


# ---------- USERS ----------
def signup(username, password):
    with database.get_db() as conn:
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM users")
        user_count = cur.fetchone()[0]

        # First user becomes admin
        is_admin = 1 if user_count == 0 else 0
        approved = 1 if user_count == 0 else 0

        try:
            cur.execute("""
            INSERT INTO users (username, password, approved, is_admin)
            VALUES (?, ?, ?, ?)
            """, (username, password, approved, is_admin))
            conn.commit()
        except:
            return "❌ Username already exists"

        return "✅ Signup successful! You are admin." if is_admin else "✅ Signup submitted for approval"


def login(username, password):
    with database.get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
        SELECT approved FROM users
        WHERE username=? AND password=?
        """, (username, password))
        user = cur.fetchone()

        if not user:
            return "❌ Invalid login"
        if user[0] == 0:
            return "❌ Not approved yet"
        return "✅ Login successful"


def is_admin(username):
    with database.get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT is_admin FROM users WHERE username=?", (username,))
        return cur.fetchone()[0] == 1


def get_users():
    with database.get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT username, approved, is_admin FROM users")
        return cur.fetchall()


def approve_user(username):
    with database.get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE users SET approved=1 WHERE username=?", (username,))
        conn.commit()
