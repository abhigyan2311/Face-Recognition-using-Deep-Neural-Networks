import os
import subprocess

s=subprocess.check_output(['./classifier.py', 'infer', 'generated-embeddings/classifier.pkl', 'test/1.jpg'])
print s
resArr=s.split()
print resArr[0]
print resArr[1]
