<h1 align="center">
  <br>
    <img src="https://github.com/EMachad0/YGO-Prog-Web-Front/blob/main/src/assets/logo.png" alt="YGO-Prog-db">
  <br>
    YGO-Progression-Bot
  <br>
</h1>

<h4 align="center">Yu-Gi-Oh, Progression Series, Sealed Draft, Pack Opener, Deck Builder, Bot and Web</h4>

<p align="center">
  <a href="#overview">Overview</a>
  •
  <a href="#contribute">Contribute</a>
  •
  <a href="#user-guide">User Guide</a>
  •
  <a href="#credits">Creditos</a>
  •
  <a href="#license">License</a>
</p>

# Overview

This Project aims to created a Safe Sealed Draft Yu-Gi-Oh format online experience similar to the Yu-Gi-Oh Progression Series.

The project curently is divided into four applications:

* [YGO-Progression-Bot](https://github.com/EMachad0/YGO-Progression-Bot): The star of the project, this bot lets players open-packs and add cards to their collection while the admim configures from which set are those pack from, the amount of packs each player can open and the desired ban-list.

* [YGO-Progression-Web](https://github.com/EMachad0/YGO-Progression-Web): The bulk of the project, built using Vue.js, this site lets players see their collection, build a deck and export it to battle on their prefed Yu-Gi-Oh dueling system.

* [YGO-Progression-Web-Back](https://github.com/EMachad0/YGO-Progression-Web-Back): The Back Bone of the project, this Flask/SQLAlchemy application exposes the card/set/banlist/player database for the site. 

* [YGO-Progression-db](https://github.com/EMachad0/YGO-Progression-db): The less exciting part of the project, scripts for getting and parsing yu-gi-oh data and adding those to the database for the others applications to use.

# Contribute

This project was developed by a single Brazilian CS Student, while I don't expect to live by this project, I do plan to continue improving this for years to come as this is such a passion project and the biggest thing I have ever built.

Hovewer, currently the project has monetary limitations, I can't pay for the servers this project runs on, that's why I need your contribution.

**With the current server there is a limit of 10000 database lines, that's why there are many sets missing and a per server player limit.**
(there exists more cards than database lines).

[Buy me a Ko-fi](https://ko-fi.com/ygoprogressionbot)

# User Guide

To do

# Dev Guide

To do

auto generated project setup
## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

# Credits

Credit where credit is due

Special Thanks for all my friends who helped on the development, specialy [Igor](https://github.com/IgorFroehner), [Joao](https://github.com/joao-frohlich) and [Felipe](https://github.com/Markhyz)

Thanks to [Cimooo](https://www.youtube.com/channel/UCrEMDvUyGV1p66Vf5P0O1pg) for creating the Progression Series and being the inspiration of this project.

Thanks to [YGOPRODECK](https://ygoprodeck.com/) for the great and well documented api.

# license

Released under the [MPL 2.0](https://www.mozilla.org/en-US/MPL/) license.
