from image_type import Image_Type
from pixel import Pixel

class Image:
    def __init__(self, height:int, width:int, pixels:list[list[Pixel]], image_type:Image_Type):
        self.height = height
        self.width = width
        self.pixels = pixels
        self.image_type = image_type

    def __str__(self) -> str:
        return f"Height:<{self.height}>, Width:<{self.width}>, Pixels:<{self.pixels}>, Type:<{self.image_type}>"

    def getImage(self):
        return self

