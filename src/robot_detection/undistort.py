import cv2
import sys
import numpy as np
# You should replace these 3 lines with the output in calibration step
#DIM=(960, 540)
DIM=(960, 600)
K=np.array([[681.5626572119695, 0.0, 473.4431157496566], [0.0, 747.6024248469107, 300.84410910303563], [0.0, 0.0, 1.0]])
D=np.array([[-0.0910103495626607], [-0.12756310131759943], [0.2554180202614854], [-0.25239505058392225]])
# DIM=(480, 300)
# K=np.array([[666.9415965508599, 0.0, 431.95115471194333], [0.0, 717.6422902502163, 278.5371490457156], [0.0, 0.0, 1.0]])
# D=np.array([[0.037063993055043515], [-0.2506574643279681], [0.09389006223318914], [0.08024155824229262]])

class undistort(object):

    def __init__(self):
        print ('undistort running')

    def undistort(self, img, balance=0.0, dim2=(960, 600), dim3=(960, 600)):    
        dim1 = img.shape[:2][::-1]  #dim1 is the dimension of input image to un-distort  
        assert dim1[0]/dim1[1] == DIM[0]/DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"    
        if not dim2:
            dim2 = dim1    
        if not dim3:
            dim3 = dim1    
        
        scaled_K = K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.
        scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0    # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
        new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
        undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        return undistorted_img