from flask import Flask, render_template, request
from flask_cors import CORS
import base64, json, requests

app = Flask(__name__)
CORS(app)

#set FLASK_APP=flask_basic
#set FLASK_ENV=development
#set FLASK_DEBUG=1

# TODO get this running in Ubuntu, Heroku and on Git

@app.route('/', methods=['GET'])
def index():
    
    access_token = ConfirmitAuthenticate()
    req = requests.get('http://ws.testlab.firmglobal.net/v1/surveys/p10210620', headers = {"Content-Type": "application/x-www-form-urlencoded", "authorization": access_token})
    if req.status_code == 200:
        respText = json.loads(req.text)
        desc = respText["description"]

    result = ""
    if desc is not None:
        result = "Survey Description: " + desc
    
    return render_template('index.html', result=result)
    

@app.route('/Response', methods=['POST'])
def CreateSurveyResponse():
    
    options = request.form['options']
    email = request.form['email']
    
    if options is not None and email is not None: 
        respValues = {"email": email, "options": options}
        access_token = ConfirmitAuthenticate()
        req = requests.post('http://ws.testlab.firmglobal.net/v1/surveys/p10210620/respondents', 
                         data = json.dumps(respValues), 
                         headers = {"Content-Type": "application/json", "Accept": "application/json", "authorization": access_token}
                         )
        if req.status_code == 201:
            respText = json.loads(req.text)
            links = respText["links"]
            nextUrl = links["self"]
            surveyLink = GetRespondentLink(nextUrl, access_token)
            result = {"surveyLink": surveyLink} 
            return json.dumps(result)
        else:
            #server-side error
            return None
    else: 
        #client-side error
        return None

    
def ConfirmitAuthenticate(): 
    basic_token = "Basic %s" % base64.b64encode(b"f60355de-1a7b-4e77-887a-fc53a3c10644:b182d8ea-a9b4-457e-ab72-590294057d9e").decode("ascii")
    grant_scope = {"grant_type": "api-user", "scope": "pub.surveys"}
    req = requests.post('http://author.testlab.firmglobal.net/identity/connect/token', 
                         data = grant_scope, 
                         headers = {"Content-Type": "application/x-www-form-urlencoded", "withCredentials": "true", "Authorization": basic_token}
                         )
    if req.status_code == 200:
        respText = json.loads(req.text)
        access_token = respText["token_type"] + " " + respText["access_token"]
        return access_token
    else: 
        #server-side error
        return None
    
    
def GetRespondentLink(url, token): 
    url = url + "?includeSurveyLink=true"
    req = requests.get(url, headers = {"Content-Type": "application/x-www-form-urlencoded", "authorization": token})
    if req.status_code == 200:
        respText = json.loads(req.text)
        links = respText["links"]
        surveyLink = links["surveyLink"] 
        return surveyLink
    else:
        #server-side error
        return None
    