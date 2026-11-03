# Eldoret Hardware: Customer Balance Tool

A small Flask web app for a hardware shop in Eldoret that sells on credit. Instead of paging through a notebook, the owner types a customer's name and sees how much they owe.

**Price:** I would charge KES 15,000 one time for this version, which includes setting it up on the shop's computer, entering the real customers and balances, and a short training session.

## What it does

- **Home page (`/`):** shows the shop name and a search box. Type a customer name, click **Check balance**, and the result appears on the page, for example "Wanjiku Mwangi owes KES 12,500."
- **Balance API (`/api/balance`):** takes a customer name as the query parameter `name` and returns the balance as JSON.

Names are matched without regard to capital letters or extra spaces, so `KIBET   rotich` finds Kibet Rotich.

## The two routes

| Route | Method | What it returns |
|---|---|---|
| `/` | GET | An HTML page with the shop name and the search form |
| `/api/balance?name=<customer name>` | GET | The customer's balance as JSON |

### API responses

| Request | Status | Response |
|---|---|---|
| `/api/balance?name=Wanjiku Mwangi` | 200 | `{"balance_kes":12500,"name":"Wanjiku Mwangi"}` |
| `/api/balance?name=John Doe` | 404 | `{"error":"Customer 'john doe' not found"}` |
| `/api/balance` (no name) | 400 | `{"error":"Please give a customer name, for example /api/balance?name=wanjiku mwangi"}` |

A customer with a balance of 0 returns `{"balance_kes":0,...}`, and the page shows "owes nothing".

## Sample customers

The customers are hardcoded in a Python dictionary called `customers` inside `app2.py`. These are sample names and balances in Kenya shillings:

| Customer | Balance (KES) |
|---|---|
| Wanjiku Mwangi | 12,500 |
| Kiprop Kemboi | 0 |
| Achieng Odhiambo | 3,200 |
| Kibet Rotich | 45,800 |
| Naliaka Wekesa | 7,150 |
| Jepchirchir Koech | 18,900 |

## How it works

1. `home()` returns the page using `render_template_string`, and fills in the shop name from `SHOP_NAME`.
2. When you submit the form, a small script on the page calls `/api/balance` with the name, then shows the answer or the error message. If JavaScript is off, the form sends you straight to the API address.
3. `balance()` reads the `name` parameter, turns it into lowercase with single spaces, and looks it up in `customers`.
4. It returns the name and balance as JSON with `jsonify`, or an error message with status 404 (not found) or 400 (no name given).

## Setup

1. Install Python 3.9 or newer.
2. Install Flask:
   ```
   pip install -r requirements.txt
   ```

## Run it

Open a terminal in the project folder and run:

```
python app2.py
```

The terminal prints `Running on http://127.0.0.1:5000` and stays open while the app runs. Press Ctrl+C to stop it.

## Test it in your browser

Use `http`, not `https`, in the address bar.

| Open | What you should see |
|---|---|
| `http://127.0.0.1:5000/` | The shop name and a search box |
| Type `Wanjiku Mwangi` and click Check balance | Wanjiku Mwangi owes KES 12,500. |
| Type `kiprop kemboi` | Kiprop Kemboi owes nothing. |
| Type `John Doe` | Customer 'john doe' not found |
| `http://127.0.0.1:5000/api/balance?name=kibet rotich` | `{"balance_kes":45800,"name":"Kibet Rotich"}` |
| `http://127.0.0.1:5000/api/balance` | The 400 error message |

If port 5000 is already in use, change the last line of `app2.py` to `app.run(debug=True, port=5001)` and use `5001` in the addresses.

## Limits

- **There is no login.** Anyone who can open the app can see every balance. Use it on one computer, and do not put it on the internet as it is.
- **Balances live in the code.** To change a balance, someone has to edit `customers` in `app2.py` and restart the app. A database and a page for updating balances would be the next version.
- **The shop name and customers are samples.** Replace `SHOP_NAME` and `customers` with the real ones.
- `debug=True` is for learning and testing only.