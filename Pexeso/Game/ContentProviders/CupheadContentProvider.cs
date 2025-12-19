namespace Pexeso.Game.ContentProviders;

public class CupheadContentProvider : IContentProvider {
    private string[] content = {
        "The Root Pack:Botanic Panic", "Goopy Le Grande:Ruse of an Ooze", "Ribby and Croaks:Clip Joint Calamity", "Cagney Carnation:Floral Fury",
        "Hilda Berg:Threatenin' Zeppelin", "Baroness Von Bon Bon:Sugarland Shimmy", "Djimmi the Great:Pyramid Peril", "Beppi the Clown:Carnival Kerfuffle",
        "Grim Matchstick:Fiery Frolic", "Wally Warbles:Aviary Action", "Captain Brineybeard:Shootin N' Lootin", "Sally Stageplay:Dramatic Fanatic",
        "Werner Werman:Murine Corps", "Dr. Kahl's Robot:Junkyard Jive", "Cala Maria:High Seas Hi-Jinx", "Phantom Express:Railroad Wrath",
        "King Dice:All Bets Are Off", "The Devil:One Hell of a Time", "Pip and Dot:Domino Duel", "Mangosteen:Eight-Ball Boogie", "Mr. Chimes:Monkey See, Monkey Doom!",
        "Chips Bettigan:Betting Boss", "Mr. Wheezy:Cigarette Scuffle", "Hopus Pocus:Rabbit Rumble", "Phear Lap:Skeletal Steed", "Pirouletta:Roulette Rampage",
        "The Tipsy Troop:Alcohol Antics", "Mortimer Freeze:Snow Cult Scuffle", "Glumstone the Giant:Gnome Way Out", "Moonshine Mob:Bootlegger Boogie",
        "Esther Winchester:High Noon Hoopla", "Chef Saltbaker:A Dish to Die For", "The Pawns:Pawn Off", "The Knight:A King's Knightmare",
        "The Bishop:Bishop Brawl", "The Rook:Rook Rampage", "The Queen:Checkmate Champion"
    };

    public Pair[] GetPairs(int number) {
        string[] shuffled = (string[]) content.Clone();
        shuffled.Shuffle();
        Pair[] pairs = new Pair[number];
        int contentIndex = 0;
        for (int i = 0; i < number; i++) {
            string[] words = content[i].Split(":");
            pairs[i] = new Pair(words[0], words[1]);
            contentIndex++;
        }
        return pairs;
    }
}