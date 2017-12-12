import pandas as pd
import re

def process_sentence(s):
        s = re.sub(r' \.', ' ',s)
        s = s = re.sub(r'=',' ',s)
        s = re.sub(r'#+',' ',s)
        s = re.sub(r'\*+',' ',s)
        s = re.sub(r'_+',' ',s)
        s = re.sub(r':+',' ',s)
        s = re.sub(r'\(+',' ',s)
        s = re.sub(r'\)+',' ',s)
        s = re.sub(r'\|+',' ',s)
        s = re.sub(r'\\\w+',' ',s)
        s = re.sub(r'/+',' ',s)
        s = re.sub(r'\\+',' ',s)
        s = re.sub(r'[^\x00-\x7f]',' ', s)
        #s = re.sub(r'[[:digit:]]',' ',s)
        s = re.sub(r'\s+',' ',s)
        return s