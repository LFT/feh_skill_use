class Hero:
    def __init__(self, name):
        self.name = name
        self.skills = []

    def add_skill(self, skill):
        self.skills.append(skill)

    def get_score(self):
        return sum(skill.score for skill in self.skills)

    def __repr__(self):
        return self.name + " : " + str(self.get_score()) + "\n"