# Pexeso
## Instalation
You need a .NET installation on the machine, which will allow you to run the by executing
```bash
dotnet run
```
## Game overview
When the title screen opens, you can start playing right away or open the settings. The placeholder values you see when you open the settings are the default settings when you choose to play right away. If the `Apply` button in the settings does not close the window, you need to check your input again (only integers greater than zero are allowed). When you click `Play` in the title screen again, the game will start with the settings that were last applied.

### Players
The player who is at turn is indicated in the game window title. It will either be something like `Player1` or an actual name like `John Doe`. Remember your player name so that you can check your score in the end.

### Gameplay
When a player is at turn he can click on two tiles to uncover them. Tiles that pair up will gain a green background when guessed correctly. When the player uncovers two tiles that do not pair up, the game waits for a mouse click or a keystroke to proceed. If the player uncovered two tiles that do pair up, he can uncover two more.

### Results
The results show the player name and his score, that is, the number of pairs he matched correctly. In single player mode, it is the number of turns it took to pair up all the tiles. The `Rematch` button will start a new game with the same settings, however tiles and player names are generated at random each time.

### Matches
You can choose from several content providers (topics) in the settings. Some want you to match the words to themselves (pair up two tiles that each contains the word `Banana`) and some want you to match words to other words based on some kind of logical relationship (match `Tequila` to `Mexico` if the topic was `Beverages and Spirits`). It should not take long to find out what the game is asking of you.

### Copyrights
The stargate glyphs have been kindly taken from https://rdanderson.com and stripped of their background. As such you are not free to use them unless you get the permission from their author.