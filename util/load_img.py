
import imgui
from OpenGL.GL import *
from PIL import Image
import numpy as np

from util.logger import logger


def get_rgba_pixels(image: Image.Image):
    if image.mode == "RGB":
        return image.tobytes("raw", "RGBX")
    else:
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        return image.tobytes("raw", "RGBA")


img_list = {}


def load_img(path: str, s):
    if path not in img_list.keys():
        try:
            img = Image.open(path)
            # img.verify()  # 验证图像文件的完整性
            image_data = get_rgba_pixels(img)
            width, height, depth = np.array(img).shape
            texture = glGenTextures(1)
            img_list.update({path: [texture, width, height]})
            glBindTexture(GL_TEXTURE_2D, texture)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
            glPixelStorei(GL_UNPACK_ROW_LENGTH, 0)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, height, width, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
            img.close()
            logger.info(f"load img: {path} [{width} X {height}]*{s}")
        except Exception as e:
            logger.error(f"load image failed: {str(e)}", exc_info=True)
    texture, width, height = img_list.get(path)
    imgui.image(texture, width * height / width * s, height * width / height * s)
