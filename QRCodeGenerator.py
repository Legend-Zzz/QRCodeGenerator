import qrcode
from PIL import Image, ImageDraw, ImageFont
import argparse
import os
import logging


class QRCodeGenerator:
    def __init__(self, qr_data, qr_path, logo_path=None, comment=None, font_path=None, font_size=16):
        self.qr_data = qr_data
        self.qr_path = qr_path
        self.logo_path = logo_path
        self.comment = comment
        self.font_path = font_path
        self.font_size = font_size
        self.DEFAULT_LOGO_SIZE = (80, 80)
        self.LOGO_POSITION_OFFSET = 10

    def _add_logo(self, qr_img):
        if self.logo_path and os.path.isfile(self.logo_path):
            logo_img = Image.open(self.logo_path)
            logo_img = logo_img.resize(self.DEFAULT_LOGO_SIZE)
            position = ((qr_img.size[0] - logo_img.size[0]) // 2, (qr_img.size[1] - logo_img.size[1]) // 2)
            qr_img.paste(logo_img, position)
            return qr_img
        else:
            logging.warning("未提供Logo图片路径或文件不存在，不添加二维码Logo")
            return qr_img

    def _add_comment(self, qr_img):
        if self.comment:
            font_path = self.font_path
            if font_path and os.path.isfile(font_path):
                font = ImageFont.truetype(font_path, self.font_size)
            else:
                logging.warning("未提供字体文件路径或文件不存在，使用默认字体")
                font = ImageFont.load_default()

            draw = ImageDraw.Draw(qr_img)
            text_width, text_height = draw.textsize(self.comment, font)
            x = (qr_img.size[0] - text_width) // 2
            y = (qr_img.height - text_height) - self.LOGO_POSITION_OFFSET
            draw.text((x, y), self.comment, fill="black", font=font)

    def generate_qr_code(self):
        if not self.qr_data or not self.qr_path:
            logging.error("请提供完整的参数：二维码内容、二维码存放路径")
            return

        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            qr.add_data(self.qr_data)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="green", back_color="white")

            qr_img = self._add_logo(qr_img)
            self._add_comment(qr_img)

            qr_img.save(self.qr_path)
            logging.info(f"二维码已保存到 {self.qr_path}")
        except Exception as e:
            logging.error(f"生成二维码时发生错误：{e}")


def parse_args():
    parser = argparse.ArgumentParser(description="Generate a QR code with optional logo and text.")
    parser.add_argument("qr_data", help="二维码内容")
    parser.add_argument("qr_path", help="二维码存放路径")
    parser.add_argument("--logo_path", default=None, help="Logo图片路径，可选参数")
    parser.add_argument("--comment", default=None, help="二维码嵌入文字内容，可选参数")
    parser.add_argument("--font_path", default=None, help="二维码嵌入文字的字体路径，可选参数")
    parser.add_argument("--font_size", type=int, default=16, help="二维码嵌入文字大小，可选参数")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    generator = QRCodeGenerator(
        args.qr_data,
        args.qr_path,
        args.logo_path,
        args.comment,
        args.font_path,
        args.font_size
    )
    generator.generate_qr_code()
