import json

class Project(object):

    def __init__(self, name = 'main') -> None:
        self.name                = name
        self.silent              = 0
        self.is_subproject       = 0
        self.cursor_date         = None
        self.logged_found        = 0
        self.cursor_hours        = 0.0
        self.show_stats          = 1
        self.is_hours_line       = 1
        self.endof               = 0
        self.hours_all           = 0.0
        self.hour_rate           = 10
        self.exchange_rate       = 0.0
        self.hours_per_date      = 0.0
        self.paid                = 0.0
        self.periods             = {}
        self.tags                = {}


    def calculate_score(self) -> float:
        return (self.hours_all * self.hour_rate) - self.paid


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
