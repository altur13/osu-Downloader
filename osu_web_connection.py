import requests
import os

from beatmap import *

class OsuWebConnection:
    login_url = "https://osu.ppy.sh/forum/ucp.php?mode=login"

    def __init__(self):
        self.session = requests.Session()
        print("Login:")
        self.login = input()
        print("Password:")
        self.password = input()

    def do_login(self):
        print("Logging in osu! site with user " + self.login + "....")
        r = self.session.post(OsuWebConnection.login_url,
                data={'redirect': '/',
                    'sid': '',
                    'username': self.login,
                    'password': self.password,
                    'login': 'login'})
        #print(r.headers)

    def is_logged(self):
        r = self.session.get(OsuWebConnection.login_url)
        text = r.text
        if "Username:" in text and "Password:" in text and \
           "Log me on automatically each visit" in text and \
           "Hide my online status this session" in text:
            return False
        elif "Announcements (click for more)" in text:
            return True
        return False

    def download_beatmap(self, beatmap, base_path):
        if not self.is_logged():
            self.do_login()

        beatmap_url = "https://osu.ppy.sh/d/" + beatmap.beatmapset_id
        r = self.session.get(beatmap_url, stream=True)

        if r.headers['Content-Type'] != "application/download":
            # beatmap not available
            beatmap.download_status = "NOT AVAILABLE"
            return

        filename_base = beatmap.beatmapset_id + " " + beatmap.artist + " - " + beatmap.title
        filename_temp = filename_base + ".temp"
        filename_final = filename_base + ".osz"
        # beatmap available, download it
        filesize = int(r.headers['Content-Length']) / 1024.0 / 1024.0
        print("Downloading '" + filename_final + "' (%.2f MB)..." % filesize)
        with open(base_path + "/" + filename_temp, 'wb') as f:
            counter = -1
            for chunk in r.iter_content(chunk_size=1023):
                if chunk:
                    f.write(chunk)
                    counter += 1023
                    print(str(int(counter / 1024)) + " bytes |", end='')
        os.rename(base_path + "/" + filename_temp, base_path + "/" + filename_final)
        print("Finished download of '" + filename_final + "'")
        beatmap.download_status = "DOWNLOADED"


    def close(self):
        self.session.close()
