from demo import *
import os



def detect_video(file):
    with open(r'demo/newfake.mp4', 'wb') as f:
        f.write(file.read())
    print("Testing ", file.name)
    response = run('demo')
    os.remove("demo/newfake.mp4")
    return response[0]

def detect_img(file):
    with open(r'demo/newimg.jpg', 'wb') as f:
        f.write(file.read())
    print("Testing ", file.name)
    response = run('demo')
    os.remove("demo/newimg.jpg")
    return response[0]

