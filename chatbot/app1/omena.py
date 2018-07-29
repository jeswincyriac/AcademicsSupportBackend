

def response( texts, project_id = 'omenakuttan-2bb44', session_id = '123', language_code = 'en'):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
	of the conversaion."""
    import pickle
    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    headers = ['MA202','CS202','CS204','CS206','CS208','HS200','CS232','CS234']

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
        with open('att_data.pickle', 'rb') as handle:
            att = pickle.load(handle)
            # headers = pickle.load(handle)
        #print(sub , att , headers)
        val = att[headers.index(sub)-1]
        text = text.replace('#' , (str)(val))
    return text
			

		
