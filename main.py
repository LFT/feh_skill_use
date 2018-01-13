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
        skills[skill].set_exclusive()

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

def browse_hero_curated_build(hero_name):
    page = requests.get(BASE_URL + hero_name + "/Builds")
    tree = html.fromstring(page.content)
    path = ""
    if USE_ONLY_CURATED:
        path = "//div[@class='curated-builds']"
    path += "//div[@class='skillbuild-section']/div[position() >=1 and position() <4]//a/text()"

    print(tree.xpath(path))

def init_skill_and_hero():
    page = requests.get(BASE_URL + "Skills_Table")
    tree = html.fromstring(page.content)
    for hero_line in tree.xpath("//table[@id='max-stats-table']/tr"):
        hero_link = hero_line.xpath("td[1]/a/@href")[1:]
        hero = Hero(hero_link)
        heroes.append(hero)
        for i in range(5,11):
            hero.add_skill(get_or_create_skill(hero_line, i))
    #print(tree.xpath("//table[@id='max-stats-table']/tr")).replace("\n","").replace("\t","")

    #hero_line = tree.xpath("//table[@id='max-stats-table']/tr")[0]
    #with open('out.txt', 'w') as f:
    #    print(page.content, file=f)
    #print(hero_line[0].)
    #for elem in hero_line:
    #    print(etree.tostring(elem, pretty_print=True))
     # pretty_print ensures that it is nicely formatted.
    #print(etree.tostring(hero_line, pretty_print=True))
    #print()
    #print(hero_line.xpath("td[2]/a/text()"))

def main():
    #init_skill_and_hero()
    #get_exclusive_passives()
    #get_legendary_weapons()
    browse_hero_curated_build("Abel")

if __name__ == "__main__":
    main()