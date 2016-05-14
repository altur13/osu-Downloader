import requests

class OsuWebConnection:
    login_url = "https://osu.ppy.sh/forum/ucp.php?mode=login"
    session = None

    def __init__(self, login, password):
        self.session = requests.Session()
        print("Logging in osu! site with user " + login + "....")
        r = self.session.post(login_url,
                data={'redirect': '/',
                    'sid': '',
                    'username': login,
                    'password': password,
                    'login': 'login'})
        print(r.headers)

    def download_beatmap(self, url, file_path):
        r = self.session.get(url, stream=True)
        with open(file_path, 'wb') as f:
            counter = -1
            for chunk in r.iter_content(chunk_size=1023):
                if chunk:
                    f.write(chunk)
                    counter += 1023
                    print("Downloaded: " + str(counter) + " kb")

    def close(self):
        self.session.close()
