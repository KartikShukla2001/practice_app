from flask import Flask,request,jsonify,Response,json,session
from functools import wraps
from models.users import User  
from config import db
from passlib.hash import pbkdf2_sha256


app = Flask(__name__)
app.secret_key = '\x90N\xdc\x1a\xc9`M\xaf:u\xf8\xa9ax\x92s'

def login_required(f):
    @wraps(f)
    def wrap(*arg, **kwarg):
        if 'logged_in' in session:
            return f(*arg,**kwarg)
        else:
            return 'message'

    return wrap
    

#login/getuser
@app.route('/user/lguser', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        return User().login()
    if request.method == 'GET':
        return User().getuser()


#signup
@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()
       
#uodate/delete/signout
@app.route('/user/udsuser/<id>',methods=['PUT','DELETE','GET'])
def udsuser(id):
    if request.method == 'GET':
        db.users.update_one({"_id":id},{"$set":{"logged":False}})
        session.clear()
        return 'User is logged out'

    if request.method == 'PUT':
        user = db.users.find_one({"_id":id})
        if user['logged']==True:
            db.users.update_one(
            {"_id":id},
            {"$set":{"name":request.form.get('name'),"email":request.form.get('email'),"password":pbkdf2_sha256.encrypt(request.form.get('password'))}}
            )

            return Response(
            response = json.dumps(
                {"message":"user updated"}
            ),
            status=200,
            mimetype="application/json"
            )
        else:
            return jsonify({"error":"Unable to update since user is logged out"})
    
    if request.method == 'DELETE':
        user= db.users.find_one({"_id":id})
        if user['logged']==True:
            db.users.delete_one({"_id":id})
            session.clear()
   
            return Response(
            response=json.dumps(
            {"message":"user deleted","id":f"{id}"}
            )
             )
        return Response(
        response=json.dumps(
            {"message":"user not deleted"}
        ),
        status=200,
        mimetype="application/json"
        )

    
if __name__ == '__main__':
    app.run(debug=True)




