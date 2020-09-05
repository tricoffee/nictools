import numpy as np
import cv2
import math
import os

def Sine(alpha):
    """

    :param alpha:  alpha是角度值，而非弧度
    :return:
    """
    return math.sin(math.radians(alpha))

def Cosine(alpha):
    """

    :param alpha: alpha是角度值，而非弧度
    :return:
    """
    return math.cos(math.radians(alpha))

def Actan(x):
    """

    :param x: math.atan(x)是角度值，而非弧度
    :return:
    """
    return math.atan(x)*180/(math.pi)



def rotateImg(img,theta):
    #旋转角度为 theta, 逆时针方向
    #theta = 30
    srcH,srcW,srcC = img.shape
    # print("# srcH ",srcH)
    # print("# srcW ",srcW)
    # print("# srcC ",srcC)
    # "theta"表示逆时针方向
    dstW = srcW*abs(Cosine(theta)) + srcH*abs(Sine(theta))
    dstH = srcH*abs(Cosine(theta)) + srcW*abs(Sine(theta))
    dstW = int(dstW)
    dstH = int(dstH)

    #创建新图像范围，使其包含旋转之后的矩形
    dstImg = np.zeros((dstH,dstW,srcC),dtype=np.uint8)

    for j in range(dstH):
        for i in range(dstW):
            # 逆时针旋转theta
            x = (i - dstW//2)*Cosine(theta) - (j - dstH//2)*Sine(theta) + srcW//2
            y = (i - dstW//2)*Sine(theta) + (j - dstH//2)*Cosine(theta) + srcH//2

            x1 = int(x)
            y1 = int(y)
            x2 = math.ceil(x)
            y2 = math.ceil(y)
            if x1 >= 0 and x1 <= srcW - 1 and y1 >= 0 and y1 <= srcH - 1 and \
                x2 >= 0 and x2 <= srcW - 1 and y2 >= 0 and y2 <= srcH - 1:
                for k in range(srcC):
                    t00 = float(img[y1,x1,k])
                    t01 = float(img[y2,x1,k])
                    t10 = float(img[y1,x2,k])
                    t11 = float(img[y2,x2,k])
                    # 双线性插值
                    a00 = t00
                    a01 = t01 - t00
                    a10 = t10 - t00
                    a11 = t00 + t11 - (t01 + t10)
                    deltaX = x - x1
                    deltaY = y - y1
                    tt = a00 + a10*deltaX + a01*deltaY + a11*deltaX*deltaY
                    dstImg[j,i,k] = tt
    return dstImg



filename = "C:/Users/BJ01/Desktop/dog.jpg"
img = cv2.imread(filename)
#旋转角度为 theta, 逆时针方向，最终输出逆时针旋转theta度之后的图像
theta = 30
dstImg = rotateImg(img,theta)
# angle = 30
# print(Sine(angle))
# angle = 60
# print(Cosine(angle))
# print(Actan(1))
# print(Sine(Actan(1)))
newAffineImgFnm = "C:/Users/BJ01/Desktop/newAffineImg-withInterpolate.{}".format(os.path.basename(filename))
cv2.imwrite(newAffineImgFnm,dstImg)


