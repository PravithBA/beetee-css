import time

source = ""

while True:
    f = open('dest/main.cvcss')
    source = f.read()
    time.sleep(0.5)
    print(source)