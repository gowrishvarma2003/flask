from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:nkpacmfb8m@localhost:5432/learn'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    

@app.route("/signup",methods=["POST"])
def signup():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    temp = User(username=username, email=email, password=password)
    db.session.add(temp)
    db.session.commit()
    return Response.jsonify({"message":"User created successfully"}), 201

@app.route("/login",methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        return jsonify({"message":"Login successful"}), 200
    else:
        return jsonify({"message":"Invalid credentials"}), 401
    
@app.route("/users",methods=["GET"])
def users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "password": user.password
        })
    return jsonify(user_list), 200

@app.route("/updatepassword",methods=["POST"])
def updatepassword():
    email = request.form.get("email")
    password = request.form.get("password")
    new_password = request.form.get("new_password")
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        user.password = new_password
        db.session.commit()
        return jsonify({"message":"Password updated successfully"}), 200
    else:
        return jsonify({"message":"User not found"}), 404

@app.route("/deleteuser",methods=["POST"])
def deleteuser():
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message":"User deleted successfully"}), 200
    return jsonify({"message":"User not found"}), 404

@app.route("/", methods=["GET"])
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test",methods=["GET"])
def test():
    return "<p>Test</p>"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)


# To run the application, use the command: python test.py

def test_signup(client):
    return "User created successfully", 201