from flask import Flask, render_template, redirect, url_for, request
import json
import os
from datetime import datetime
import random


app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PRODUCT_FILE = os.path.join(
    BASE_DIR,
    "products.json"
)


cart = []


def load_products():

    try:

        with open(PRODUCT_FILE, "r") as file:
            return json.load(file)

    except FileNotFoundError:

        print("products.json not found")
        return []


def save_products(products):

    with open(PRODUCT_FILE, "w") as file:

        json.dump(
            products,
            file,
            indent=4
        )


def calculate_total(items):

    total = 0

    for item in items:

        total += item["price"] * item["quantity"]

    return total


@app.route("/")
def home():

    products = load_products()

    return render_template(
        "index.html",
        products=products
    )


@app.route("/products")
def products_page():

    products = load_products()

    return render_template(
        "products.html",
        products=products
    )


@app.route("/add/<int:product_id>")
def add_to_cart(product_id):

    products = load_products()

    for product in products:

        if product["id"] == product_id:

            if product["stock"] > 0:

                found = False

                for item in cart:

                    if item["id"] == product_id:

                        item["quantity"] += 1
                        found = True
                        break

                if not found:

                    new_item = product.copy()
                    new_item["quantity"] = 1
                    cart.append(new_item)

                product["stock"] -= 1

                save_products(products)

            break

    return redirect(
        url_for("view_cart")
    )


# =========================================
# INCREASE / DECREASE QUANTITY
# =========================================

@app.route("/update/<int:product_id>/<action>")
def update_quantity(product_id, action):

    products = load_products()

    for item in cart:

        if item["id"] == product_id:

            # Increase quantity
            if action == "increase":

                for product in products:

                    if product["id"] == product_id:

                        if product["stock"] > 0:

                            item["quantity"] += 1
                            product["stock"] -= 1

                            save_products(products)

                        break

            # Decrease quantity
            elif action == "decrease":

                if item["quantity"] > 1:

                    item["quantity"] -= 1

                    for product in products:

                        if product["id"] == product_id:

                            product["stock"] += 1
                            break

                    save_products(products)

                else:

                    for product in products:

                        if product["id"] == product_id:

                            product["stock"] += 1
                            break

                    save_products(products)

                    cart.remove(item)

            break

    return redirect(
        url_for("view_cart")
    )


@app.route("/cart")
def view_cart():

    total = calculate_total(cart)

    return render_template(
        "cart.html",
        cart=cart,
        total=total
    )


@app.route("/remove/<int:index>")
def remove_from_cart(index):

    if index < len(cart):

        removed_item = cart[index]

        products = load_products()

        for product in products:

            if product["id"] == removed_item["id"]:

                product["stock"] += removed_item["quantity"]
                break

        save_products(products)

        cart.pop(index)

    return redirect(
        url_for("view_cart")
    )


@app.route("/cancel")
def cancel_order():

    products = load_products()

    for cart_item in cart:

        for product in products:

            if product["id"] == cart_item["id"]:

                product["stock"] += cart_item["quantity"]
                break

    save_products(products)

    cart.clear()

    return redirect(
        url_for("products_page")
    )


# =========================================
# CHECKOUT
# =========================================

@app.route("/checkout", methods=["GET", "POST"])
def checkout():

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]

        order_type = request.form["order_type"]

        address = request.form.get("address", "")

        subtotal = calculate_total(cart)

        delivery_fee = 0

        if order_type == "delivery":

            delivery_fee = 3

        total = subtotal + delivery_fee

        order_id = random.randint(1000, 9999)

        date = datetime.now().strftime("%d %B %Y")

        return render_template(
            "invoice.html",
            name=name,
            phone=phone,
            address=address,
            order_type=order_type,
            cart=cart,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total=total,
            order_id=order_id,
            date=date
        )

    subtotal = calculate_total(cart)

    return render_template(
        "checkout.html",
        cart=cart,
        subtotal=subtotal
    )


if __name__ == "__main__":
    app.run(debug=True)