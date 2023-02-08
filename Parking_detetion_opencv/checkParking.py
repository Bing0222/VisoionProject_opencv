# @Time    : 2023/2/3
# @Author  : Bing


# 处理视频图像
import cv2
import pickle
import numpy as np
from rotaParking import recRota  # 导入自定义的旋转矩形框函数
from rotaParking import drawLine  # 导入绘制旋转矩形线条函数

# （1）读取视频
filepath = 'C:\\Users\\WenBi\\Desktop\\Project\\opencv\\carPark.mp4'
cap = cv2.VideoCapture(filepath)

# 初始的车位框颜色
color = (255, 255, 0)

# （2）导入先前记录下来的车位矩形框的左上角坐标
filename = 'parking_position.txt'  # 保存的车位坐标
with open(filename, 'rb') as f:
    posList = pickle.load(f)

# （3）处理每一帧图像
while True:

    # 记录有几个空车位
    spacePark = 0

    # 返回图像是否读取成功，以及读取的帧图像img
    success, img = cap.read()

    # 为了使裁剪后的单个车位里面没有绘制的边框，需要在画车位框之前，把原图像复制一份
    imgCopy = img.copy()

    # 获得整每帧图片的宽和高
    img_w, img_h = img.shape[:2]  # shape是(w,h,c)

    # ==1== 转换灰度图，通过形态学处理来检测车位内有没有车
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ==2== 高斯滤波,卷积核3*3,沿x和y方向的卷积核的标准差为1
    imgGray = cv2.GaussianBlur(imgGray, (3, 3), 1)

    # ==3== 二值图，自适应阈值方法
    imgThresh = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 101, 20)

    # ==4== 删除零散的白点，
    # 如果车位上有车，那么车位上的像素数量(白点)很多，如果没有车，车位框内基本没什么白点
    imgMedian = cv2.medianBlur(imgThresh, 5)

    # ==5== 扩张白色部分，膨胀
    kernel = np.ones((3, 3), np.uint8)  # 设置卷积核
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)  # 迭代次数为1

    # 由于这个视频比较短，就循环播放这个视频
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        # 如果当前帧==总帧数，那就重置当前帧为0
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # （4）绘制停车线矩形框
    w, h = 90, 160  # 矩形框的宽和高

    # 遍历所有的矩形框坐标
    for pos in posList:
        # 得到旋转后的矩形的四个角坐标，传入原图，旋转参考点坐标，矩形框左上角坐标，框的宽w和高h，逆时针转4°
        angle = recRota(imgDilate, pos[0], pos[1], pos[0], pos[1], w, h, -4, draw=False)  # 裁剪的车位不绘制车位图

        # （5）裁剪所有的车位框，由于我们的矩形是倾斜的，先要把矩形转正之后再裁剪
        # 变换矩阵，以每个矩形框的左上坐标为参考点，顺时针寻转4°，旋转后的图像大小不变
        rota_params = cv2.getRotationMatrix2D(angle[0], angle=-4, scale=1)

        # 旋转整张帧图片，输入img图像，变换矩阵，指定输出图像大小
        rota_img = cv2.warpAffine(imgDilate, rota_params, (img_w, img_h))

        # 裁剪摆正了的矩形框，先指定高h，再指定宽w
        imgCrop = rota_img[pos[1]:pos[1] + h, pos[0]:pos[0] + w]

        # 显示裁剪出的图像
        cv2.imshow('imgCrop', imgCrop)

        # （6）计算每个裁剪出的单个车位有多少个像素点
        count = cv2.countNonZero(imgCrop)

        # 将计数显示在矩形框上
        cv2.putText(imgCopy, str(count), (pos[0] + 5, pos[1] + 20), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)

        # （7）确定车位上是否有车
        if count < 3000:  # 像素数量小于2500辆就是没有车
            color = (0, 255, 0)  # 没有车的话车位线就是绿色
            spacePark += 1  # 每检测到一个空车位，数量就加一
        else:
            color = (0, 0, 255)  # 有车时车位线就是红色

        # （8）绘制所有车位的矩形框
        # 在复制后的图像上绘制车位框
        imgCopy = drawLine(imgCopy, angle, color, 3)

    # 绘制目前还剩余几个空车位
    cv2.rectangle(imgCopy, (0, 150), (200, 210), (255, 255, 0), cv2.FILLED)
    cv2.rectangle(imgCopy, (5, 155), (195, 205), (255, 255, 255), 3)
    cv2.putText(imgCopy, 'FREE: ' + str(spacePark), (31, 191), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 3)

    # （9）显示图像，输入窗口名及图像数据
    cv2.imshow('img', imgCopy)  # 原图
    cv2.imshow('imgGray', imgGray)  # 高斯滤波后
    cv2.imshow('imgThresh', imgThresh)  # 二值化后
    cv2.imshow('imgMedian', imgMedian)  # 模糊后
    cv2.imshow('imgDilate', imgDilate)  # 膨胀

    if cv2.waitKey(1) & 0xFF == 27:  # 每帧滞留20毫秒后消失，ESC键退出
        break

# 释放视频资源
cap.release()
cv2.destroyAllWindows()