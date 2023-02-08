# @Time    : 2023/2/3
# @Author  : Bing

import cv2
import math

"""
Assume a point(x,y) in a pic, it's rotated by a degree around a coordinate point(x0,yo)

x0 = (x - rx0) * cos(a) - (y - ry0) * sin(a) + rx0 

y0 = (x - rx0) * sin(a) + (y - ry0) * cos(a) + ry0

"""

def angleRota(center_x,center_y,x,y,w,h,a):
    """

    Args:
        center_x: Rotating reference point
        center_y:Rotating reference point
        x: rectangle left up
        y: rectangle left up
        w: rectangle
        h: rectangle
        a: rotating degree

    Returns:

    """
    a = (math.pi/180)*a
    x1,y1 = x,y # left up
    x2,y2 = x+w,y # right up
    x3,y3 = x+w, y+h # right down
    x4,y4 = x,y+h #left down

    # rota
    px1 = int((x1 - center_x) * math.cos(a) - (y1 - center_y) * math.sin(a) + center_x)
    py1 = int((x1 - center_x) * math.sin(a) + (y1 - center_y) * math.cos(a) + center_y)
    px2 = int((x2 - center_x) * math.cos(a) - (y2 - center_y) * math.sin(a) + center_x)
    py2 = int((x2 - center_x) * math.sin(a) + (y2 - center_y) * math.cos(a) + center_y)
    px3 = int((x3 - center_x) * math.cos(a) - (y3 - center_y) * math.sin(a) + center_x)
    py3 = int((x3 - center_x) * math.sin(a) + (y3 - center_y) * math.cos(a) + center_y)
    px4 = int((x4 - center_x) * math.cos(a) - (y4 - center_y) * math.sin(a) + center_x)
    py4 = int((x4 - center_x) * math.sin(a) + (y4 - center_y) * math.cos(a) + center_y)
    pt1 = (px1, py1)
    pt2 = (px2, py2)
    pt3 = (px3, py3)
    pt4 = (px4, py4)

    angle = [pt1,pt2,pt3,pt4]

    return angle

def drawLine(img,angle,color,thickness):
    cv2.line(img,angle[0],angle[1],color,thickness)
    cv2.line(img, angle[1], angle[2], color, thickness)
    cv2.line(img, angle[2], angle[3], color, thickness)
    cv2.line(img, angle[3], angle[0], color, thickness)

    return img


def recRota(img,center_x,center_y,x1,y1,w,h,rota,draw=True):
    color = (255,255,0)
    thickness = 2
    angle = angleRota(x1,y1,x1,y1,w,h,rota)

    if draw==True:
        img = drawLine(img,angle,color,thickness)
        return img, angle
    else:
        return angle


