from flask import Flask, jsonify, request

app = Flask(__name__)

inventory = {
    "maize flour":{"price": 2800, "stock": 120},
    "rice":       {"price": 4500, "stock": 200},
    "cooking oil":{"price": 1800, "stock": 45}
}

@app.route("/")
def home():
    return "Kamau stores API is running."

@app.route("/products")
def products():
    return "Maize flour, Wheat flour, rice, cooking oil"

@app.route("/products/<name>")
def product_detail(name):
    return f"You asked about: {name}"

@app.route("/api/products")
def get_products():
    return jsonify(inventory)

@app.route("/api/products/<product_name>")
def get_product(product_name):
    if product_name in inventory:
        data = inventory[product_name]
        data["name"] = product_name
        return jsonify(data)
    return jsonify({"error": f"Product '{product_name}' not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)    