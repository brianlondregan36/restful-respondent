from respondents import app
from respondents.passwords import *
from flask import Flask, render_template, request
from flask_cors import CORS
import base64, json, requests


@app.route('/', methods=['GET'])
def index():
    access_token = ConfirmitAuthenticate("testlab")
    req = requests.get('https://ws.testlab.firmglobal.net/v1/surveys/p10210620', headers = {"Content-Type": "application/x-www-form-urlencoded", "authorization": access_token})
    desc, result = None, ""
    if req.status_code == 200:
        respText = json.loads(req.text)
        desc = respText["description"]
    if desc is not None:
        result = "Survey Description: " + desc
    return render_template('index.html', result=result)

@app.route('/Response', methods=['POST'])
def CreateSurveyResponse():
    options = request.form['options']
    email = request.form['email']
    if options is not None and email is not None:
        respValues = {"email": email, "options": options}
        access_token = ConfirmitAuthenticate("testlab")
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

@app.route('/Practice/<site>', methods=['GET'])
def practice(site):
    access_token = ConfirmitAuthenticate(site)
    return render_template('practice.html')





def ConfirmitAuthenticate(site):
    grant_scope = {"grant_type": "api-user", "scope": "pub.surveys pub.hubs"}
    if site == "us":  
        authEndpoint = "https://idp.us.confirmit.com/identity/connect/token"
        req = requests.post(authEndpoint, data=grant_scope, auth=(us_clientid, us_clientsecret))
    elif site == "euro":
        authEndpoint = "https://idp.euro.confirmit.com/identity/connect/token"
        req = requests.post(authEndpoint, data=grant_scope, auth=(euro_clientid, euro_clientsecret))
    elif site == "nordic":
        authEndpoint = "https://idp.nordic.confirmit.com/identity/connect/token"
        req = requests.post(authEndpoint, data=grant_scope, auth=(nordic_clientid, nordic_clientsecret))
    elif site == "testlab":
        authEndpoint = "https://idp.testlab.firmglobal.net/identity/connect/token"
        req = requests.post(authEndpoint, data=grant_scope, auth=(testlab_clientid, testlab_clientsecret))
    
    if req.status_code == 200:
        respText = json.loads(req.text)
        access_token = respText["token_type"] + " " + respText["access_token"]
        print(str(access_token))
        return access_token
    else:
        print(str(req.status_code))
        print(str(requests.exceptions.RequestException))
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

