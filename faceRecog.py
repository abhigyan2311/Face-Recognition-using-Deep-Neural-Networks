import os
import subprocess

def recog(img):
    imgPath='test/' + img
    s=subprocess.check_output(['./classifier.py', 'infer', 'generated-embeddings/classifier.pkl', imgPath])
    resArr=s.split()
    nameArr = resArr[0].split('-')
    name = nameArr[0] + ' ' + nameArr[1]
    conf = resArr[1]
    return (name,conf)

def train:
    
