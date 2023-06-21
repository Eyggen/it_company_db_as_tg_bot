import re

def check(param):
    if re.search(r'\d{4}-\d{2}-\d{2}', param):
        #print(0)
        param = str(param)
    elif (re.search(r'[1-9]', param) or re.search(r'-[1-9]', param)) and not re.search(r'\d', param):
        #print(1)
        param = int(param)
    elif (re.search(r'[1-9]*[.]?[1-9]', param) or re.search(r'-[1-9]*[.]?[1-9]', param)) and not re.search(r'\d', param):
        #print(2)
        param = float(param)
    else:
        #print(3)
        param = str(param)
    return param

print(type(check(param="Sentinel_2")))