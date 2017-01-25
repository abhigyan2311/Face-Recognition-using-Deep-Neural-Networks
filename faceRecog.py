import os
import subprocess

subprocess.call(['./classifier.py', 'infer', 'generated-embeddings/classifier.pkl', 'test/1.jpg'])
