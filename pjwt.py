from flask import Flask, request, jsonify, make_response
import jwt
import datetime


app = Flask(__name__)

# Secret key to encode and decode the JWT tokens
app.config['SECRET_KEY'] = '381836fe163039ab7bcd0a84bf54dded9fbd4269'

# Dummy user data for demonstration
USER_DATA = {
    "username": "testuser",
    "password": "1234testuser"
}

# Route for generating JWT token
@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    username = auth.get('username')
    password = auth.get('password')

    if not username in USER_DATA and USER_DATA[username] ==password:
        token = jwt.encode({
             'username': auth['username'],
             'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=180)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token})
    else:
        return jsonify({'message': "Invalid username or password"})
    
@app.route('/protected', methods =["GET"])
def protected():
    token = request.headers.get("Token is provided")
    if not token:
        return jsonify({"message": "Token is missing"})
    
    try:
         data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    except:
         return jsonify({'message': 'Token is invalid!'}), 403

    return jsonify({'message': 'Token is valid', 'USER_DATA': data['username']})

if __name__ == '__main__':
     app.run(debug=True)














#     print(auth)
#     if not auth or not auth.get('username') or not auth.get('password'):
#         return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

#     if auth['username'] == USER_DATA['username'] and auth['password'] == USER_DATA['password']:
#         token = jwt.encode({
#             'username': auth['username'],
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=180)
#         }, app.config['SECRET_KEY'], algorithm="HS256")

#         return jsonify({'token': token})

#     return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

# # Route for accessing protected content
# @app.route('/protected', methods=['GET'])
# def protected():
#     token = request.headers.get('x-access-tokens')

#     if not token:
#         return jsonify({'message': 'Token is missing!'}), 403

#     try:
#         data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
#     except:
#         return jsonify({'message': 'Token is invalid!'}), 403

#     return jsonify({'message': 'Token is valid', 'user': data['username']})

# if __name__ == '__main__':
#     app.run(debug=True)