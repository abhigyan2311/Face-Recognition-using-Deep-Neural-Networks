import os
import subprocess

s=subprocess.check_output(['./classifier.py', 'infer', 'generated-embeddings/classifier.pkl', 'test/1.jpg'])
print "OK"
print s
