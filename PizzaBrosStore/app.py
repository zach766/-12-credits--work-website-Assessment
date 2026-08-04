from flask import Flask, render_template, redirect, url_for, request
import json
import os


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


            # Check stock

            if product["stock"] > 0:


                found = False


                # If already in cart increase quantity

                for item in cart:

                    if item["id"] == product_id:

                        item["quantity"] += 1

                        found = True

                        break



                # If new item add quantity

                if not found:

                    new_item = product.copy()

                    new_item["quantity"] = 1

                    cart.append(new_item)



                # decrease stock

                product["stock"] -= 1


                save_products(products)



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


                # return all quantity back to stock

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


    # Return stock when cancelling

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





@app.route("/checkout", methods=["GET","POST"])
def checkout():

    if request.method == "POST":


        name = request.form["name"]

        email = request.form["email"]


        total = calculate_total(cart)



        return render_template(
            "invoice.html",
            name=name,
            email=email,
            cart=cart,
            total=total
        )



    return render_template(
        "checkout.html"
    )





if __name__ == "__main__":
    app.run(debug=True)