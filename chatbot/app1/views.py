from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.http import JsonResponse
import json
import urllib3
from bs4 import BeautifulSoup
import requests
import pickle
import re

@csrf_exempt


def respond2( texts, project_id = 'omenakuttan-2bb44', session_id = '123', language_code = 'en'):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
	of the conversaion."""
    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/media/jeswin/Lectures and Files/Angelhack/env/omanakuuttan/omenakuttan-2bb44-bb92f0b04461.json'
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    import pickle
    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    headers = ['MA202','CS202','CS204','CS206','CS208','HS200','CS232','CS234']
    att = ['KURIAKOSE ELDHO' , 84.09 , 89.036 , 81.13 , 83.72 , 84.78 , 81.82 , 100.0 , 100.0]

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)


        # print('=' * 20)
        # print(response)
        # print('Query text: {}'.format(response.query_result.query_text))
        # print('Detected intent: {} (confidence: {})\n'.format(
        #     response.query_result.intent.display_name,
        #     response.query_result.intent_detection_confidence))
        # print('Fulfillment text: {}\n'.format(
        #     response.query_result.fulfillment_text))
    #return [format(response.query_result.fulfillment_text) , format(x.query_result.intent.display_name) , response]
    # return response
    text = format(response.query_result.fulfillment_text)

    if(format(response.query_result.intent.display_name) == 'Attendance_HowMuch_Subject'):
        sub = response.query_result.parameters['Subject']
        # with open('att_data.pickle', 'rb') as handle:
        #     att = pickle.load(handle)
            # headers = pickle.load(handle)
        #print(sub , att , headers)
        val = att[headers.index(sub)-1]
        text = text.replace('#' , (str)(val))
    return text



def respond( texts, project_id = 'omenakuttan-2bb44', session_id = '123', language_code = 'en'):
    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/media/jeswin/Lectures and Files/Angelhack/env/omanakuuttan/omenakuttan-2bb44-bb92f0b04461.json'
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)


        print('=' * 20)
        print(response)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))
    return format(response.query_result.fulfillment_text)

def scrape(clas, rollnoo):
    '''url = 'http://attendance.mec.ac.in/view4stud.php?class=' +clas+ '&submit=view'


    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # pattern = re.compile(r'CSU')
    # table = soup.find('table',{"class":"attn"})

    data = []
    row = soup.findAll("tr")[int(rollno) + 1]

    data.append(row.contents[2].contents[0][5:])
    for i in range(3,11):
        data.append((float)(row.contents[i].contents[0]))
    # print(data)
    with open('att_data.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # with open('att_data.pickle', 'rb') as handle:
    #     b = pickle.load(handle)
    return data  '''
    rollno = int(rollnoo)
    url = 'http://attendance.mec.ac.in/view4stud.php?class='+clas+'&submit=view'
    #url = 'http://attendance.mec.ac.in/view4stud.php?class=C4B&submit=view'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    pattern = re.compile(r'CSU')
    table = soup.find('table',{"class":"attn"})

    #for i in range(1,66):
    #    print(tags[i])
    rows=list()
    i=0
    for row in soup.findAll("tr"):
        #print(i)
        rows.append(row)
        i=i+1

    td = rows[rollno].findAll('td')
    #print(td.[0])


@csrf_exempt
def login(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        print(data)
        request.session["class"]=data["class"]
        request.session["rollno"]=data["rollno"]

        #result = scrape(data["class"].upper(),data["rollno"])
    #    print(result)



        return JsonResponse({'success': 'hai'})
    except Exception as e:
        # To be changed during production
        print(e)
        return JsonResponse({'Error': 'Something unexpected happened'}, status=500)

@csrf_exempt
def message(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        print(respond2([data["string"]]))

        #kuriakose api

        #if statement toidentify the problem
        # call the required function

        return JsonResponse({'success': respond2([data["string"]])})
    except Exception as e:
        # To be changed during production
        print(e)
        return JsonResponse({'Error': 'Something unexpected happened'}, status=500)
