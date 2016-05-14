class Beatmap:
    def __init__(self):
        self.beatmapset_id = ""
        self.title = ""
        self.artist = ""
        self.mapper = ""
        self.bpm = ""
        self.status = ""
        self.length = ""
        self.favorites = ""
        self.diff_name = ""
        self.download_status = "NOT DOWNLOADED"

    def build_from_query(self, qdict):
        self.title = qdict['title']
        self.beatmapset_id = qdict['beatmapset_id']
        self.artist = qdict['artist']
        self.mapper = qdict['mapper']
        self.bpm = qdict['bpm']
        self.add_status(qdict['beatmap_status'])
        self.length = qdict['total_length']
        self.favorites = qdict['favorites']
        self.diff_name = qdict['difficulty_name']

    def build_from_file_line(self, export_string):
        fields = export_string.split("||")
        self.beatmapset_id = fields[0]
        self.title = fields[1]
        self.artist = fields[2]
        self.mapper = fields[3]
        self.bpm = fields[4]
        self.status = fields[5]
        self.length = fields[6]
        self.favorites = fields[7]
        self.download_status = fields[8].strip()

    def add_status(self, status):
        if status == 1:
            self.status = "Ranked"
        elif status == 3:
            self.status = "Qualified"
        else:
            self.status = "Unranked"

    def print_info(self):
        print(self.artist + " -- " + self.title + "[" + self.diff_name + "] (by " + self.mapper + ")")
        print("ID: " + str(self.beatmapset_id))
        print("BPM: " + str(self.bpm))
        print("Status: " + self.status)
        print("Length: " + str(int(self.length) // 60) + ":" + str(int(self.length) % 60))
        print("Favorites: " + str(self.favorites))
        print("Download Status: " + self.download_status)

    def export_string(self):
        str_repr = ""
        str_repr += str(self.beatmapset_id)
        str_repr += "||" + self.title + "||" + self.artist + "||" + self.mapper
        str_repr += "||" + str(self.bpm) + "||" + str(self.status) + "||" + str(self.length)
        str_repr += "||" + str(self.favorites) + "||" + self.download_status
        return str_repr
