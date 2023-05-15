
import pytesseract
from PIL import Image
import pyocr
import re

class make_Receipt_Text:
    fPath = ""

    def set_filePath(self, t):
        fPath = t

    def make_Text(self, path):
        pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract"
        pyocr.tesseract.TESSERACT_CMD = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        tools = pyocr.get_available_tools()
        tool = tools[0]

        # image path
        root = r'C:\\Users\\water\\Python\\data\\'
        #image_name = r'IMG_0524.jpeg'

        '''
        # Get bounding box estimates
        # https://pypi.org/project/pytesseract/
        print(pytesseract.image_to_boxes(Image.open(image_path)))

        # Example of adding any additional options
        custom_oem_psm_config = r'--oem 3 --psm 6'
        pytesseract.image_to_string(image, config=custom_oem_psm_config)
        '''

        # 元画像の読み込み
        img_org = Image.open(path)
        img_rgb = img_org.convert("RGB")
        pixels = img_rgb.load()

        # 原稿画像加工（黒っぽい色以外は白=255,255,255にする）
        c_max = 200
        for j in range(img_rgb.size[1]):
            for i in range(img_rgb.size[0]):
                if (pixels[i, j][0] > c_max or pixels[i, j][1] > c_max or
                        pixels[i, j][0] > c_max):
                    pixels[i, j] = (255, 255, 255)

        # 画像のファイル保存
        img_rgb.save(root + r'image_test.png')

        # OCRの実施
        builder = pyocr.builders.TextBuilder(tesseract_layout=6)
        text = tool.image_to_string(img_rgb, lang="jpn", builder=builder)
        
        # 余分なスペースを削除
        text = re.sub(" +", " ", text)

        # 結果のテキストをファイルに保存
        fileobj = open(root + "resutl_OCR.txt", "w")
        fileobj.write(text)
        fileobj.close()

        return text

# テスト。スマホで撮影したレシートのOCRを実施
#text = make_Receipt_Text().make_Text()
#print(text)
