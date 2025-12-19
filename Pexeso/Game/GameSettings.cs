using System;
using Pexeso.Game.ContentProviders;

namespace Pexeso.Game;

public record GameSettings(int NumPairs, int NumPlayers, IContentProvider ContentProvider) {
    public bool RandomPlayerNames { get; } = new Random().NextDouble() > 0.5;
    public static GameSettings DefaultSettings() {
        return new GameSettings(8, 2, new DefaultContentProvider());
    }
}