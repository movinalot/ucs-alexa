from __future__ import print_function
import paramiko
import unicodedata

ssh_host = '10.10.10.10'
ssh_user = 'ssh_user'
ssh_pass = 'ssh_pass'

ucsm_domain_1 = '10.10.10.20'
ucsm_domain_2 = '10.10.10.30'

ucsm_admin_user = 'admin'
ucsm_admin_pass = 'password'

def make_simple_ucsapi_call(ucs_api_cmd):

    ucs_api_response = "0,0,0,0"  
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ssh_host, username=ssh_user, password=ssh_pass)
    
    stdin, stdout, stderr = ssh.exec_command(ucs_api_cmd)

    stdout = stdout.readlines()
    ssh.close()

    
    for line in stdout:

        line = str(line)

        if len(line.rstrip()) > 0:

            ucs_api_response = line
            
    return ucs_api_response.rstrip()

def get_ucsm_faults(ucsm_domain):

    if ucsm_domain == '1':
        ucsm_domain_ip = ucsm_domain_1
    else:
        ucsm_domain_ip = ucsm_domain_2

    return make_simple_ucsapi_call("powershell -Command \"& {./Get-UcsFaultCount.ps1 -ucsHost " + ucsm_domain_ip + " -ucsUser " + ucsm_admin_user + " -ucsPass " + ucsm_admin_pass + "}\"")

def get_ucsm_server_faults(ucsm_domain,ucsm_chassis,ucsm_blade):

    if ucsm_domain == '1':
        ucsm_domain_ip = ucsm_domain_1
    else:
        ucsm_domain_ip = ucsm_domain_2

    return make_simple_ucsapi_call("powershell -Command \"& {./Get-UcsBladeFaultCount.ps1 -ucsHost " + ucsm_domain_ip + " -ucsUser " + ucsm_admin_user + " -ucsPass " + ucsm_admin_pass + " -ucsChassis " + ucsm_chassis + " -ucsBlade " + ucsm_blade + "}\"")

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
    speech_output = "Welcome to the Alexa Skill for UCS Managment. " \
                    "You can say things like, what are the faults counts on domain one? " \
                    "You can ask what are the faults counts on chassis two blade 3?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask me what is the LED state? "
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skill for UCS Management. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def get_faults(intent, session):
    session_attributes = {}
    reprompt_text = None

    ucsm_domain = intent['slots']['domain']['value']
    fault_counts = get_ucsm_faults(ucsm_domain)

    faults = fault_counts.split(',')

    speech_output = "For the queried UCS domain, there are, " \
                    + faults[0] + ", critical faults, " \
                    + faults[1] + ", major faults, " \
                    + faults[2] + ", minor faults, and," \
                    + faults[3] + ", warnings."
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


def get_blade_faults(intent, session):
    session_attributes = {}
    reprompt_text = None

    ucsm_domain = intent['slots']['domain']['value']
    ucsm_chassis = intent['slots']['chassis']['value']
    ucsm_blade = intent['slots']['serverid']['value']
    fault_counts = get_ucsm_server_faults(ucsm_domain,ucsm_chassis,ucsm_blade)

    faults = fault_counts.split(',')

    speech_output = "For the queried UCS blade, there are, " \
                    + faults[0] + ", critical faults, " \
                    + faults[1] + ", major faults, " \
                    + faults[2] + ", minor faults, and," \
                    + faults[3] + ", warnings."
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
    if intent_name == "GetFaults":
        return get_faults(intent, session)
    elif intent_name == "GetServerFaults":
        return get_blade_faults(intent, session)
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

