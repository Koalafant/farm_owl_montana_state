class Camera_Driver:
    def __init__(self, standby):
        self.standby = standby

    def snap(self, iso: float, shutter: float, name: str) -> int:
        pass

    def ret_imgs(self, names: list[str]):
        pass

    def check_standby(self):
        pass

    def send_finished(self) -> int:
        pass
