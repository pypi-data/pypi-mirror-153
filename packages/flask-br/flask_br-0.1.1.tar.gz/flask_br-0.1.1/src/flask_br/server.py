from flask import Flask, request, jsonify
from flask.templating import render_template

price = []

def init(app: Flask):

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