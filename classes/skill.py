import operator

class Skill:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.exclusive = False
        self.score = 0
        self.curated_score = 0
        self.usage_by = {}
        self.curated_usage_by = {}

    def set_exclusive(self):
        self.exclusive = True

    def increase_hero_usage(self, hero_name, is_curated):
        attr_name = "usage_by"
        if is_curated:
            attr_name = "curated_usage_by"
        hero_dict = getattr(self, attr_name)
        if hero_name in hero_dict:
            hero_dict[hero_name] += 1
        else:
            hero_dict[hero_name] = 1

    def increase_score(self, is_curated):
        self.score+=1
        if is_curated:
            self.curated_score+=1

    def pretty_print(self):
        return_string = self.name.ljust(20) + " -- " +  str(self.score).ljust(2) + "( " + str(self.curated_score).ljust(2) + " ) /\ "
        for hero in sorted(self.usage_by.items(), key=operator.itemgetter(1), reverse=True):
            return_string += hero[0] + " : " + str(hero[1])
            if hero[0] in self.curated_usage_by :
                return_string += " ("  + str(self.curated_usage_by[hero[0]]) + ")"
            return_string +=  ", "
        return return_string

    def __repr__(self):
        return self.name + " / " + self.type + " / score : " + str(self.score) + " / curated score: " + str(self.curated_score) +"\n"