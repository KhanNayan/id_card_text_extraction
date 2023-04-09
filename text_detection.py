import pytesseract

def tesseract_text_detector(image):
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
    custom_config = r'--oem 3 -l eng+ben --psm 6'
    data = pytesseract.image_to_string(image,config=custom_config)
    return data