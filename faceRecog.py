import os
import subprocess

s=subprocess.check_output(['./classifier.py', 'infer', 'generated-embeddings/classifier.pkl', 'test/1.jpg'])

resArr=s.split()
nameArr = resArr[0].split('-')
name = nameArr[0] + ' ' + nameArr[1]
conf = resArr[1]

print name
print conf
