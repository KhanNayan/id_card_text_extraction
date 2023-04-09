
from craft_text_detector import Craft
import cv2
import numpy as np
from matplotlib import pyplot as plt
# from math import sin, cos, radians
import warnings
warnings.filterwarnings("ignore", category=UserWarning) 

def gray_scale(path):
    '''
    this function is used for read the image from drive.
    it convert image into gray scale image and retun it.
    @param : it take image path as a string type data.
    @return : it returns gray image and orginal image
    '''
    try:
        img  = cv2.imread(path,cv2.IMREAD_UNCHANGED)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # plt.imshow(img_gray,cmap='gray')
        # plt.show()
        return img_gray,img
    except Exception as e:
        return e 
def img_rotation(img_gray,angle):
    '''
    this function is used for rotate the image.
    @param : it take canny edge detected image.
    @return : it rotate the image counter clockwise.
    '''
    h, w = img_gray.shape[:2]
    M = cv2.getRotationMatrix2D((int(w/2), int(h/2)), int(angle), 1)
    img_gray = cv2.warpAffine(img_gray, M, (w, h))
    return img_gray 

def rotation_angle(regions,img_gray):
    """
    The coordinates of the texts on the id card are converted 
    to x, w, y, h type and the centers and coordinates of these boxes are returned.
    """
    angles = []
    for i,box_region in enumerate (regions):

        if i >= 0:
            def first(n):
                return n[0]
            def last(n):
                return n[-1]

            reg1 = sorted(box_region, key= first)

            ks = [reg1[0],reg1[1]]
            ks_sort = sorted(ks, key= last)
            
            ks1 = [reg1[2],reg1[3]]
            ks1_sort = sorted(ks1, key= last)

            final = np.array([ks_sort[0],ks_sort[1],ks1_sort[1],ks1_sort[0]],
                np.int32)

            x1,y1, x2, y2, x3, y3, x4, y4 = np.int0(final.reshape(-1))

            if y2 > y3:
                a = np.array([x2,y1])
                b = np.array([x1, y1]) # y max
                c = np.array([x2, y2])
                ba = a - b
                bc = c - b
                cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
                angle = np.arcsin(cosine_angle)
                
                # print ("degree " + str(np.degrees(angle)))
                angle = -np.degrees(angle)
                angles.append(angle)

            elif y2 < y3:
                a = np.array([x1,y2])
                b = np.array([x2, y2]) # y max
                c = np.array([x1, y1])
                ba = a - b
                bc = c - b
                cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
                angle = np.arcsin(cosine_angle)
                
                # print ("degree " + str(np.degrees(angle)))
                angle = np.degrees(angle)
                angles.append(angle)
                
    return angles

def box_regions(regions):
    """
    The coordinates of the texts on the id card are converted 
    to x, w, y, h type and the centers and coordinates of these boxes are returned.
    """
    boxes = []
    centers = []
    for box_region in regions:

        x1,y1, x2, y2, x3, y3, x4, y4 = np.int0(box_region.reshape(-1))
        x = min(x1, x3)
        y = min(y1, y2)
        w = abs(min(x1,x3) - max(x2, x4))
        h = abs(min(y1,y2) - max(y3, y4))

        cX = round(int(x) + w/2.0)
        cY = round(int(y) + h/2.0)
        centers.append((cX, cY))
        bbox = (int(x), w, int(y), h)
        boxes.append(bbox)
    return np.array(boxes), np.array(centers)

def heat_map(image):
    """
    takes the ID image and sends it to the craft model. 
    Craft returns the character density map and
    the box coordinates of the characters in the image.
    """
    input_image = image.copy()
    craft = Craft(cuda=False)
    prediction_result = craft.detect_text(input_image)
    heatmaps = prediction_result["heatmaps"]
   
    return heatmaps["text_score_heatmap"], prediction_result["boxes"]

def denoise(img_segment):
    img_segment = cv2.fastNlMeansDenoising(img_segment)
    kernel = np.ones((2,1), np.uint8)
    img_segment = cv2.dilate(img_segment, kernel, iterations=1)
    return img_segment

# def adaptive_thresholding(img_segment):
#     # hsv = cv2.cvtColor(img_segment, cv2.COLOR_BGR2HSV)
#     lower = np.array([0, 0])
#     upper = np.array([100, 175])
#     mask = cv2.inRange(img_segment, lower, upper)

#     # Invert image and OCR
    # invert = 255 - mask
    # return invert

# def median_subtract(noisy_img):
#     background=cv2.medianBlur(noisy_img, 33)
#     result=cv2.subtract(background, noisy_img)
#     result=cv2.bitwise_not(result)
#     return (result, background)

def image_preprocessing(path):
    '''
    main function of image processing and augmentation.
    @param : it take os path as input.
    @return : processed image to extract data from it.
    '''
    img_gray,img = gray_scale(path)

    txt_heat_map, regions = heat_map(img_gray)
    
    angles = rotation_angle(regions,img_gray)
    neg_count = len(list(filter(lambda x: (x < 0), angles)))

    pos_count = len(list(filter(lambda x: (x >= 0), angles)))

    if pos_count >= neg_count :
        angles = list(filter(lambda x : x >= 0, angles))
    else:
        angles = list(filter(lambda x : x < 0, angles))
    
    angle = sum(angles)/len(angles)
    print("Rotation Angle: " + str(angle))
    img_gray = img_rotation(img_gray,angle)

    return img_gray,img
    

