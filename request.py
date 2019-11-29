# importing the requests library
import requests
import json

# api-endpoint
URL = "http://ec2-34-229-150-165.compute-1.amazonaws.com/dogs/"

# location given here

# defining a params dict for the parameters to be sent to the API
PARAMS = {"dogs":[{"name": 'testi', "image": 'toinen'}]}

# sending get request and saving the response as response object
r = requests.post(url=URL, json=PARAMS)

