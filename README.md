<h1 align="center">
  <br>
    <img src="https://github.com/EMachad0/YGO-Prog-Web-Front/blob/main/src/assets/logo.png" alt="" width="75%">
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
  <a href="#credits">Credits</a>
  •
  <a href="#license">License</a>
</p>

# Overview

This Project aims to create a Safe Sealed Draft Yu-Gi-Oh format online experience similar to the Yu-Gi-Oh Progression Series.

The project currently is divided into four applications:

* [YGO-Progression-Bot](https://github.com/EMachad0/YGO-Progression-Bot): The star of the project, this bot lets players open-packs and add cards to their collection while the admin configures from which set are those pack from, the amount of packs each player can open, and the desired ban-list.

* [YGO-Progression-Web](https://github.com/EMachad0/YGO-Progression-Web): The bulk of the project, built using Vue.js, this site lets players see their collection, build a deck and export it to battle on their preferred Yu-Gi-Oh dueling system.

* [YGO-Progression-Web-Back](https://github.com/EMachad0/YGO-Progression-Web-Back): The Backbone of the project, this Flask/SQLAlchemy application exposes the card/set/banlist/player database to the site. 

* [YGO-Progression-db](https://github.com/EMachad0/YGO-Progression-db): The less exciting part of the project, scripts for getting and parsing yu-gi-oh data and adding those to the database for the others applications to use.

# Contribute

This project was develop by a single Brazilian CS Student, while I don't expect to live by this project, I do plan to continue improving this for years to come as this is such a passion project and the biggest thing I have ever built.

However, currently the project has monetary limitations, I can't pay for the servers this project runs on, that's why I need your contribution.

**With the current server there is a limit of 10000 database lines, that's why there are many sets missing and a per server player limit.**
(Currently only the first 5 sets are available) (there exists more cards than database lines).

<h1 align="center">
    <a href="https://ko-fi.com/ygoprogressionbot">
      <img src="https://i.imgur.com/R2F5Os9.png" alt="[Buy me a Ko-fi]">
    </a>
</h1>

You can also contribute by opening issues if you found any problem. Any pull request welcome.

Any questions? You can contact me on this [Discord](https://discord.gg/ztj2kSk) Server.

# User Guide

## Bot

First, Add the [Bot](https://discord.com/api/oauth2/authorize?client_id=859241519781642251&permissions=59456&scope=bot) to your server!

https://discord.com/api/oauth2/authorize?client_id=859241519781642251&permissions=59456&scope=bot

As admin, configure which channels the bot has access to then send the following message:
```
$new_game
```
This will register a game in your server.

at any point you can finish the game with following command:
```
$end_game
```
Beware, sending *end_game* deletes **all** data, including player's collection. 

Now every player who wants to participate can join with: 
```
$enter
```

And players can open packs with the *pack* command,
```
$pack 7
```
Here the 7 is the number of packs to open, passing no number will open only 1 pack.

This can take a while depending on the amount of cached images the bot has, however the bot will respond with *"Opening..."* to ensure you it's working correctly.

Also, the bot tries to reduce the amount of flooding by grouping maximum 5 packs per image.

After running the command, all shown cards will be automatically be added into the player collection.

However, to open packs, players need to have available packs.

A player can see their available packs and collection url using:
```
$status
```

The admin needs to distribute packs to the players, using *give_pack* and the set code:
```
$give_pack LOB
```
Here *LOB* is the code for *Legend of Blue Eyes*, you can easily find set cods by searching the sets in [Yugipedia](yugipedia.com).
If needed, the command supports an arbitrary number of usernames, so you can give specific packs to specific players:
```
$give_pack LOB @player1 @player2
```

The command *give_card* has yet to be implemented.

Any questions? You can contact me on this [Discord](https://discord.gg/ztj2kSk) Server.

### Bot Screenshot:
<h1 align="center">
    <img src="/screenshots/discord_screenshot.png" alt="" width="30%">
</h1>

### Configs

Configs are keywords to make so the admin can customize the game and implement the format he considers the best, like so:
```
$config ban_list May 2002
```
Here, *ban_list* is the key while *May 2002* is the value, this command is setting the server banlist to the [May 2002](https://yugipedia.com/wiki/May_2002_Lists_(TCG)) lists.

Supported configs for now:
|Key         |Supported Values                    |Info                                                  |Default Behavior               |
|------------|------------------------------------|------------------------------------------------------|-------------------------------|
|ban_list    |"Month Year" of any official banlist|Let admin set the deck builder banlist                |No ban list                    |
|private_pack|"False"                             |*$pack* response is sent on the channel of the command|*$pack* response is sent via DM|

Passing an invalid key will do nothing while passing a invalid value will change the key to it's default behavior.

## Web

The Site will display only your entire collection, you can't add cards you haven't pull and those won't appear if you search for then.

Also, the cards may take a while to load depending on the size of your collection, don't panic if it looks stuck.

Use the fields and Options to filter/sort, and you can Drag/Drop or Right Click on cards to add/remove then from deck.

That is it, there is no magic here, the ui should be intuitive enough, but you can message me any questions.

Any questions? You can contact me on this [Discord](https://discord.gg/ztj2kSk) Server.

### Web Screenshot:
<h1 align="center" float="left">
    <img src="/screenshots/collection_screenshot.png" alt="" width="45%">
    <img src="/screenshots/deck_builder_screenshot.png" alt="" width="45%">
</h1>

# Dev Guide

(to do)

Any questions? You can contact me on this [Discord](https://discord.gg/ztj2kSk) Server.

# Credits

Credit where credit is due

Special Thanks for all my friends who helped on the development, specially [Igor](https://github.com/IgorFroehner), [Joao](https://github.com/joao-frohlich) and [Felipe](https://github.com/Markhyz).

Thanks to [Cimooo](https://www.youtube.com/channel/UCrEMDvUyGV1p66Vf5P0O1pg) for creating the Progression Series and being the inspiration of this project.

Thanks to [YGOPRODECK](https://ygoprodeck.com/) for the great and well documented api.

# license

Released under the [MPL 2.0](https://www.mozilla.org/en-US/MPL/) license.
