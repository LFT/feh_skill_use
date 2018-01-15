class Skill:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.exclusive = False
        self.score = 0
        self.curated_score = 0

    def set_exclusive(self):
        self.exclusive = True

    def increase_score(self, is_curated):
        self.score+=1
        if is_curated:
            self.curated_score+=1

    def __repr__(self):
        return self.name + " / " + self.type + " / score : " + str(self.score) + " / curated score: " + str(self.curated_score) +"\n"