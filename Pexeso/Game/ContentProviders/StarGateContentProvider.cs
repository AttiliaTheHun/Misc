namespace Pexeso.Game.ContentProviders;

using System;

public class StarGateContentProvider : IContentProvider {
    private readonly string[] content = {
        "Earth:earth.png", "Crater:crater.png", "Virgo:virgo.png", "Bootes:bootes.png", "Centaurus:centaurus.png", "Libra:libra.png",
        "Serpens Caput:serpens_caput.png", "Norma:norma.png", "Scorpio:scorpio.png", "Cra:cra.png", "Scutum:scutum.png", "Sagittarius:sagittarius.png",
        "Aquila:aquila.png", "Mic:mic.png", "Capricorn:capricorn.png", "Pisces Austrinus:pisces_austrinus.png", "Equuleus:equuleus.png", "Aquarius:aquarius.png", 
        "Pegasus:pegasus.png", "Sculptor:sculptor.png", "Pisces:pisces.png", "Andromeda:andromeda.png", "Triangulum:triangulum.png", "Aries:aries.png",
        "Perseus:perseus.png", "Cetus:cetus.png", "Taurus:taurus.png", "Auriga:auriga.png", "Eridanus:eridanus.png", "Orion:orion.png", 
        "Canis Minor:canis_minor.png", "Monoceros:monoceros.png", "Gemini:gemini.png", "Hydra:hydra.png", "Lynx:lynx.png", "Cancer:cancer.png", 
        "Sextans:sextans.png", "Leo Minor:leo_minor.png", "Leo:leo.png"
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
        return true;
    }
}