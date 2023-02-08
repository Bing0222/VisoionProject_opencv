# @Time    : 2023/2/3
# @Author  : Bing


import cv2
import pickle
from rotaParking import recRota
from rotaParking import drawLine

filepath = 'C:/Users/WenBi/Desktop/Project/opencv/carPark.mp4'
cap = cv2.VideoCapture(filepath)

# load recode(parking position in .txt)
filename = 'C:/Users/WenBi/Desktop/Project/opencv/parking_position.txt'
with open(filename,'rb') as f:
    posList = pickle.load(f)

# Process each frame of the image
while True:
    success, img = cap.read()
    imgCopy = img.copy()
    img_w,img_h = img.shape[:2]

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    w,h = 100,50

    for pos in posList:
        angle = recRota(img, pos[0], pos[1], pos[0], pos[1], w, h, -4, draw=False)
        rota_params = cv2.getRotationMatrix2D(angle[0],angle=-4,scale=1)
        rota_img = cv2.warpAffine(img, rota_params, (img_w, img_h))
        imgCrop = rota_img[pos[1]:pos[1] + h, pos[0]:pos[0] + w]
        cv2.imshow(f'imgCrop:{pos[0], pos[1]}', imgCrop)
        imgCopy = drawLine(imgCopy, angle, (255, 255, 0), 3)

    cv2.imshow('img',imgCopy)
    if cv2.waitKey(10) & 0xFF==27:
        break

cap.release()
cv2.destroyAllWindows()
