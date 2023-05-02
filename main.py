import requests, re
from flask import *



app=Flask(__name__)
app.secret_key="haVaiThikHaiGaandMara"



def isEmail(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    match = re.match(pattern, email)
    if match:
        return True
    else:
        return False



h={"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"}

def chkBreachpCloud(email):
    #pCloud
    api="https://eapi.pcloud.com/checkpwned?checkemail="
    try:
        r=requests.get(api+email, headers=h)
        print(r.json())
        if r.json().get("result")==0:
            data=r.json().get("data")
            return True, data
        if r.json().get("error"):
            return False, r.json().get("error")
        return False, None
    except Exception as e:
        print(e)
        return False, None



@app.route("/")
def apiHome():
    return "<b>OK</b>"


@app.route("/api/breach")
@app.route("/api/breach/")
def breachCheck():
    if request.method!="GET":
        return jsonify(status=False, data=None, message="Please use only GET method.")
    email=None
    if not request.args.get("email", "").strip():
        return jsonify(status=False, data=None, message="Please Specify a Valid Email.")

    if not isEmail(request.args.get("email", "").strip()):
        return jsonify(status=False, data=None, message="Please Specify a Valid Email.")
    email=request.args.get("email").strip()
    status, data=chkBreachpCloud(email)
    if status:
        return jsonify(status=status, data=data, message="Success.")
    return jsonify(status=False, data=None, message="Something Went Wrong.")

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0", threaded=True)
