from __future__ import print_function
import paramiko
import unicodedata
import connection as Connection

ssh_host = Connection.ssh_host
ssh_user = Connection.ssh_user
ssh_pass = Connection.ssh_pass

server_1 = '10.0.210.75'
server_2 = '10.0.210.76'

cimc_admin_user = 'admin'
cimc_admin_pass = 'password'

def make_simple_cimc_call(cimc_cmd):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ssh_host, username=ssh_user, password=ssh_pass)
    
    stdin, stdout, stderr = ssh.exec_command(cimc_cmd)

    stdout = stdout.readlines()
    ssh.close()
    
    state = "unknown"

    for line in stdout:

        line = str(line)

        if len(line.rstrip()) > 0:

            state = line
            
    return state.rstrip()

def get_cimc_serial_number(server_cimc):

    if server_cimc == 'server 1':
        server_ip = server_1
    else:
        server_ip = server_2

    return make_simple_cimc_call("powershell -Command \"& {./ucs-alexa/Get-ImcSerial.ps1 -Server " + server_ip + " -User " + cimc_admin_user + " -Pass " + cimc_admin_pass + "}\"")

def set_cimc_led(led_state,server_cimc):

    if server_cimc == 'server 1':
        server_ip = server_1
    else:
        server_ip = server_2

    return make_simple_cimc_call("powershell -Command \"& {./ucs-alexa/Set-ImcLed.ps1 -Server " + server_ip + " -User " + cimc_admin_user + " -Pass " + cimc_admin_pass + " -LedState " + led_state + "}\"")

def get_cimc_led(server_cimc):

    if server_cimc == 'server 1':
        server_ip = server_1
    else:
        server_ip = server_2

    return make_simple_cimc_call("powershell -Command \"& {./ucs-alexa/Get-ImcLed.ps1 -Server " + server_ip + " -User " + cimc_admin_user + " -Pass " + cimc_admin_pass + "}\"")


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Skill for UCS IMC Managment. " \
                    "You can say things like, Set Server Once LED state on, "\
                    "or Set Server One LED state off. You can also get the " \
                    "state of the LED by asking, what is the LED state on " \
                    "Server One. To retrieve a server's serial number ask, " \
                    "what is the serial number on Server One?"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask me something about the UCS Server. "
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills UCS sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def set_imc_led_state(intent, session):
    session_attributes = {}
    reprompt_text = None

    if 'ledstate' in intent['slots']:
        led_state = intent['slots']['ledstate']['value']
        server_cimc = intent['slots']['server']['value']
        set_cimc_led(led_state,server_cimc)

        speech_output = "I have set the LED state to " + \
                        led_state + ", on " + server_cimc + "."
        should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


def get_cimc_led_state(intent, session):
    session_attributes = {}
    reprompt_text = None

    server_cimc = intent['slots']['server']['value']
    led_state = get_cimc_led(server_cimc)

    speech_output = "The UCS Server LED state is " + led_state + "."
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def get_cimc_serial(intent, session):
    session_attributes = {}
    reprompt_text = None

    server_cimc = intent['slots']['server']['value']
    cimc_serial = get_cimc_serial_number(server_cimc)

    speech_output = "The UCS Server serial number is " + cimc_serial + "."
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "SetLedState":
        return set_imc_led_state(intent, session)
    elif intent_name == "GetLedState":
        return get_cimc_led_state(intent, session)
    elif intent_name == "GetSerialNumber":
        return get_cimc_serial(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

