


import pandas as pd
import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

#旧的目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# dicta = {"name":[1111111]}
# aa = pd.read_csv(r"aaa.csv")
print(BASE_DIR)

if os.path.exists("aaa.csv"):
    print("aaaa")
else:
    print("bbb")