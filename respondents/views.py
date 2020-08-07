from respondents import app
from respondents.passwords import *
from flask import Flask, render_template, request
from flask_cors import CORS
import base64, json, requests




'''ROUTING''' 
@app.route('/practice', methods=['GET'])
def Practice():
    return render_template('practice.html', result=["",""])

@app.route('/practice/<site>', methods=['GET'])
def PracticeWithActions(site):
    access_token = ConfirmitAuthenticate(site)
    if access_token == None:
        return render_template('practice.html', result=["Authentication Token", "NON-200: ERROR"])
    root = "https://ws." + site + ".confirmit.com" if site == "us" or site == "euro" or site == "nordic" else "https://ws.testlab.firmglobal.net"
    path = "/v1/surveys"
    endpoint = root + path
    req = requests.get(endpoint, headers = {"Content-Type": "application/x-www-form-urlencoded", "authorization": access_token})
    requestDesc = "GET " + endpoint + " using access token " + access_token
    responseDesc = str(req.status_code) + ": " + str(req.text)
    return render_template('practice.html', result=[requestDesc, responseDesc])

@app.route('/demo', methods=['GET'])
def Index():
    access_token = ConfirmitAuthenticate("us")
    req = requests.get('https://ws.us.confirmit.com/v1/surveys/p191045119335', headers = {"Content-Type": "application/x-www-form-urlencoded", "authorization": access_token})
    desc, result = None, ""
    if req.status_code == 200:
        respText = json.loads(req.text)
        desc = respText["description"]
    if desc is not None:
        result = "Survey Description: " + desc
    return render_template('index.html', result=result)

@app.route('/response', methods=['POST'])
def CreateSurveyResponse():
    options = request.form['options']
    email = request.form['email']
    if options is not None and email is not None:
        respValues = {"email": email, "options": options}
        access_token = ConfirmitAuthenticate("testlab")
        req = requests.post('https://ws.us.confirmit.com/v1/surveys/p191045119335/respondents',
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
            return None
    else:
        #client-side error
        return None





'''REUSABLE FUNCTIONS'''

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
