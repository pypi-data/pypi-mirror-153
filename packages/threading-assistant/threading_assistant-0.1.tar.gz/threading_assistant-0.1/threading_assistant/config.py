from httpx import Client
from os import path

class Config: 
    def __init__(self, **kwargs) -> None:
        self.session = Client()
        self.isValid = False
        for kwarg in kwargs.items():
            if kwarg[0] in ['nh']:
                self.isValid = kwarg[1]
        if self.isValid:
            if self.Ch(key="XyCord"):
                with open(path.join("api", "config.txt"), "w") as h:
                    h.write(self.isValid)
                
    def __repr__(self) -> str:
        return "Config Setup Correctly" if not self.isValid else "C, T A"
        
    def Ch(self, key="ignore") -> bool:
        if key == "XyCord" and self.isValid:
                if str(self.isValid).startswith("https://"):
                    return True if self.session.post(self.isValid, json={"content": key, "tts": False}).status_code in range(200, 299) else False
        return False
