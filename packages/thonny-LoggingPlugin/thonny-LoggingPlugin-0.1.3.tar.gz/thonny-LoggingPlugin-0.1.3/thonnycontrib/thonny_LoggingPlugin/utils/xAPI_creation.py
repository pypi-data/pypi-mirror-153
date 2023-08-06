# This script has as goal to convert data to the format xAPI 

EVENTTYPE_TO_VERB_ID = {
    'Run_program'   : 'https://www.serveur.com/verbs/Run.Program',
    'Run_command'   : 'https://www.serveur.com/verbs/Run.Command',
    'Open'          : 'https://www.serveur.com/verbs/File.Open',
    'Save'          : 'https://www.serveur.com/verbs/File.Save',
    'Session_start' : 'https://www.serveur.com/verbs/Session.Start',
    'Session_end'   : 'https://www.serveur.com/verbs/Session.End',
}

def convert_to_xAPI(data):
    """
    Convert the data to xAPI format
    Args :
        data (object: dict()): the data to convert
    Return :
        (object: dict()): the data to xAPI format

    """
    statement = {
        'timestamp' : data['timestamp'],
        'verb' : create_verb(data),
        'actor' : create_actor(data),
        'object' : create_object(data),
        'context' : create_context(data)
    }
    if data['eventType'] in {'Run_program','Run_command'}:
        statement['result'] = create_result(data)

    return statement

def create_actor(data):
    """
    Create an xAPI actor from the data

    Args :
        data (object: dict()): the data to convert
    Return :
        (object: dict()): an actor from the xAPI format
    """
    return {"openid" :'https://www.serveur.com/user/' + str(data['userID'])}

def create_verb(data):
    """
    Create an xAPI verb from the data

    Args :
        data (object: dict()): the data to convert
    Return :
        (object: dict()): an verb from the xAPI format
    """
    return {'id' : EVENTTYPE_TO_VERB_ID[data['eventType']]}

def create_object(data):
    """
    Create an xAPI object from the data

    Args :
        data (object: dict()): the data to convert
    Return :
        (object: dict()): an object from the xAPI format
    """
    object = dict()
    type = data['eventType']
    if type in ('Open','Save'):
        object['id'] = 'https://www.serveur.com/object/File'
        object['extension'] = {
            "https://www.serveur.com/object/File/Filename" : data['filename'],
            "https://www.serveur.com/object/File/CodeStateID" : data['codestate'][1]
        }
    elif type == 'Run_program':
        object['id'] = 'https://www.serveur.com/object/Program'
        object['extension'] = {
            'https://www.serveur.com/object/Command/CommandRan' : data['command'],
            'https://www.serveur.com/object/CodeState/CurrentEditorContent' : data['codestate']
            }

    elif type == 'Run_command' :
        object['id'] = 'https://www.serveur.com/object/Command'
        object['extension'] = {'https://www.serveur.com/object/Command/CommandRan' : data['command']}
    elif type in {'Session_start','Session_end'} :
        object['id'] = 'https://www.serveur.com/object/Session'
    else :
        raise Exception("Error : eventType not accepted")
    return object

def create_result(data):
    """
    Create an xAPI result from the data

    Args :
        data (object: dict()): the data to convert
    Return :
        (object: dict()): an result from the xAPI format
    """
    return{
        "extension" : {
            "https://www.serveur.com/object/Command/stdin"     : data['stdin'],
            "https://www.serveur.com/object/Command/stdout"    : data['stdout'],
            "https://www.serveur.com/object/Command/stderr"    : data['stderr'],
            },
        "success" : data['status']
    }

def create_context(data):
    """
    Create an xAPI context from the data

    Args :
        data (object: dict()): the data to convert
    Return :
        (object: dict()): an context from the xAPI format
    """
    return {'extension' : { 'https://www.serveur.com/object/Session/ID' : str(data['sessionID']) }}


