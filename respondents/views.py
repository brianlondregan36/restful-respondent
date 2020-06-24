from respondents import app
from respondents.passwords import clientid, clientsecret
from flask import Flask, render_template, request
from flask_cors import CORS
import base64, json, requests


@app.route('/', methods=['GET'])
def index():
    access_token = ConfirmitAuthenticate()
    req = requests.get('https://ws.testlab.firmglobal.net/v1/surveys/p10210620', headers = {"Content-Type": "application/x-www-form-urlencoded", "authorization": access_token})
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
        req = requests.post('https://ws.testlab.firmglobal.net/v1/surveys/p10210620/respondents',
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
            return requests.exceptions.RequestException
    else:
        #client-side error
        return None

@app.route('/Practice', methods=['GET'])
def practice(): 
    access_token = ConfirmitAuthenticate()
    return render_template('practice.html')




def ConfirmitAuthenticate():
    endpoint = "https://author.testlab.firmglobal.net/identity/connect/token"
    grant_scope = {"grant_type": "api-user", "scope": "pub.surveys pub.hubs"}
    req = requests.post(endpoint, data=grant_scope, auth=(clientid, clientsecret))
    if req.status_code == 200:
        respText = json.loads(req.text)
        access_token = respText["token_type"] + " " + respText["access_token"]
        return access_token
    else:
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
        return None
