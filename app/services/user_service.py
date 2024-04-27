from app import app,db
from app.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify
from flask_jwt_extended import create_access_token

def get_all_users():
    users=User.query.all()
    user_list=[{"id":user.id, "username":user.username, "role":user.role, "isActive":user.is_active,"email":user.email} for user in users]
    return jsonify(user_list),200

def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return None
    return {'id': user.id, 'username': user.username, "role": user.role, "isActive":user.is_active,"email":user.email}

def create_user(username, password, email):
    try:
        # Check if the user already exists
        if User.query.filter_by(username=username).first() is not None:
            return {"message": "User already exists"}, 409

        # Create a new user instance
        new_user = User(username=username)
        new_user.set_password(password)  # Hash the password and store
        new_user.email=email

        # Add the new user to the session and commit it to the database
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully"}, 201

    except SQLAlchemyError as e:
        # Log the error - you might want to configure proper logging
        print(f"Database error occurred: {e}")

        # Rollback in case of error
        db.session.rollback()
        
        return {"message": "An error occurred while creating the user"}, 500

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id,additional_claims={"role": user.role})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401
    
def update_user(user_id,user_data):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Check for 'username' in the data to update and update if present
    username = user_data.get('username')
    if username:
        user.username = username

    # Check for 'role' in the data to update and update if present
    role = user_data.get('role')
    if role:
        user.role = role

     # Attempt to commit changes to the database
    try:
        db.session.commit()
        return {'message': 'User updated successfully', 'id': user.id, 'username': user.username, 'role': user.role,'password':user.password_hash}, 200
    except Exception as e:
        db.session.rollback()  # Roll back the transaction on error
        return {'message': f'An error occurred: {str(e)}'}, 500    
    
def delete_user(user_id):
    user = User.query.get(user_id)  # Get the user again for deletion
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted successfully"}), 200    