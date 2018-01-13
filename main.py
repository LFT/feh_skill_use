from lxml import html
from lxml import etree
from classes.skill import Skill
from classes.hero import Hero
import requests

BASE_URL="https://feheroes.gamepedia.com/"
NAME_COL = { 5 : "Weapon",
    6 : "Assist",
    7 : "Special",
    8 : "A",
    9 : "B",
    10 : "C"
}
USE_ONLY_CURATED = False

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

def browse_hero_builds(hero_name):
    page = requests.get(BASE_URL + hero_name + "/Builds")
    tree = html.fromstring(page.content)
    path = ""
    if USE_ONLY_CURATED:
        path = "//div[@class='curated-builds']"
    path += "//div[@class='skillbuild-section']/div[position() >=1 and position() <4]//a/text()"
    for skill_name in tree.xpath(path):
        if skill_name in skills:
            skills[skill_name].increase_score()
        else:
            skill = Skill(skill_name, "?")
            skill.increase_score()
            skills[skill_name] = skill

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

def main():
    init_skill_and_hero()
    get_exclusive_passives()
    get_legendary_weapons()
    for hero in heroes:
        browse_hero_builds(hero.name)
    heroes.sort(key=lambda hero : hero.get_score())
    with open('out.txt', 'w') as f:
        print(heroes, file=f)


if __name__ == "__main__":
    main()