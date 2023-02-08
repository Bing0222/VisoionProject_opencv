# @Time    : 2023/2/3
# @Author  : Bing


import cv2
import pickle
from rotaParking import recRota

# 1.load pic
filepath = 'C:/Users/WenBi/Desktop/Project/opencv/carParking.jpg'
filename = 'parking_position.txt' # save parking position

w,h = 100,50

try:
    with open(filename,'rb') as file_object:
        posList = pickle.load(file_object)

except:
    posList = []

# 2.callback function, mouse event trigger
def onMouse(events,x,y,flag,params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for index, pos in enumerate(posList):
            if pos[0]<x<pos[0]+w and pos[1]<y<pos[1]+h:
                posList.pop(index)
    # 3. save
    with open(filename,'wb') as file_object:
        pickle.dump(posList,file_object)


# 4. draw parking box
while True:
    img = cv2.imread(filepath)
    # Iterate over all the coordinates that the mouse clicked,
    # which is the xy coordinate in the top left corner of the rectangle
    for pos in posList:
        img, angle = recRota(img,pos[0],pos[1],pos[0],pos[1],w,h,-4)
    cv2.imshow('img',img)

    cv2.setMouseCallback('img',onMouse)
    key = cv2.waitKey(0)
    cv2.destroyAllWindows()
