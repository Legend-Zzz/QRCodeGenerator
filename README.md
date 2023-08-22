Python 3.10
```
usage: QRCodeGenerator.py [-h] [--logo_path LOGO_PATH] [--comment COMMENT] [--font_path FONT_PATH] [--font_size FONT_SIZE] qr_data qr_path

Generate a QR code with optional logo and text.

positional arguments:
  qr_data               二维码内容
  qr_path               二维码存放路径

options:
  -h, --help            show this help message and exit
  --logo_path LOGO_PATH
                        Logo图片路径，可选参数
  --comment COMMENT     二维码嵌入文字内容，可选参数
  --font_path FONT_PATH
                        二维码嵌入文字的字体路径，可选参数
  --font_size FONT_SIZE
                        二维码嵌入文字大小，可选参数
```

QRCode Example

![QRCode](./QRCode.png)
