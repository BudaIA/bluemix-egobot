# Egobot
## A slightly mutating ego-centric chatbot
Chat with this bot, ask about its metadata and make the bot apply changes to itself.

The code supports chatbots in any language. A German and English version is provided.

A sample session:   

![](https://raw.githubusercontent.com/data-henrik/bluemix-egobot/master/images/egobot-session.en.gif)

# Setup instructions coming...

If you have been working with the Watson service and Python before, you probably already have everything installed. If not, you need to install Python and then head over to the Watson Developer Tools and follow the link to the [Python SDK](https://github.com/watson-developer-cloud/python-sdk). Install the SDK, too. Now download a copy of this repository or clone it.   
To use the tool, copy `config.json.sample` to `config.json` and insert your service credentials. Note that the service URL depends on the IBM Bluemix region. It is shown as part of the credentials. You can read here more about [how to manage the Bluemix service keys](https://www.ibm.com/blogs/bluemix/2017/06/manage-bluemix-service-keys-via-cli/).

English setup:   
```
python egobot.py -setup -name egoEnglish -lang en
```
German setup:
```
python egobot.py -setup -name egoDeutsch -lang de
```


Wait 1-5 minutes for the training of Watson Conversation to be completed.

Start the dialog:   
```
python egobot.py -dialog -id "fasda5-xxxx-yyyy-913e-cde11d305ccf"
```


# Documentation and Resources
Here are some useful links to documentation and other resources:
* Watson Conversation service: https://www.ibm.com/watson/developercloud/doc/conversation/index.html
* API for Watson Conversation service: https://www.ibm.com/watson/developercloud/conversation/api/v1/#introduction
* Python SDK, Watson Developer Cloud: https://github.com/watson-developer-cloud/python-sdk
* Conversation API file in Python SDK: https://github.com/watson-developer-cloud/python-sdk/blob/master/watson_developer_cloud/conversation_v1.py
* The `argparse` module used for this tool: https://docs.python.org/2/library/argparse.html
* Watson Conversation Tool: https://github.com/data-henrik/watson-conversation-tool


# License
See [LICENSE](LICENSE) for license information.

The tool is provided on a "as-is" basis and is un-supported. Use with care...

# Contribute / Contact Information
If you have found errors or some instructions are not working anymore, then please open an GitHub issue or, better, create a pull request with your desired changes.

You can find more tutorials and sample code at:
https://ibm-bluemix.github.io/
