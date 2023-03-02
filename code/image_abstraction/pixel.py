class Pixel:
    def __init__(self, red:int, green:int, blue:int):
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self) -> str:
        return f"R:<{self.red}>, G:<{self.green}>, B:<{self.blue}>"

