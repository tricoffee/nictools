import  os
import cv2
import numpy as np
# 原图像
img_fnm = "/dataset/imgs/1.bmp"
img = cv2.imread(img_fnm)
# mask图
mask_fnm = img_fnm.strip(".bmp")+"_mask.png"
print(mask_fnm)
mask = cv2.imread(mask_fnm, cv2.IMREAD_GRAYSCALE)
# 应用mask抠图
masked_img = cv2.add(img,np.zeros(np.shape(img), dtype=np.uint8), mask=mask)
new_fnm = "/dataset/imgs/1_masked.bmp"
cv2.imwrite(new_fnm,masked_img)
# 应用mask产生ROI轮廓（边界）
retval, binary = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# 判断point点是否在轮廓内部
point = (1981,1000)
cns_ = sorted(contours, key=lambda x: cv2.arcLength(x, True), reverse=True)
cns = cns_[0:2]
cv2.drawContours(img, cns, -1, (0, 0, 255), 3) # 将轮廓画在图像上

outside_flag = 1
for cn in cns:
    outside_flag *= cv2.pointPolygonTest(cn,point,False)
if outside_flag == 1:#点在ROI内部
    print("point {} is outside the ROI".format(point))
elif outside_flag == -1:#点在ROI外部
    print("point {} is inside the ROI".format(point))
elif outside_flag == 0:#点在边界上
    print("point {} is on the boundary of ROI".format(point))
else:
    raise NotImplementedError
# 保存画有轮廓的图像
bin_fnm = "/dataset/imgs/1_masked_binary.bmp"
cv2.imwrite(bin_fnm,img)
