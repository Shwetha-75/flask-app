from flask import Flask,make_response,jsonify,request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import base64
import json

load_dotenv()

app=Flask(__name__)

domains=[
    "http://localhost:5173",
     "http://localhost:5174",
     "http://192.168.1.3:5173",
     os.getenv('FRONTEND_URL')
]

cookie_domain=None

CORS( 
      app,
      supports_credentials=True,
      resources={r"/*": {"origins": domains}},
      allow_headers=["Content-Type", "Authorization"],
      methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=='POST':
        data=dict(request.form)
        print(data)
        response=make_response(jsonify({'status':'Logged In Successfully!!'}))
        payload={
            'username':data['username'],
             'session_id':os.getenv('SECRET_KEY')
        }
        secret_value=base64.urlsafe_b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8')
        
        response.set_cookie(
            'cookie',
            secret_value,
            max_age=3600,
            httponly=True,
            samesite='Lax',
            secure=False,
            domain=cookie_domain
        )
        return response
    return jsonify({"status":"Invalid"})
@app.route("/logout",methods=['POST','GET'])
def logout():
    response=make_response(jsonify({'message':'Logged out Successfully !!'}))
    response.set_cookie('cookie','',expires=0)
    return response

@app.route("/protected",methods=['POST','GET'])
def protected():
    session_token=request.cookies.get('cookie')
    if session_token:
        decoded_payload_bytes=base64.urlsafe_b64decode(session_token)
        decoded_payload_data=json.loads(decoded_payload_bytes.decode('utf-8'))
        username=decoded_payload_data.get('username')
        session_id=decoded_payload_data.get('session_id')
        if session_id==os.getenv('SECRET_KEY'):
            return jsonify({
                'message':f'Welcome {username} Good to see you',
                 'status':'true',      
            })
    return jsonify({
        'message':'Invalid !!',
        'status':'false'
    })
if __name__=='__main__':
    app.run(port=5000,debug=True,host='0.0.0.0')
    