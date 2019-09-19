# Python REST API demo

[Try it out here](https://restful-respondent.herokuapp.com/)

"views.py" under the "respondents" folder has the API calls. 
The page markup is under "templates" folder and javascript is under "static" folder. 

### 6/13/19 --- 

So far the demo only uses the Surveys API...

1. authentication 
2. on page load flash survey's description onto the page. Using GET/{surveyId}
3. user fills out a form to create a respondent. Adding the record via POST /{surveyId}/respondents
4. flash that new respondent's survey link onto the page. Using GET /{surveyId}/respondents/{respId} 
