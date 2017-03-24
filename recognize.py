from fbrecog import recognize
import sys, json

for line in sys.stdin:
 path = line[:-1]

path = './'+path+'.jpg'
access_token = 'EAAO1qxWMufsBAMYl0IUWKnMhQ2ebDMjtlm5Oh9LB4U6Fbp13U1ewGzSKPovxiWUg3OH7q9YG39bQwGVlxeXjJKi7BonaggZCSzAwn1pHMX3HZAtE34XiLBf1AddBys4mCUErDbkIwJ9f9QFzZBV3yIP9jzubbMk4N3mw4EX8wZDZD'
cookie = 'datr=dfRTWMGsPA7exeoXIj2LX43x; sb=-PRTWLHlqlWfTjtD62dzO59p; c_user=100002221569995; xs=11%3AO5u2NHgGlMHFKQ%3A2%3A1481897208%3A4831; fr=0AlYydX1C7b1JYXjo.AWVrlN-NQoFxwO-PJS4qyq4MscE.BYI2pk.Bn.AAA.0.0.BYU_T4.AWWKuXn1; csm=2; s=Aa6AwfHffG_4nCdT.BYU_T4; pl=n; lu=ggFeRlLj9_Xkmmb3xPIA46SA; act=1481897312600%2F1; p=-2; presence=EDvF3EtimeF1481897390EuserFA21B02221569995A2EstateFDutF1481897390118CEchFDp_5f1B02221569995F4CC;'
fb_dtsg = 'AQG9AGMpnGmx%3AAQF8DLfTx81k' #Insert the fb_dtsg parameter obtained from Form Data here.
print(recognize(path,access_token,cookie,fb_dtsg))


