class Skill:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.exclusive = False
        self.score = 0

    def set_exclusive(self):
        self.exclusive = True

    def increase_score(self):
        self.score+=1

    def __repr__(self):
        return self.name + " / " + self.type + " / " + str(self.score) + "\n"