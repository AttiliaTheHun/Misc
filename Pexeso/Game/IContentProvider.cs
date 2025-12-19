namespace Pexeso.Game;

public interface IContentProvider {
    public Pair[] GetPairs(int number);
}

public readonly record struct Pair(string First, string Second) {}