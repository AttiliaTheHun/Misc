using System.Diagnostics;

namespace Pexeso.Game;

public class Player {
    private static readonly string[] RandomNames = {"Mjr. John Sheppard", "Edward Snowden", "Clarke Kent", "John Reese", "Harold Finch",
        "James Bond", "Adam Sandler", "John Powell", "Hans Zimmer", "Hugo Boss", "Jean Gionno", "Elvis Presley", "Tony Stark", "William Wallace",
        "Jim Carry"};
    public Player(string name) {
        Debug.Assert(name != null && name.Length > 0, "player name null or empty");
        this.Name = name;
    }
    public string Name { get; init; }
    public int Points { get; set; } = 0;

    public static Player[] Players(int numPlayers, bool randomNames) {
        if (randomNames) {
            return RandomPlayers(numPlayers);
        }
        return StandardPlayers(numPlayers);
    }

    private static Player[] StandardPlayers(int numPlayers) {
        Player[] players = new Player[numPlayers];
        for (int i = 0; i < numPlayers; i++) {
            players[i] = new Player($"Player{i+1}");
        }
        return players;
    }

    private static Player[] RandomPlayers(int numPlayers) {
        string[] names = (string[]) RandomNames.Clone();
        names.Shuffle();
        Player[] players = new Player[numPlayers];
        for (int i = 0; i < numPlayers; i++) {
            players[i] = new Player(names[i]);
        }
        return players;
    }
}