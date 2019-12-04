# importing the requests library
import requests

def sendNewReport(userName, event, timeStamp, imageName):
    # api-endpoint
    URL = "http://ec2-34-229-150-165.compute-1.amazonaws.com/logins"

    # location given here

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'name': userName,'state': event,'time': timeStamp,'image': imageName}

    # sending get request and saving the response as response object
    r = requests.post(url=URL, json=PARAMS)

    print(r.text)