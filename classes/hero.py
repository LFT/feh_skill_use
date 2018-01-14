class Hero:
    def __init__(self, name):
        self.name = name
        self.skills = []

    def add_skill(self, skill):
        self.skills.append(skill)

    def get_score(self, is_curated):
        if is_curated:
            return sum(skill.curated_score for skill in self.skills)
        else:
            return sum(skill.score for skill in self.skills)

    def has_exclusive_skil(self)
        for skill in self.skills:
            if skill.exclusive:
                return True
        return False

    def pretty_hero_string(self, is_curated):
        return_string = self.name + " : " + str(self.get_score(is_curated))
        if self.has_exclusive_skil():
            return_string += " (Hero has exclusive skill/weapon)"
        return return_string

    def __repr__(self):
        return self.name