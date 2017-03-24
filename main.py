from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory
from fbrecog import recognize
import sys, json
import subprocess
import urllib

pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-383332aa-dcc0-11e6-b6b1-02ee2ddab7fe"
pnconfig.publish_key = "pub-c-73cca4b9-e219-4f94-90fc-02dd8f018045"
pnconfig.secret_key = "sec-c-YzcyZjI4NzEtNmUxMi00ZDc0LWI4ZGMtNGUyYmFlZmI1OTQ3"
pnconfig.ssl = False

access_token = 'EAAO8ErKT0tkBAMZAvvgsKAmg4OIXyAjM2CeUTrAQeib26eSGLlcWkIbY7BK5wreglZC6GiZBqDi8gyOOgfzSSz'
cookie = 'datr=dfRTWMGsPA7exeoXIj2LX43x; sb=-PRTWLHlqlWfTjtD62dzO59p; c_user=100002221569995; xs=1%3Ad2iAeVIJVH813Q%3A2%3A1490370805%3A4831; fr=0AlYydX1C7b1JYXjo.AWW21x2w4q6cKw-Q-g20bDm-03Q.BYI2pk.Bn.Fh8.0.0.BY1UD1.AWVHr2k9; csm=2; pl=n; lu=gghjXVbPCttQrj2bVnBiUC1w; presence=EDvF3EtimeF1490370848EuserFA21B02221569995A2EstateFDutF1490370848557CEchFDp_5f1B02221569995F3CC'
fb_dtsg = 'AQFR6XCnO_c6:AQF1CkRDYXg_' #Insert the fb_dtsg parameter obtained from Form Data here.

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
            print(type(conf))

            conf=float(conf)
            if(conf>75):
                pubnub.publish().channel('faceRecog').message([name]).sync()
            else:
                path='test/capturedImg.jpg'
                for line in sys.stdin:
                    path = line[:-1]
                print(recognize(path,access_token,cookie,fb_dtsg))





pubnub.add_listener(MySubscribeCallback())

pubnub.subscribe().channels('faceCapture').execute()
