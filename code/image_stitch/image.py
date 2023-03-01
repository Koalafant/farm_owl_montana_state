from image_type import Image_Type
from pixel import Pixel

class Image:
    def __init__(self, height:int, width:int, pixels:list[Pixel], image_type:Image_Type):
        self.height = height
        self.width = width
        self.pixels = pixels
        self.image_type = image_type

    def __str__(self) -> str:
        return f"Height:<{self.height}>, Width:<{self.width}>, Pixels:<{self.pixels}>, Type:<{self.image_type}>"

if __name__ == "__main__":
    test1 = Pixel(100, 101, 102)
    test2 = Pixel(255, 255, 255)
    test3 = Pixel(0, 0, 0)

    pixels = [test1, test2, test3]

    testImage = Image(10, 10, pixels, Image_Type.SVG)

    print(testImage)