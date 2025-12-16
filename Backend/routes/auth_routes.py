from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from flask_jwt_extended import create_access_token


auth_bp = Blueprint("auth", __name__)


# ---------- REGISTER ----------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "User already exists"}), 400

    user = User(
        name=data["name"],
        email=data["email"],
        role=data.get("role", "user")  
    )
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# ---------- LOGIN ----------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    # ✅ FIX: identity is a DICTIONARY
    access_token = create_access_token(
        identity={
            "id": str(user.id),
            "role": str(user.role)
        }
    )

    return jsonify({
        "access_token": access_token,
        "role": user.role
    })




# from flask import Blueprint, request, jsonify
# from extensions import db
# from models.user import User
# from flask_jwt_extended import create_access_token
# from schemas.user_schema import UserRegisterSchema
# from marshmallow import ValidationError
# from schemas.login_schema import LoginSchema

# auth_bp = Blueprint('auth', __name__)

# @auth_bp.route('/register', methods=['POST'])
# def register():
#     data = request.json

#     schema = UserRegisterSchema()
#     try:
#         validated_data = schema.load(data)
#     except ValidationError as err:
#         return {"errors": err.messages}, 400

#     name = validated_data["name"]
#     email = validated_data["email"]
#     password = validated_data["password"]
#     role = validated_data.get("role", "user")

#     if User.query.filter_by(email=email).first():
#         return jsonify({'message': 'User already exists'}), 400

#     new_user = User(name=name, email=email, role=role)
#     new_user.set_password(password)

#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({'message': 'User registered successfully'}), 201

# @auth_bp.route('/login', methods=['POST'])
# def login():
#     data = request.json

#     schema = LoginSchema()
#     try:
#         validated_data = schema.load(data)
#     except ValidationError as err:
#         return {"errors": err.messages}, 400

#     email = validated_data["email"]
#     password = validated_data["password"]

#     user = User.query.filter_by(email=email).first()

#     if not user or not user.check_password(password):
#         return jsonify({'message': 'Invalid credentials'}), 401

#     token = create_access_token(
#         identity=str(user.id),
#         additional_claims={
#             "role": user.role,
#             "email": user.email
#         }
#     )

#     return jsonify({
#         'access_token': token,
#         'role': user.role
#     }), 200










# # from flask import Blueprint, request, jsonify
# # from extensions import db
# # from models.user import User
# # from flask_jwt_extended import create_access_token
# # from schemas.user_schema import UserRegisterSchema
# # from marshmallow import ValidationError
# # from schemas.login_schema import LoginSchema
# # from marshmallow import ValidationError

# # auth_bp=Blueprint('auth',__name__)

# # @auth_bp.route('/register',methods=['POST'])
# # def register():
# #     data=request.json

# #     schema = UserRegisterSchema()
# #     try:
# #         validated_data = schema.load(data)
# #     except ValidationError as err:
# #         return {"errors": err.messages}, 400

# #     name = validated_data["name"]
# #     email = validated_data["email"]
# #     password = validated_data["password"]

# #     if User.query.filter_by(email=email).first():
# #         return jsonify({'message':'User already exists'}),400

# #     new_user=User(name=name,email=email)
# #     new_user.set_password(password)

# #     db.session.add(new_user)
# #     db.session.commit()

# #     return jsonify({'message':'User registered successfully'}),201

# # @auth_bp.route('login',methods=['POST'])
# # def login():
# #     data=request.json

# #     schema = LoginSchema()
# #     try:
# #         validated_data = schema.load(data)
# #     except ValidationError as err:
# #         return {"errors": err.messages}, 400

# #     email = validated_data["email"]
# #     password = validated_data["password"]
    
# #     user=User.query.filter_by(email=email).first()

# #     if not user or not user.check_password(password):
# #         return jsonify({'message':'Invalid credentials'}),401

# #     token=create_access_token(identity={'id':user.id,'email':user.email,'role':user.role})

# #     return jsonify({'access_token':token,"role":user.role}),200