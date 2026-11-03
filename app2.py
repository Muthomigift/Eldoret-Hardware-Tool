from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# Sample details: replace the shop name and customers with the real ones.
SHOP_NAME = "Eldoret Hardware"

# Customer names in lowercase, balances in KES.
customers = {
    "wanjiku mwangi": 12500,
    "kiprop kemboi": 0,
    "achieng odhiambo": 3200,
    "kibet rotich": 45800,
    "naliaka wekesa": 7150,
    "jepchirchir koech": 18900,
}

HOME_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ shop_name }} - Customer Balances</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 520px; margin: 40px auto; padding: 0 16px; color: #1c2b3a; }
    h1 { color: #1F4E79; }
    label { display: block; font-weight: bold; margin-bottom: 6px; }
    input { padding: 10px; font-size: 16px; width: 100%; box-sizing: border-box; border: 1px solid #b8c7d9; border-radius: 6px; }
    button { margin-top: 10px; padding: 10px 20px; font-size: 16px; color: #fff; background: #2E75B6; border: 0; border-radius: 6px; cursor: pointer; }
    button:hover { background: #1F4E79; }
    #result { margin-top: 20px; padding: 14px; background: #f4f7fb; border: 1px solid #d0dff0; border-radius: 8px; min-height: 24px; }
  </style>
</head>
<body>
  <h1>{{ shop_name }}</h1>
  <p>Type a customer name to see how much they owe.</p>

  <form id="search" action="/api/balance" method="get">
    <label for="name">Customer name</label>
    <input id="name" name="name" type="text" required autofocus>
    <button type="submit">Check balance</button>
  </form>

  <div id="result" aria-live="polite"></div>

  <script>
    const form = document.getElementById("search");
    const result = document.getElementById("result");

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const name = document.getElementById("name").value;
      result.textContent = "Checking...";

      try {
        const response = await fetch("/api/balance?name=" + encodeURIComponent(name));
        const data = await response.json();

        if (!response.ok) {
          result.textContent = data.error;
          return;
        }

        result.textContent = data.balance_kes === 0
          ? data.name + " owes nothing."
          : data.name + " owes KES " + data.balance_kes.toLocaleString() + ".";
      } catch (error) {
        result.textContent = "Could not reach the server. Check that the app is running.";
      }
    });
  </script>
</body>
</html>"""


@app.route("/")
def home():
    return render_template_string(HOME_PAGE, shop_name=SHOP_NAME)


@app.route("/api/balance")
def balance():
    # Ignore capital letters and extra spaces in the name.
    name = " ".join(request.args.get("name", "").lower().split())

    if not name:
        return jsonify({"error": "Please give a customer name, for example /api/balance?name=wanjiku mwangi"}), 400

    if name not in customers:
        return jsonify({"error": f"Customer '{name}' not found"}), 404

    return jsonify({"name": name.title(), "balance_kes": customers[name]})


if __name__ == "__main__":
    app.run(debug=True)