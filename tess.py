import pytesseract
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import re


class Tess():
    def __int__(self):
        names = ["1.png", "2.jpg", "3.png"]

        start = "\033[1m"
        end = "\033[0;0m"
        count = 1

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def convert_grayscale(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img

    def threshold(self, img):
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        return img

    def denoise(self, img):
        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        dst = cv2.fastNlMeansDenoisingColored(image_rgb, None, 10, 10, 7, 21)
        return dst

    def get_digits(self, str1):
        c = ""
        for i in str1:
            if i.isdigit():
                c += i
        return c

    # for the UAE national id data extraction\

    def getIdNo(self, string):
        idNoDigitString = ""

        lineSplitString = string.split('\n')
        for line in lineSplitString:
            digitString = self.get_digits(line)
            length = len(str(digitString))
            if length > 14:
                idNoDigitString = digitString
                break

        idNoSplit = idNoDigitString.split('784')
        tempString = str(idNoSplit[1])
        char12 = tempString[0:12]
        idNoString = "784" + char12

        return idNoString

    def getName(self, string):
        name = ""
        lineSplitString = string.split('\n')
        for line in lineSplitString:
            if "Name:" in line:
                lineSplit = line.split('Name: ')
                name = str(lineSplit[1])
                break
        return name

    def scanImage(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        image = cv2.imread("./uploads/temp.png")

        # plt.subplot(121), plt.imshow(image)
        # plt.title('Original Image')
        # plt.show()

        image = self.convert_grayscale(image)
        image = self.threshold(image)
        image = self.denoise(image)

        string = pytesseract.image_to_string(image, lang ='eng+ara')

        # structuring data
        idNo = self.getIdNo(string)
        name = self.getName(string)
        return {
            "Name": name,
            "ID No": idNo,
            "Nationality": "United Arab Emirates"
        }

    # for name in names:
    #     image = cv2.imread("testData/id/" + name)
    #
    #     print("\n\n\n\n\n\n\n\n\t\t\t\t\t\t" + start + "Test Case #" + str(count) + "" + end)
    #
    #     plt.subplot(121), plt.imshow(image)
    #     plt.title('Original Image')
    #     plt.show()
    #
    #     image = convert_grayscale(image)
    #     image = threshold(image)
    #     image = denoise(image)
    #
    #     string = pytesseract.image_to_string(image)
    #
    #     # structuring data
    #
    #     idNo = getIdNo(string)
    #     name = getName(string)
    #     print("Name: " + name)
    #     print("ID No: " + idNo)
    #     print("Nationality: United Arab Emirates")
    #
    #     # print(start+"\n\nOriginal String\n"+end+repr(string))
    #     # print(start+"\n\Python Structured Data\n"+end+string)
    #     # print(start+"\n\nStructured Data\n"+end+"Work In Progress")
    #     count = count + 1
