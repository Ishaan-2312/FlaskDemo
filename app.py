from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Ishaan%4023@localhost/flask_crud_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

class User(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  username=db.Column(db.String(100),nullable=False)
  email=db.Column(db.String(100),nullable=False)

  def to_dict(self):
      return {
          "id": self.id,
          "username": self.username,
          "email": self.email
      }

  def __repr__(self):
      return f'<User {self.username}>'


with app.app_context():
    db.create_all()

@app.route('/saveUser',methods=['POST'])
def saveUser():
    data=request.get_json()
    userName=data.get('username')
    email=data.get('email')

    if not userName or not email:
        return jsonify({"error":"Please provide both username and email"})

    if(User.query.filter_by(email=email).first()):
        return jsonify({"error": "User with this email already exists"})

    user=User(username=userName,email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict())


@app.route('/getUserById',methods=['GET'])
def getUserById():
    user_id = request.args.get('id', type=int)
    print(f"Received user_id: {user_id}")
    if not user_id:
        return jsonify({"error": "Missing 'id' query parameter"}), 400

    user = User.query.get(user_id)

    if user:
        return jsonify(user.to_dict())
    return jsonify({"error": "User not found"}), 404


@app.route('/getAllUsers',methods=['GET'])
def getAllUsers():
    users = User.query.all()
    userList=[user.to_dict() for user in users]
    return jsonify(userList)







if __name__ == '__main__':
    app.run(debug=True)
