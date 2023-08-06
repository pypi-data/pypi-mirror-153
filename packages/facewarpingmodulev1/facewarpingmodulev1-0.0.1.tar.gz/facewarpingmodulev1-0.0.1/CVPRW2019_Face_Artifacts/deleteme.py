from __init__ import  *
from io import BytesIO
import cv2


file = open('sample/2008_000003.jpg', 'rb')
# cap = cv2.VideoCapture('demo/demo_fake.mp4')
# print("FILE " , BytesIO(file).read())

print("eee" , detect_img(file))