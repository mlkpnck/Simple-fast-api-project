import time

from utils import generateAccessToken

for i in range(1,30):
    time.sleep(2)
    print(generateAccessToken())