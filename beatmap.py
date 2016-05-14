class Beatmap:
    beatmap_id = ""
    title = ""
    artist = ""
    mapper = ""
    bpm = ""
    status = ""
    length = ""
    favorites = ""
    diff_name = ""
    download_status = "NOT DOWNLOADED"

    def __init__(self):
        pass

    def self_build(export_string):
        fields = export_string.split("||")
        self.beatmap_id = fields[0]
        self.title = fields[1]
        self.artist = fields[2]
        self.mapper = fields[3]
        self.bpm = fields[4]
        self.status = fields[5]
        self.length = fields[6]
        self.favorites = fields[7]
        self.download_status = fields[8]

    def add_status(self, status):
        if status == 1:
            self.status = "Ranked"
        elif status == 3:
            self.status = "Qualified"
        else:
            self.status = "Unranked"

    def print_info(self):
        print(self.artist + " -- " + self.title + "[" + self.diff_name + "] (by " + self.mapper + ")")
        print("ID: " + str(self.beatmap_id))
        print("BPM: " + str(self.bpm))
        print("Status: " + self.status)
        print("Length: " + str(self.length // 60) + ":" + str(self.length % 60))
        print("Favorites: " + str(self.favorites))
        print("Download Status: " + self.download_status)

    def export_string(self):
        str_repr = ""
        str_repr += str(self.beatmap_id)
        str_repr += "||" + self.title + "||" + self.artist + "||" + self.mapper
        str_repr += "||" + str(self.bpm) + "||" + str(self.status) + "||" + str(self.length)
        str_repr += "||" + str(self.favorites) + "||" + self.download_status
        return str_repr
