# -----Imports------
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt


class Conversor:
    """class to convert a RGB to HSI"""

    def __init__(self, img):
        """constructor"""
        self.img = img.copy()
        self.height, self.width, chanels = self.img.shape
        self.red = np.uint16(self.img[:, :, 0])
        self.gre = np.uint16(self.img[:, :, 1])
        self.blu = np.uint16(self.img[:, :, 2])

        division = self.red + self.blu + self.gre
        self.norm_red = self.red / division
        self.norm_gre = self.gre / division
        self.norm_blu = self.blu / division
        self.calc_hsi()

    @staticmethod
    def Hsi(norm_red, norm_gre, norm_blu, red, blu, gre):
        """define h depending of b>g or not
        define s and i"""

        numerator = 0.5 * ((norm_red - norm_gre) + (norm_red - norm_blu))

        denominator = (
            (norm_red - norm_gre) ** 2 + (norm_red - norm_blu) * (norm_gre - norm_blu)
        ) ** 0.5
        s = 1 - (3 * np.minimum(norm_red, np.minimum(norm_gre, norm_blu)))
        if denominator > 0:
            h = np.arccos(numerator / denominator)
        else:
            h = 0
        i = (red + blu + gre) / (3 * 255)

        if norm_blu > norm_gre:
            h = 2 * np.pi - h
        return (h, s, i)

    def calc_hsi(self):
        """just call the Hsi function and place zero in NaN H values"""
        vect_func_hsi = np.vectorize(self.Hsi)

        self.h, self.s, self.i = vect_func_hsi(
            self.norm_red, self.norm_gre, self.norm_blu, self.red, self.blu, self.gre
        )
        self.h[np.isnan(self.h)] = 0

    @staticmethod
    def convert_normHsi_to_hsi(red, gre, blu, h, s, i):
        h = h * 180 / np.pi
        s = s * 100
        i = (red + gre + blu) / 3
        return (h, s, i)

    # def convert_normHsi_to_hsi(red, gre, blu, h, s, i):
    #     h = h * 180 / np.pi
    #     s = s * 100
    #     i = i * 255  # correção aqui
    #     h = np.where(h < 0, h + 360, h)  # correção aqui
    #     return (h, s, i)

    def normHsi_to_hsi(self):
        vect_func_hsi = np.vectorize(self.convert_normHsi_to_hsi)
        self.h, self.s, self.i = vect_func_hsi(
            self.red, self.gre, self.blu, self.h, self.s, self.i
        )
        self.h = np.round(self.h)
        self.s = np.round(self.s)
        self.i = np.round(self.i)
        img_cpy = np.uint16(self.img.copy())
        img_cpy[:, :, 0] = self.h
        img_cpy[:, :, 1] = self.s
        img_cpy[:, :, 2] = self.i
        return img_cpy

    @staticmethod
    def rgb_to_cmy(norm_red, norm_gre, norm_blu):
        c = 1 - norm_red
        m = 1 - norm_gre
        y = 1 - norm_blu
        return (c, m, y)

    def convert_rgb_to_cmy(self, image=None):
        """Convert an RGB image to CMY"""
        vect_func_cmy = np.vectorize(self.rgb_to_cmy)
        if image is None:
            self.c, self.m, self.y = vect_func_cmy(
                self.norm_red, self.norm_gre, self.norm_blu
            )
            img = np.float16(self.img.copy())
            img[:, :, 0] = self.c
            img[:, :, 1] = self.m
            img[:, :, 2] = self.y
        else:
            division = image[:, :, 0] + image[:, :, 1] + image[:, :, 2]
            norm_red = image[:, :, 0] / division
            norm_gre = image[:, :, 1] / division
            norm_blu = image[:, :, 2] / division
            c, m, y = vect_func_cmy(norm_red, norm_gre, norm_blu)
            img = np.float16(image.copy())
            img[:, :, 0] = c
            img[:, :, 1] = m
            img[:, :, 2] = y
        img = img * 255
        img = np.round(img)
        return img

    @staticmethod
    def to_gray(r, g, b):
        gray = int(0.299 * r + 0.587 * g + 0.114 * b)
        return gray

    def conver_rgb_to_gray(self):
        vect_func_gray = np.vectorize(self.to_gray)
        # gray =
        img_gray = np.zeros((self.height, self.width), dtype=np.uint8)
        img_gray = vect_func_gray(self.red, self.gre, self.blu)
        return img_gray

    def equalize(self, img):
        image = img
        hist, bins = np.histogram(image.flatten(), 256, [0, 256])
        hist_norm = hist / float(image.size)
        cdf = np.zeros_like(hist_norm)
        cdf[0] = hist_norm[0]
        for i in range(1, 256):
            cdf[i] = cdf[i - 1] + hist_norm[i]
        cdf_norm = cdf * 255
        norm_img = (
            np.interp(image.flatten(), bins[:-1], cdf_norm)
            .reshape(image.shape)
            .astype(np.uint8)
        )
        return norm_img

    @staticmethod
    def convert_hsi_to_rgb(h, s, i):
        """
        Convert HSI (Hue, Saturation, Intensity) color representation to RGB color representation.

        Args:
        - h (float): Hue value in degrees, ranging from 0 to 360.
        - s (float): Saturation value, ranging from 0 to 100.
        - i (float): Intensity value, ranging from 0 to 255.

        Returns:
        - Tuple of RGB values ranging from 0 to 255.
        """

        # Normalize saturation and intensity values
        s = s / 100
        i = i / 255

        # Convert hue to radians
        h = h * np.pi / 180

        # Calculate intermediate values based on hue
        if h < 2 * np.pi / 3:
            b = i * (1 - s)
            r = i * (1 + s * np.cos(h) / np.cos(np.pi / 3 - h))
            g = 3 * i - (r + b)
        elif h < 4 * np.pi / 3:
            h = h - 2 * np.pi / 3
            r = i * (1 - s)
            g = i * (1 + s * np.cos(h) / np.cos(np.pi / 3 - h))
            b = 3 * i - (r + g)
        else:
            h = h - 4 * np.pi / 3
            g = i * (1 - s)
            b = i * (1 + s * np.cos(h) / np.cos(np.pi / 3 - h))
            r = 3 * i - (g + b)

        # Convert RGB values to [0, 255] range
        r = int(round(r * 255))
        g = int(round(g * 255))
        b = int(round(b * 255))

        return (r, g, b)

    def hsi_to_rgb(self, img):
        vect_func_hsi2rgb = np.vectorize(self.convert_hsi_to_rgb)
        # print(img)
        img_cpy = np.uint16(img.copy())
        img_cpy[:, :, 0], img_cpy[:, :, 1], img_cpy[:, :, 2] = vect_func_hsi2rgb(
            img[:, :, 0], img[:, :, 1], img[:, :, 2]
        )
        img_cpy = np.uint8(img_cpy)
        # print("------------")
        # print(img)
        return img_cpy


if __name__ == "__main__":
    image = Image.open("./images/lena.png").resize((500, 500))
    image = image.convert("RGB")
    imgNumpy = np.array(image)
    conversor = Conversor(imgNumpy)
    img_gray = conversor.conver_rgb_to_gray()
    plt.imshow(img_gray, cmap="gray")
    plt.show()
