import pandas as pd
import os
import psutil

def handle_uploaded_file(f):
    print(os.getcwd())
    with open(''+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def processed():
    pass


#processed()