Allow to create/refresh the list of skill used by builds referenced in https://feheroes.gamepedia.com/Main_Page . Following that a note is given to heroes (the lower the score, the less used its skills are).

Current output are present in [heroes.txt](https://github.com/LFT/feh_skill_use/blob/master/heroes.txt) and [curated_heroes.txt](https://github.com/LFT/feh_skill_use/blob/master/curated_heroes.txt) for the heroes and in [skills.txt](https://github.com/LFT/feh_skill_use/blob/master/skills.txt) for the skills.

Each skill scores one point when it's used. And each hero has a score equals to the sum of its skills score
It can generate a score for all the builds and only curated builds.

Built using python3 and lxml.

The results are licensed under [CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/)

The code is licensed under [MIT License](https://opensource.org/licenses/MIT)
