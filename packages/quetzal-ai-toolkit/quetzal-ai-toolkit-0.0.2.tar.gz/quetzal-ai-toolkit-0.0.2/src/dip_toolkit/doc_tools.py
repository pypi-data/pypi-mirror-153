import cv2
import numpy as np

def scan_doc_from_image(imgpath, corners, w=250, h=350, verbose=True, show_img=True):
    """
        A utility to crop out the document from the provivded image
        Parameters
        @TODO: Will remove the param corners in future release
        ----------
        imgpath : str
            Full Path of the image
        corners : list
            list of co-ordinates of the corners of the doc
        w : int, optional, default 250
            width of the resultant image
        h: int, optional, default 350
            height of the resultant image
        verbose: bool, optional, default True
            if True, console logs will be enabled
        show_img: bool, optional, default True
            if True, the original and resultant image will be diaplayed

        Returns
        -------
        numpy array representing the resultant image
    """
    print("Reading image", imgpath) if verbose else None
    img = cv2.imread(imgpath)
    pts1 = np.float32(corners)
    pts2 = np.float32([[0,0],[w,0],[w,h],[0,h]])

    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgout = cv2.warpPerspective(img, matrix, (w,h))


    cv2.imshow("Original Image", img) if show_img else None
    cv2.imshow("Scanned Document", imgout) if show_img else None
    cv2.waitKey(0) if show_img else None

    return imgout