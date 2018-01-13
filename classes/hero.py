class Hero:
    def __init__(self, name):
        self.name = name
        self.skills = []

    def add_skill(self, skill):
        self.skills.append(skill)

    def get_score(self):
        return sum(skill.score for skill in self.skills)