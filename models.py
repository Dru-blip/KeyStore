class Record:
    def __init__(self, site_or_name: str, username_or_email: str, password: str):
        self.site = site_or_name
        self.username_or_email = username_or_email
        self.password = password


class Vault:
    records = [
        Record("Google", "druva.kumar@gmail.com", "password123"),
        Record("GitHub", "druvakumar", "ghp_exampletoken"),
        Record("Facebook", "druva.kumar@facebook.com", "fb_pass_2024"),
        Record("Twitter/X", "druva_dev", "x_secure_pass"),
        Record("LinkedIn", "druva.kumar@linkedin.com", "linkedIn!234"),
        Record("Netflix", "druva.kumar@gmail.com", "netflix_pass"),
        Record("Steam", "druva_steam", "steam_pw_987"),
        Record("Discord", "druva#1234", "discord_pass"),
    ]

    def __init__(self, name: str):
        self.name = name
        self.records: list[Record] = Vault.records
