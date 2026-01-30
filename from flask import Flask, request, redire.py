from flask import Flask, request, redirect, render_template_string, session

app = Flask(__name__)
app.secret_key = "supermarket_secret_key"

# -----------------------------
# Product Data
# -----------------------------
products = {
    1: {"name": "Milk", "price": 2.5, "stock": 20},
    2: {"name": "Bread", "price": 1.5, "stock": 30},
    3: {"name": "Eggs", "price": 3.0, "stock": 15},
    4: {"name": "Rice", "price": 10.0, "stock": 10},
}

# -----------------------------
# HTML Template
# -----------------------------
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Online Supermarket</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        table { border-collapse: collapse; width: 60%; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
        th { background: #f2f2f2; }
        button { padding: 6px 12px; }
    </style>
</head>
<body>

<h1>🛒 Online Supermarket</h1>

<table>
<tr>
    <th>ID</th><th>Name</th><th>Price</th><th>Stock</th><th>Buy</th>
</tr>

{% for pid, p in products.items() %}
<tr>
    <td>{{ pid }}</td>
    <td>{{ p.name }}</td>
    <td>${{ p.price }}</td>
    <td>{{ p.stock }}</td>
    <td>
        <form method="post" action="/buy">
            <input type="hidden" name="pid" value="{{ pid }}">
            <input type="number" name="qty" min="1" max="{{ p.stock }}" required>
            <button type="submit">Buy</button>
        </form>
    </td>
</tr>
{% endfor %}
</table>

<h2>💵 Total Bill: ${{ total }}</h2>

</body>
</html>
"""

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    if "total" not in session:
        session["total"] = 0
    return render_template_string(HTML, products=products, total=session["total"])


@app.route("/buy", methods=["POST"])
def buy():
    pid = int(request.form["pid"])
    qty = int(request.form["qty"])

    if pid in products and 0 < qty <= products[pid]["stock"]:
        products[pid]["stock"] -= qty
        session["total"] += products[pid]["price"] * qty

    return redirect("/")


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
