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
