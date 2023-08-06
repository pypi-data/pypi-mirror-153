from flask import Flask, request, jsonify
from flask.templating import render_template
from pathlib import Path

price = []

def init(app: Flask):
  app.template_folder = Path(__file__).parent.absolute()

  print("Template >>>" + Path(__file__).parent.absolute())

  @app.route('/price', methods=['POST'])
  def set_price():
      global price
      print(request.json)
      price.append(request.json['price'])
      return jsonify(price)

  @app.route('/price', methods=['GET'])
  def price_form():
      return render_template('index.html')

def clear():
  global price
  price = []