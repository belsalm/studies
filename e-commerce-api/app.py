from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

# Modelagem
# Produto (id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
@app.route('/products/add', methods=["POST"])
def add_products():
    data = request.json
    if 'name' in data and 'price' in data: 
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added successfully!"})
    return jsonify({"message": "Invalid product data"}), 400

@app.route('/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product != None:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully!"})
    return jsonify({"message": "Product not found"}), 404


@app.route('/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
    return jsonify({"message": "Product not found"}), 404 


@app.route("/products/update/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    data = request.json
    if 'name' in data:
        product.name = data['name']
        
    if 'price' in data:
        product.price = data['price']
    
    if 'description' in data: 
        product.description = data['description']
        
    db.session.commit()
    return jsonify({"message": "Product updated successfully"})


@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price
        }
        product_list.append(product_data)
    
    return jsonify(product_list)

# Definir uma rota raiz (Página inicial) e a função que será executada ao  requisitar
@app.route('/test', methods=["GET"]) 
def hello_world():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True)