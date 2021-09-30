from common.utils import create_csv_headers, append_to_csv
from data import users_path, users_temp_path


class User:

    def __init__(self, name, url, twitter=None, instagram=None):
        self.name = name
        self.url = url
        self.twitter = twitter
        self.instagram = instagram

    def __repr__(self):
        return "User(%s, %s)" % (self.name, self.url)

    def __eq__(self, other):
        if isinstance(other, User):
            return self.name == other.name
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__repr__())

    def save(self):
        if self.instagram or self.twitter:
            create_csv_headers(users_path, "name,url,twitter,instagram")
            new_row = f"{self.name},{self.url},{self.twitter},{self.instagram}"
            append_to_csv(users_path, new_row, False)
        else:
            create_csv_headers(users_temp_path, "name,url")
            new_row = f"{self.name},{self.url}"
            append_to_csv(users_temp_path, new_row, False)
