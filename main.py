from lxml import html
from lxml import etree
from classes.skill import Skill
from classes.hero import Hero
import requests
import operator

BASE_URL="https://feheroes.gamepedia.com/"
NAME_COL = { 5 : "Weapon",
    6 : "Assist",
    7 : "Special",
    8 : "A",
    9 : "B",
    10 : "C"
}
ATTRIBUTE_ABR = {
    "Res" : "Resistance",
    "Def" : "Defense",
    "Atk" : "Attack",
    "Spd" : "Speed"
}

skills = {}
heroes = []

def add_exclusive_skill(page):
    tree = html.fromstring(page.content)
    for skill in tree.xpath("//div[@class='mw-category-generated']//a/text()"):
        skill_name = skill.split("(")[0].strip()
        if skill_name in skills:
            skills[skill_name].set_exclusive()

def get_exclusive_passives():
    page = requests.get(BASE_URL + "Category:Exclusive_Passives")
    add_exclusive_skill(page)

def get_legendary_weapons():
    page = requests.get(BASE_URL + "Category:Legendary_Weapons")
    add_exclusive_skill(page)

def get_or_create_skill(hero_line, number):
    skill_name = hero_line.xpath("td[" + str(number) + "]/a/text()")
    if not skill_name:
        return
    skill_name = skill_name[0]
    if skill_name in skills:
        skill = skills[skill_name]
    else :
        skill = Skill(skill_name, NAME_COL[number])
        skills[skill_name] = skill
    return skill

def try_finding_skill(skill_name):
    # handling the fact that some skill are not properly capitalized in the build section
    return_skill_name = skill_name[:1].upper() + skill_name[1:]
    if not skill_name in skills:
        #Handling builds using only the 2nd level version of another one.
        if return_skill_name.replace("2", "3") in skills:
            return_skill_name = return_skill_name.replace("2", "3")
        # Handling builds using only the nonplussed version of a weapon.
        elif return_skill_name + "+" in skills:
            return_skill_name += "+"
        else:
            temp_skill = return_skill_name
            unknown_skill = True
            # Handling skill using an attribute abreviation instead of the full name
            for attribute in ATTRIBUTE_ABR:
                temp_skill = temp_skill.replace(attribute, ATTRIBUTE_ABR[attribute])
            if temp_skill in skills:
                unknown_skill = False
                return_skill_name = temp_skill
            temp_skill = return_skill_name
            # Handling skill using an attribute full name instead of the abreviation
            for attribute in ATTRIBUTE_ABR:
                temp_skill = temp_skill.replace(ATTRIBUTE_ABR[attribute], attribute)
            if unknown_skill and temp_skill in skills:
                unknown_skill = False
                return_skill_name = temp_skill
            # All the other case (level 1 skill, skill not properly named, weapon evolutions)
            if unknown_skill:
                skill = Skill(return_skill_name, "?")
                skills[return_skill_name] = skill
    return skills[return_skill_name]

def get_skills(tree, is_curated):
    if is_curated:
        path = "//div[@class='curated-builds']"
    else :
        path = "//div[@class='user-builds']"
    path += "//div[@class='skillbuild-section']/div[position() >=1 and position() <4]//a/text()"
    for skill_name in tree.xpath(path):
        try_finding_skill(skill_name).increase_score(is_curated)

def browse_hero_builds(hero_name):
    page = requests.get(BASE_URL + hero_name + "/Builds")
    tree = html.fromstring(page.content)
    get_skills(tree, True)
    get_skills(tree, False)

def init_skill_and_hero():
    page = requests.get(BASE_URL + "Skills_Table")
    tree = html.fromstring(page.content)
    for hero_line in tree.xpath("//table[@id='max-stats-table']/tr"):
        hero_link = hero_line.xpath("td[1]/a/@href")[0][1:]
        if hero_link:
            hero = Hero(hero_link)
            heroes.append(hero)
            for i in range(5,11):
                skill = get_or_create_skill(hero_line, i)
                if skill:
                    hero.add_skill(skill)

def print_hero_file(is_curated):
    filename = "heroes.txt"
    if is_curated:
        filename = "curated_" + filename
    with open(filename, 'w') as f:
        heroes.sort(key=lambda hero : hero.get_score(is_curated))
        for hero in heroes:
            print(hero.pretty_hero_string(is_curated), file=f)

def print_skill_file():
    with open("skills.txt", 'w') as f:
        print(sorted(skills.values(), key=operator.attrgetter("score")), file=f)

def main():
    init_skill_and_hero()
    get_exclusive_passives()
    get_legendary_weapons()
    for hero in heroes:
        browse_hero_builds(hero.name)
    print_hero_file(True)
    print_hero_file(False)
    print_skill_file()

if __name__ == "__main__":
    main()