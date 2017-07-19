from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory
from fbrecog import recognize
import sys, json
import subprocess
import urllib
import requests

pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-383332aa-dcc0-11e6-b6b1-02ee2ddab7fe"
pnconfig.publish_key = "pub-c-73cca4b9-e219-4f94-90fc-02dd8f018045"
pnconfig.secret_key = "sec-c-YzcyZjI4NzEtNmUxMi00ZDc0LWI4ZGMtNGUyYmFlZmI1OTQ3"
pnconfig.ssl = False

# Python FB Recog
access_token = 'EAACEdEose0cBAKy8ZCBws0vy9afemiROAPxoELKSCGQl8llYbKjvulx0D9Bw2g9p4EHYR4IUwbeLcMEOcVGimZCHa1Wflk8t2UFteUV3oaZCAc5Oj7PK3ofVvscerf53zh3xpYFdZCKZC1jL1oRClMZCbm36gKHIxYXQ3PtoIhbvN3UYhy1m3u'
cookie = 'datr=8wXpWOwBF5zcTxi5xMExyte9; sb=EQbpWNv6X1UWIz9BVRei6SHq; c_user=1842019331; xs=34%3AKCfAlA5OfOAOKA%3A2%3A1491666449%3A10351; fr=0OixAHtbgwIdlgHAk.AWVQKbVnjXcqZErMPcHLz98YetQ.BY6QXz.u3.AAA.0.0.BY6QYR.AWVACKPI; pl=n; lu=ggQSCKfnOEB5SsrO47Bl1FkA; presence=EDvF3EtimeF1491666468EuserFA21842019331A2EstateFDutF1491666468166CEchFDp_5f1842019331F2CC'
fb_dtsg = 'AQHgIxDYSM3I:AQGX5-a1FDM9'

#NodeJS FB Recog
# data={"accessToken":"EAAO1qxWMufsBAK3EBf6wf1YHojaaMqZBZCeYQhvqZBPOLveYl7hznEAZAPCxL6Nz7rZBZBC7xtv1N7SqOssqdZB8OZAZBSfEtYoq7MBmR2BY7KBZBucLOnmd8aWKQz7Icr2XwPC3xDaI00UNBEcGpBZCssUZARJgejxVlQIZD",
# 	  "url":"https://s3-ap-southeast-1.amazonaws.com/hellomark/capturedImg.jpg"}
# API_ENDPOINT="http://helloava.southindia.cloudapp.azure.com:3000/recognize"

pubnub = PubNub(pnconfig)

class MySubscribeCallback(SubscribeCallback):
    def status(self, pubnub, status):
        pass
        # The status object returned is always related to subscribe but could contain
        # information about subscribe, heartbeat, or errors
        # use the operationType to switch on different options
        if status.operation == PNOperationType.PNSubscribeOperation \
                or status.operation == PNOperationType.PNUnsubscribeOperation:
            if status.category == PNStatusCategory.PNConnectedCategory:
                pass
                # This is expected for a subscribe, this means there is no error or issue whatsoever
            elif status.category == PNStatusCategory.PNReconnectedCategory:
                pass
                # This usually occurs if subscribe temporarily fails but reconnects. This means
                # there was an error but there is no longer any issue
            elif status.category == PNStatusCategory.PNDisconnectedCategory:
                pass
                # This is the expected category for an unsubscribe. This means there
                # was no error in unsubscribing from everything
            elif status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                pass
                # This is usually an issue with the internet connection, this is an error, handle
                # appropriately retry will be called automatically
            elif status.category == PNStatusCategory.PNAccessDeniedCategory:
                pass
                # This means that PAM does allow this client to subscribe to this
                # channel and channel group configuration. This is another explicit error
            else:
                pass
                # This is usually an issue with the internet connection, this is an error, handle appropriately
                # retry will be called automatically
        elif status.operation == PNOperationType.PNSubscribeOperation:
            # Heartbeat operations can in fact have errors, so it is important to check first for an error.
            # For more information on how to configure heartbeat notifications through the status
            # PNObjectEventListener callback, consult <link to the PNCONFIGURATION heartbeart config>
            if status.is_error():
                pass
                # There was an error with the heartbeat operation, handle here
            else:
                pass
                # Heartbeat operation was successful
        else:
            pass
            # Encountered unknown status type

    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def message(self, pubnub, message):
        if(message.channel == 'faceCapture'):
            urllib.urlretrieve("https://s3-ap-southeast-1.amazonaws.com/hellomark/capturedImg.jpg", "test/capturedImg.jpg")
            imgPath='test/capturedImg.jpg'
            s=subprocess.check_output(['./classifier.py', 'infer', 'generated-embeddings/classifier.pkl', imgPath])
            resArr=s.split()
            nameArr = resArr[0].split('-')
            name = nameArr[0] + ' ' + nameArr[1]
            conf = resArr[1]
            print(conf)
            print(name)
            conf=float(conf)
            if(conf>0.80):
                pubnub.publish().channel('faceRecog').message([name]).sync()
            else:
                #Python
                resp = recognize(imgPath,access_token,cookie,fb_dtsg)
                conf = resp[0]['certainity']
                name = resp[0]['name']
                print(conf,name)

                #NodeJS
                # response=requests.post(url=API_ENDPOINT,data=data)
            	# json_data = json.loads(response.text)
            	# conf=json_data[0]["recognitions"][0]["certainty"]
            	# name=json_data[0]["recognitions"][0]["user"]["name"]
            	# print(conf,name)
            	if(conf>0.75):
            		pubnub.publish().channel('faceRecog').message([name]).sync()
            	else:
            		print("not matched")

pubnub.add_listener(MySubscribeCallback())

pubnub.subscribe().channels('faceCapture').execute()
