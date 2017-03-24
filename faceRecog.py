import os
import subprocess
import urllib

def recog(img):
    urllib.urlretrieve("https://s3-ap-southeast-1.amazonaws.com/hellomark/capturedImg.jpg", "test/capturedImg.jpg")
    imgPath='test/capturedImg.jpg'
    s=subprocess.check_output(['classifier.py', 'infer', 'generated-embeddings/classifier.pkl', imgPath])
    resArr=s.split()
    nameArr = resArr[0].split('-')
    name = nameArr[0] + ' ' + nameArr[1]
    conf = resArr[1]
    return (name,conf)

def train(name, ):
