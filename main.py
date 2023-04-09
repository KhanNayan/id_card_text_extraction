import os
from matplotlib import pyplot as plt
import preprocess
import text_detection
from card_type import id_card_formation
import cv2
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def nvid_image_process(path):
    '''
    Take image path as input, and feed it to image preporeccesing module.
    Check if the path is valid.
    @return processed image with angel rotation and denoizing filters.
    '''
    if os.path.isfile(path):
        img_gray,img = preprocess.image_preprocessing(path)
        return img_gray,img
    else :
        print("Invalid file path")

def nvid_text_detection(img_gray,img):
        txt_heat_map, regions = preprocess.heat_map(img_gray)
        boxes,center =preprocess.box_regions(regions)
        x_mean = np.mean(boxes, axis=0)
        max_len = 0
        for box in boxes:
            if int(box[0])+int(box[1]) > max_len:
                max_len = int(box[0])+int(box[1])
        # img_gray=preprocess.adaptive_thresholding(img)
        print(x_mean[0])
        data_store = []
        t = []
        tx = []
        ty = []
        for box in boxes:
            x = box[0]- 1
            y = box[2]- 1
            w = box[1] + 2
            h = box[3] + 2
            t.append((x,y))
            tx.append(x)
            ty.append(y)
            if x>= x_mean[0]-150 and x+w <= max_len:
                img_temp = img_gray.copy()
                img_segment = img_temp[y:y+h,x:x+w]

                # plt.imshow(img_segment,cmap='gray')
                # plt.show()
                img_segment = preprocess.denoise(img_segment)
                
                
                # plt.imshow(img_segment,cmap='gray')
                # plt.show()
                cv2.rectangle(img_gray, (x,y), (x+w,y+h), (0, 0, 0), 2)
                data = text_detection.tesseract_text_detector(img_segment)
                data_store.append(data)
                print(data.replace('\n','').replace('\n\n',''))
                # break

            # break
        # print(t)
        print(tx)
        print(ty)
        res = id_card_formation.nid_save(data_store)
        return img_gray,res,data
        # plt.imshow(img_gray,cmap='gray')
        # plt.show()



def main():
    # # img_name = input("Give your image name: ")
    img_name = 'suhel222.jpeg'
    path = 'data/nid/' + img_name
    img_gray,img = nvid_image_process(path)
    img_box,json_res,data = nvid_text_detection(img_gray,img)
    plt.imshow(img_gray,cmap='gray')
    plt.show()
    # test(path)


if __name__ == "__main__": 
    main()

def test(path):
    import numpy as np
    from scipy import signal
    from PIL import Image


    def load_image(path):
        return np.asarray(Image.open(path))/255.0

    def save(path, img):
        tmp = np.asarray(img*255.0, dtype=np.uint8)
        Image.fromarray(tmp).save(path)

    def denoise_image(inp):
        # estimate 'background' color by a median filter
        bg = signal.medfilt(inp, 3)
        save('background.png', bg)

        # compute 'foreground' mask as anything that is significantly darker than
        # the background
        mask = inp < bg - 0.1
        save('foreground_mask.png', mask)

        # return the input value for all pixels in the mask or pure white otherwise
        return np.where(mask, inp, 1.0)


    # inp_path = '../input/train/2.png'
    out_path = 'output.png'

    inp = load_image(path)
    out = denoise_image(inp)

    save(out_path, out)