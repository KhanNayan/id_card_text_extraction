# nid-text-extraction



## Installing Tesseract on obuntu

First check if your machine has already installed the Tessearct.
Run this command to check it:
```
which tesseract
```
If Tesseract exist,this command will show an output like "/usr/bin/tesseract".

If not then, Installed the tesseract with bellow command lines.
```
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```
By default, Tesseract will install the English language pack.For bangla language pack run this command.

```
sudo apt install tesseract-ocr-ben
```
## Requirements 

You need libraries like opencv, numpy,tqdm,pytesseract etc.Run this command to install those library.
```
pip install -r requiremnet.txt
```

