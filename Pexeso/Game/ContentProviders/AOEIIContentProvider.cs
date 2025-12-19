namespace Pexeso.Game.ContentProviders;

using System;

public class AOEIIContentProvider : IContentProvider {
    private string[] content = {
        "Britons:Longbowman", "Franks:Throwing Axeman", "Goths:Huskarl", "Teutons:Teutonic Knight", "Japanese:Samurai",
        "Chinese:Chu Ko Nu", "Byzantines:Cataphract", "Persians:War Elephant", "Saracens:Mameluke", "Turks:Janissary",
        "Mongols:Mangudai", "Celts:Woad Raider", "Spanish:Conquistador", "Koreans:War Wagon", "Mayans:Plumed Archer",
        "Aztecs:Jaguar Warrior", "Huns:Tarkan", "Vikings:Berserk", "Indians:Elephant Archer", "Italians:Genoese Crossbowman",
        "Slavs:Boyar", "Magyars:Magyar Huszar", "Ethiopians:Shotel Warrior", "Malians:Gbeto", "Berbers:Camel Archer",
        "Khmer:Ballista Elephant", "Malay:Karambit Warrior", "Burmese:Arambai", "Vietnamese:Rattan Archer", "Bulgarians:Konnik",
        "Tatars:Keshik", "Cumans:Kipchak", "Lithuanians:Leitis", "Burgundians:Coustillier", "Sicilians:Serjeant",
        "Poles:Obuch", "Bohemians:Hussite Wagon", "Dravidians:Urumi Swordsman", "Bengalis:Ratha", "Gurjaras:Chakram Thrower"
    };

    public Pair[] GetPairs(int number) {
        number = Math.Min(number, content.Length);
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

    public bool IsGraphic() {
        return false;
    }

}