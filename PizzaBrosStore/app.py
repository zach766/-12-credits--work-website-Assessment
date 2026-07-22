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