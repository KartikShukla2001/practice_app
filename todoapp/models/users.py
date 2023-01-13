from flask import request,jsonify,Response,session,json
from config import db
from passlib.hash import pbkdf2_sha256
import uuid

class User:

    def start_session(self, user):
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200       

    def signup(self):
        if 'logged_in' in session:
            return jsonify({"error": "User is logged in"})
        else:
            print(request.form)

        user= {
            "_id": uuid.uuid4().hex,
            "name":request.form.get('name'),
            "email":request.form.get('email'),
            "password":pbkdf2_sha256.encrypt(request.form.get('password')),
            "logged":True
        }


        if db.users.find_one({"email":user['email']}):
            return jsonify({"error":"Email address already in use"}), 400  

        if db.users.insert_one(user):
            return self.start_session(user)
           
        return jsonify({"error": "Unable to signup"}), 400
        
    
    def getuser(self):
        print(request.form)
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(
            response = json.dumps(data),
            status=500,
            mimetype="application/json"
        )


    def login(self):
        if 'logged_in' in session:
            return jsonify({"error": "User is already logged in"}),401
        else:
            user = db.users.find_one({
            "email" : request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'),user['password']):
            db.users.update_one({"email":user['email']},{"$set":{"logged":True}})
            return self.start_session(user)

            
        return jsonify({"error": "Invald login credentials"}), 401

        
    
    
       

        
