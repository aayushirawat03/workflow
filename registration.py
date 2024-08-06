from flask import Flask, request, jsonify, make_response
import jwt
import datetime

app = Flask(__name__)
# to encode and decode JWT tokens 
app.config['SECRET_KEY'] = '381836fe163039ab7bcd0a84bf54dded9fbd4269'

users = {
    "username": "testuser",
    "password": "1234testuser"
}

def generate_token(username):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow(),
        'sub': username
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

@app.route('/register', methods = ['POST'])
def register():
    if not request.is_json:
        return jsonify({'message': 'content type in jason'})
    
    data = request.json
    username = data['username']
    password = data['password']

    if username in users:
        return jsonify({'message': 'user already exists!'})
    else:
        return jsonify({'message': 'successfully registered'})     
    

@app.route('/login', methods= ['POST'])
def login():

    data = request.json
    username =data.get('username')
    password = data.get('password')

    print(username)
    print(users["username"])

    if users["username"] == username and users["password"] == password:
        token = jwt.encode({
             'username': data['username'],
             'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token})
    else:
        return jsonify({'message': "Invalid username or password"})
    

@app.route('/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({'message': 'Logged out successfully'}))
    response.set_cookie('token', '', expires=0)
    return response

if __name__ == '__main__':
     app.run(debug=True)
    


    
#     if not request.is_json:
#         return jsonify({'message': 'content type in jason'})
#     auth = request.json
#     print(auth)
#     if not auth or not auth.get('username') or not auth.get('password'):
#         return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


#     if auth['username'] == users['username'] and auth['password'] == users['password']:
#         token = jwt.encode({
#             'username': auth['username'],
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=180)
#         }, app.config['SECRET_KEY'], algorithm="HS256")

#         return jsonify({'token': token})
    

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

#     return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


