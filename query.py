class OsuSearchQuery:
    # ignored parameters
    date_start = ""
    date_end = ""
    min_favorites = ""
    max_favorites = ""
    min_play_count = ""
    max_play_count = ""
    min_bpm = ""
    max_bpm = ""

    def __init__(self):
        self.query_dict = {}
        self.query_dict['genres'] = []
        self.query_dict['languages'] = []
        self.query_dict['modes'] = []
        self.query_dict['statuses'] = []

    def set_title(self, title):
        self.query_dict['title'] = title

    def set_artist(self, artist):
        self.query_dict['artist'] = artist

    def set_source(self, source):
        self.query_dict['source'] = source

    def set_mapper(self, mapper):
        self.query_dict['mapper'] = mapper

    def set_diff_name(self, diff_name):
        self.query_dict['diff_name'] = diff_name
    
    def set_min_length(self, min_length):
        self.query_dict['min_length'] = min_length

    def set_max_length(self, max_length):
        self.query_dict['max_length'] = max_length

    def add_genre(self, genre):
        self.query_dict['genres'].append(genre)

    def add_language(self, language):
        self.query_dict['languages'].append(language)

    def add_mode(self, mode):
        self.query_dict['modes'].append(mode)

    def add_status(self, status):
        self.query_dict['statuses'].append(status)

    def set_star_range(self, min_star="0.00", max_star="10.00"):
        self.query_dict['star'] = "(" + min_star + "," + max_star + ")"

    def set_ar_range(self, min_ar="0.00", max_ar="10.00"):
        self.query_dict['ar'] = "(" + min_ar + "," + max_ar + ")"

    def set_od_range(self, min_od="0.00", max_od="10.00"):
        self.query_dict['od'] = "(" + min_od + "," + max_od + ")"

    def set_cs_range(self, min_cs="0.00", max_cs="10.00"):
        self.query_dict['cs'] = "(" + min_cs + "," + max_cs + ")"

    def set_hp_range(self, min_hp="0.00", max_hp="10.00"):
        self.query_dict['hp'] = "(" + min_hp + "," + max_hp + ")"

    def set_query_order(self, order="favorites"):
        self.query_dict['query_order'] = order

    def get_query_string(self):
        url = "http://osusearch.com/query/?"
        for key, value in self.query_dict.items():
            if isinstance(value, list) and not value:
                continue

            url += key + "="
            if isinstance(value, list) and value:
                url += value[0]
                for i in value[1:]:
                    url += "," + i
            else:
                url += value
            url += "&"
        return url
