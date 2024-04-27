from flask import Blueprint, request, jsonify
from app.services.user_service import create_user, login_user,get_all_users,update_user,get_user_by_id,delete_user
from flask_jwt_extended import jwt_required, get_jwt,get_jwt_identity

bp = Blueprint('user', __name__, url_prefix='/users')


@bp.route('/', defaults={'user_id': None},methods=['GET'])
@bp.route('/<int:user_id>',methods=['GET'])
@jwt_required()  # Requires a valid access token in the request
def get_users_route(user_id):
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"msg": "Access is restricted to administrators only."}), 403

    if user_id is None:
        return get_all_users()  # Assuming this returns a proper JSON response

    user_data = get_user_by_id(user_id)
    if user_data is None:
        return jsonify({"msg": "User not found"}), 404

    return jsonify(user_data), 200
    
@bp.route('/create_user', methods=['POST'])
def create_user_route():    
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Ensure password is a string
    password = str(password)

    response, status_code = create_user(username, password, email)
    return jsonify(response), status_code

@bp.route('/login', methods=['POST'])
def login_user_route():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400
    
    password = str(password)

    return login_user(username, password)

@bp.route("/<int:user_id>",methods=["PUT"])
@jwt_required()
def update_user_route(user_id):    
    try:
        user_id = int(user_id)  # Convert URL param to integer
    except ValueError:
        return jsonify({"msg": "Invalid user ID format"}), 400
    # Get the identity and additional claims from the JWT
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    user_role = claims.get('role', '')
    # Check if the current user is the target user or if they are an admin
    if current_user_id != user_id and user_role != 'admin':
        return jsonify({'msg': 'Access denied'}), 403

    user_data = request.get_json()
    result = update_user(user_id, user_data)
    return jsonify(result)

@bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user_route(user_id):
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    user_role = claims.get('role', '')

    # Use the refactored function to get user data
    user_data = get_user_by_id(user_id)
    if user_data is None:
        return jsonify({"msg": "User not found"}), 404

    # Check if the current user is allowed to delete this user
    if current_user_id != user_id and user_role != 'admin':
        return jsonify({"msg": "Access denied"}), 403

    return delete_user(user_id)    