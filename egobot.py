# Copyright 2017 IBM Corp. All Rights Reserved.
# See LICENSE for details.
#
# Author: Henrik Loeser
#
# A slightly mutating ego-centric chatbot
# Using the IBM Watson Conversation service on IBM Bluemix
#
# See the README for documentation.
#
# Partially based on this repo https://github.com/data-henrik/watson-conversation-tool

import json, argparse
from os.path import join, dirname
from watson_developer_cloud import ConversationV1

# Credentials are read from a file
with open("config.json") as confFile:
     config=json.load(confFile)['credentials']

# Initialize the Conversation client
conversation = ConversationV1(
    username=config['username'],
    password=config['password'],
    version=config['version'],
    url=config['url']
    )


# Define parameters that we want to catch and some basic command help
def getParameters(args=None):
    parser = argparse.ArgumentParser(description='A slightly mutating ego-centric chatbot',
                                     prog='egobot.py',
                                     usage='%(prog)s [-h | -l | -logs | -dialog] [-id workspaceID]')
    parser.add_argument("-l",dest='listWorkspaces', action='store_true', help='list workspaces')
    parser.add_argument("-logs",dest='listLogs', action='store_true', help='list logs')
    parser.add_argument("-dialog",dest='dialog', action='store_true', help='have dialog')
    parser.add_argument("-setup",dest='setup', action='store_true', help='setup chatbot')
    parser.add_argument("-id",dest='workspaceID', help='Workspace ID')
    parser.add_argument("-name",dest='setupName', help='Workspace Name')
    parser.add_argument("-lang",dest='setupLanguage', help='Workspace Language')

    parms = parser.parse_args()
    return parms

# Setup workspace for specified language
def setupWorkspace(newName, newLang):
    # Load language-dependent workspace file
    inFile="resources/egobot."+newLang+".json"
    with open(inFile) as jsonFile:
        ws=json.load(jsonFile)

    # Now open localization file for chat language
    fname="lang/"+newLang+".json"
    with open(fname) as localizationFile:
        localizationConf=json.load(localizationFile)
    newWorkspace=conversation.create_workspace(name=newName,
                                               description=ws['description'],
                                               language=newLang,
                                               intents=ws["intents"],
                                               entities=ws["entities"],
                                               dialog_nodes=ws["dialog_nodes"],
                                               counterexamples=ws["counterexamples"],
                                               metadata=ws['metadata'])
    print localizationConf['setup']['details']
    print(json.dumps(newWorkspace, indent=2))
    print
    print localizationConf['setup']['workspaceID']+":\n\""+newWorkspace['workspace_id']+"\""


# List available dialogs
def listWorkspaces():
    print(json.dumps(conversation.list_workspaces(), indent=2))

# List logs for a specific workspace by ID
# For now just dump them, do not filter, do not store
def listLogs(workspaceID):
    print(json.dumps(conversation.list_logs(workspace_id=workspaceID), indent=2))

def listIntents(workspaceID):
    print(json.dumps(conversation.list_intents(workspace_id=workspaceID,export=False)['intents'], indent=2))

def listEntities(workspaceID):
    print(json.dumps(conversation.list_entities(workspace_id=workspaceID,export=False)['entities'], indent=2))

# Add new intent after gathering the necessary data
def addIntent(workspaceID, localizationConf):
    # Get intent name, description and examples
    inputForIntent = raw_input(localizationConf['intents']['iname']+"\n")
    descForIntent = raw_input(localizationConf['intents']['idescription']+"\n")
    examplesForIntent = raw_input(localizationConf['intents']['isamples']+"\n").split('/')

    # Create JSON array from examples
    samples=[]
    for num in range (0, len(examplesForIntent)):
        samples.append({"text": examplesForIntent[num]})

    # Now create the intent and print the JSON response
    print(json.dumps(conversation.create_intent(workspace_id=workspaceID,
                        intent=inputForIntent,
                        description=descForIntent,
                        examples=samples),
                         indent=2))


# Start a dialog and converse with Watson
#
def converse(workspaceID):
    # Fetch language of workspace
    lang=conversation.get_workspace(workspace_id=workspaceID)['language']

    # Now open localization file for chat language
    fname="lang/"+lang+".json"
    with open(fname) as localizationFile:
        localizationConf=json.load(localizationFile)
    print localizationConf['chat']['initialMessage']+"\n"
    print "=========================\n"
    # Start the dialog
    context={}

    # Now loop to chat
    while True:
        # get some input
        minput = raw_input(localizationConf['chat']['prompt']+"\n")
        # if we catch a "bye" then exit
        if (minput == "bye"):
            break
        # send the input to Watson
        resp=conversation.message(workspace_id=workspaceID,
                             message_input={'text': minput},
                             alternate_intents=True,
                             context=context,
                             entities=None,
                             intents=None,
                             output=None)

        print(json.dumps(resp))
        print
        if resp['intents'][0]['intent']=="Display" and resp['intents'][0]['confidence']>0.5:
            print resp['output']['text'][0]
            if resp['context']['action']:
                if resp['context']['action']=="listIntents":
                    listIntents(workspaceID)
                elif resp['context']['action']=="listEntities":
                    listEntities(workspaceID)
        elif resp['intents'][0]['intent']=="Create":
            print resp['output']['text'][0]
            if resp['context']['action']=="addIntent":
                addIntent(workspaceID,localizationConf)
        else:
            print resp['output']['text'][0]
        # Save context for next round, but wipe out the action
        context=resp['context']
        context['action']=""

#
# Main program, for now just detect what function to call and invoke it
#
if __name__ == '__main__':
    parms = getParameters()
    #print parms
    if (parms.listWorkspaces):
        listWorkspaces()
    if (parms.listLogs and parms.workspaceID):
        listLogs(parms.workspaceID)
    if (parms.dialog and parms.workspaceID):
        converse(parms.workspaceID)
    if (parms.setup and parms.setupName and parms.setupLanguage):
        setupWorkspace(newName=parms.setupName, newLang=parms.setupLanguage)
