from myutils import (
    list_basefiles,
    list_files
)
import os
import cv2

def inspect_img_scale(img_dir):
    fnms = list_files(img_dir)
    for fnm in fnms:
        img = cv2.imread(fnm)
        print(img.shape)

def crop(raw_dir,dst_dir):
    fnms = list_basefiles(raw_dir)
    for fnm in fnms:
        image_path = os.path.join(raw_dir, fnm)
        print("Cropping {}".format(image_path.replace("\\","/")))
        img = cv2.imread(image_path)
        img = img[0:12800, 0:8192]
        export_path = os.path.join(dst_dir, fnm)
        cv2.imwrite(export_path, img)

def roi(img_dir,bin_dir,cns_dir,roi_dir):
    fnms = list_basefiles(img_dir)

    for base_fnm in fnms:
        fnm = os.path.join(img_dir, base_fnm)
        # 读取图像
        img = cv2.imread(fnm)
        img0 = img.copy()
        img = cv2.medianBlur(img, 5)
        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        retval, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        new_fnm = "binary.{}".format(base_fnm)
        new_fnm = os.path.join(bin_dir, new_fnm)
        cv2.imwrite(new_fnm, binary)
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cns = []
        for cn in contours:
            if (len(cn) > 5) and cv2.arcLength(cn, True) > 10000:
                cns.append(cn)

        rx = 0
        rylist = []
        for c in cns:
            epsilon = 0.001 * cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, epsilon, True)
            # 轮廓特征之宽高比
            bx, by, bw, bh = cv2.boundingRect(c)
            aspect_ratio = float(bw) / bh
            # 椭圆的中心坐标，短轴长轴(也就是2b,2a)，旋转角度
            exy, eba, angle = cv2.fitEllipse(c)
            if (len(approx) < 100 and len(approx) > 4 and aspect_ratio < 0.5):
                cv2.drawContours(img0, [approx], -1, (0, 0, 255), 3)

                # 轮廓的矩
                mm = cv2.moments(c)
                # 使用前三个矩m00, m01和m10计算重心
                pt = (int(mm['m10'] / mm['m00']), int(mm['m01'] / mm['m00']))

                ptx, pty = pt

                for tmp in c:
                    tx, ty = tmp[0]
                    if ptx < tx:
                        rx = max(rx, tx)
                        rylist.append(ty)

        new_fnm = "img-with-contours.{}".format(base_fnm)
        new_fnm = os.path.join(cns_dir, new_fnm)
        cv2.imwrite(new_fnm, img0)

        rylist.sort(reverse=True)

        rx1 = rx
        ry1 = rylist[len(rylist) - 1]
        rx2 = rx
        ry2 = rylist[0]

        # ---------
        # (x11,y11)  .........(rx1,ry1)..... (x12,y12)
        #  ................................
        #  ................................
        #  ................................
        # (x21,y21)  .........(rx2,ry2)..... (x22,y22)
        # ---------

        x11 = rx1 - 150
        y11 = ry1
        x12 = rx1 + 10
        y12 = ry1
        x21 = rx2 - 150
        y21 = ry2
        x22 = rx2 + 10
        y22 = ry2
        #

        roi = img[y12:y22, x11:x12, :]
        roi_fnm = "roi-{}".format(base_fnm)
        roi_fnm = os.path.join(roi_dir, roi_fnm)

        # save roi
        cv2.imwrite(roi_fnm, roi)
        print("roi {}".format(roi_fnm))


def patch(roi_dir,pch_dir,window=160,skip=100):
    window = window
    skip = skip
    fnms = list_basefiles(roi_dir)
    for base_fnm in fnms:
        fnm = os.path.join(roi_dir, base_fnm)
        img = cv2.imread(fnm)

        num = int((img.shape[0] - window) / skip) + 1
        k = 0
        for i in range(num):
            patch = img[k:k + window, :, :]
            k = k + skip
            pch_fnm = "patch-{}-{}".format(i, base_fnm)
            pch_fnm = os.path.join(pch_dir, pch_fnm)
            print(pch_fnm)
            # save patch
            cv2.imwrite(pch_fnm, patch)
