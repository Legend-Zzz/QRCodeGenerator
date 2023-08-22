import qrcode
from PIL import Image, ImageDraw, ImageFont
import argparse
import os
import logging

class QRCodeGenerator:
    def __init__(self, apk_url, qr_path, logo_path="", comment="", font_path="msyh.ttc", font_size=16):
        self.apk_url = apk_url
        self.qr_path = qr_path
        self.logo_path = logo_path
        self.comment = comment
        self.font_path = font_path
        self.font_size = font_size

    def generate_qr_code(self):
        if not self.apk_url or not self.qr_path:
            logging.error("请提供完整的参数：APK网页地址、二维码存放路径")
            return

        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            qr.add_data(self.apk_url)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="green", back_color="white")

            if self.logo_path and os.path.exists(self.logo_path):
                logo_img = Image.open(self.logo_path)
                logo_img = logo_img.resize((80, 80))
                position = ((qr_img.size[0] - logo_img.size[0]) // 2, (qr_img.size[1] - logo_img.size[1]) // 2)
                qr_img.paste(logo_img, position)
            else:
                logging.warning("未提供Logo图片路径或文件不存在，不添加二维码Logo")

            if self.comment:
                font = ImageFont.truetype(self.font_path, self.font_size)
                draw = ImageDraw.Draw(qr_img)
                text_width, text_height = draw.textsize(self.comment, font)
                x = (qr_img.size[0] - text_width) // 2
                y = (qr_img.height - text_height) - 10
                draw.text((x, y), self.comment, fill="black", font=font)
            else:
                logging.warning("未提供二维码文字，不添加二维码文字")

            qr_img.save(self.qr_path)
            logging.info(f"二维码已保存到 {self.qr_path}")
        except Exception as e:
            logging.error(f"生成二维码时发生错误：{e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a QR code with optional logo and text.")
    parser.add_argument("apk_url", help="APK网页地址")
    parser.add_argument("qr_path", help="二维码存放路径")
    parser.add_argument("--logo", help="Logo图片路径")
    parser.add_argument("--comment", help="二维码文字")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    generator = QRCodeGenerator(args.apk_url, args.qr_path, args.logo, args.comment)
    generator.generate_qr_code()
