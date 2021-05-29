import requests
import json

URL = 'https://www.sms4india.com/api/v1/createSenderId'

apikey='YEJRRZMY0J688Q12WTS6E9K4NHDLXZIG'
secretkey='ZOUDXYB1652FU858'
useType='prod'
senderId='SMSIND'

# post request
def sendPostRequest(reqUrl, apiKey, secretKey, useType, senderId):
    req_params = {
    'apikey':apiKey,
    'secret':secretKey,
    'usetype':useType,
    'senderid':senderId
    }
    return requests.post(reqUrl, req_params)

# get response
response = sendPostRequest(URL, apikey, secretkey, useType, senderId)

# print response if you want
print(response.text)