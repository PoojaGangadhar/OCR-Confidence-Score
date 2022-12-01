import pytesseract
from PIL import Image
import cv2
from flask import request
from pytesseract import Output


# file = r"image1.jpg"


def ocr_ext(filename):
    text = pytesseract.image_to_string(Image.open(filename))
    return text


def confidenceScore(filename):
    score = 0
    count = 0
    # images = cv2.imread(filename)
    images = Image.open(filename)
    # rgb = cv2.cvtColor(images, cv2.COLOR_BGR2RGB)
    results = pytesseract.image_to_data(images, output_type=Output.DICT)
    for i in range(0, len(results["text"])):
        """x = results["left"][i]
        y = results["top"][i]
        w = results["width"][i]
        h = results["height"][i]"""

        text = results["text"][i]
        conf = int(results["conf"][i])

        if conf > 0:
            """print("Confidence: {}".format(conf))
            print("Text: {}".format(text))
            print("")"""
            text = "".join(text).strip()
            score += conf
            count += 1
            """cv2.rectangle(images,
                          (x, y),
                          (x + w, y + h),
                          (0, 0, 255), 2)
            cv2.putText(images,
                        text,
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2, (0, 255, 255), 3)"""

    confidence = score / count
    print("Confidence: ", round(confidence, 2))
    print("Extraction Completed!")

    # data = pytesseract.image_to_string(Image.open(filename))
    # data = pytesseract.image_to_string(images)
    return confidence


"""if __name__ == "__main__":
    ocr_ext(file)
"""
