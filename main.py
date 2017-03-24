from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory
import subprocess
import urllib

pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-383332aa-dcc0-11e6-b6b1-02ee2ddab7fe"
pnconfig.publish_key = "pub-c-73cca4b9-e219-4f94-90fc-02dd8f018045"
pnconfig.secret_key = "sec-c-YzcyZjI4NzEtNmUxMi00ZDc0LWI4ZGMtNGUyYmFlZmI1OTQ3"
pnconfig.ssl = False

pubnub = PubNub(pnconfig)

class MySubscribeCallback(SubscribeCallback):
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

            #code here Aalekh Sir

            pubnub.publish().channel('faceRecog').message([name]).sync()


pubnub.add_listener(MySubscribeCallback())

pubnub.subscribe().channels('faceCapture').execute()
