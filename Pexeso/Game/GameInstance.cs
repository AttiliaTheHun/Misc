using Avalonia.Controls;
using Pexeso.Views;
using Pexeso.ViewModels;
using System;
using Avalonia.Media;
using Avalonia;
using Avalonia.Media.Imaging;
using Avalonia.Platform;
using System.Diagnostics;
using Avalonia.Interactivity;
using Avalonia.Layout;

namespace Pexeso.Game;

public class GameInstance {
    public static readonly Uri BASE_ASSETS_URI = new Uri("avares://Pexeso/Assets/");
    private GameWindow window = new GameWindow {
                DataContext = new GameWindowViewModel(),
    };
    private GameSettings settings;
    private Player[] players;
    private Tile[] tiles;
    // we will init this by calling SwitchToNextPlayer()
    private int playerAtTurnIndex = -1;
    private Tile firstUncoveredTile = null;
    private Tile secondUncoveredTile = null;
    private int claimedTilesNum = 0;
    private bool singlePlayer = false;
    private bool isOver = false;


    public GameInstance(GameSettings settings) {
        this.settings = settings;
        this.players = Player.Players(settings.NumPlayers, settings.RandomPlayerNames);
        this.singlePlayer = players.Length == 1;
        if (singlePlayer) {
            // had he guessed them all in the first round, he would have the score of zero
            players[0].Points++;
        }
        InitTiles();
        InitGameGrid();
        SwitchToNextPlayer();
        window.AddHandler(Window.KeyUpEvent, HandleKeyReleased, RoutingStrategies.Bubble);
        window.Show();
    }

    private void InitTiles() {
        Pair[] content =  settings.ContentProvider.GetPairs(settings.NumPairs);
        tiles = new Tile[content.Length*2];
        int contentIndex = 0;
        for (int i = 0; i < tiles.Length; i+=2) {
            bool isFirstGraphic = (settings.ContentProvider.IsGraphic() && content[contentIndex].First.Contains('.'));;
            bool isSecondGraphic = (settings.ContentProvider.IsGraphic() && content[contentIndex].Second.Contains('.'));
            tiles[i] = new Tile(content[contentIndex].First, isFirstGraphic);
            tiles[i+1] = new Tile(content[contentIndex].Second, isSecondGraphic);
            tiles[i].Other = tiles[i+1];
            tiles[i+1].Other = tiles[i];
            contentIndex++;
        }
    }

    private void InitGameGrid() {
        Tile[] shuffled = (Tile[]) tiles.Clone();
        shuffled.Shuffle();
        Grid grid = window.GetGrid();
        int columns = (int) Math.Floor(Math.Sqrt(shuffled.Length));
        // if the remainder is zero, it would create a needles empty row, however if it is not, we would be missing a row
        int rows = (shuffled.Length % columns == 0) ? (shuffled.Length / columns) : (shuffled.Length / columns) + 1;
        InitGameGridDimensions(rows, columns);
        for (int i = 0; i < shuffled.Length; i++) {
            Border border = TileBorder();
            TextBlock control = TileText();
            border.Tag = shuffled[i];
            int column = i % columns;
            int row = i / columns;
            border.SetValue(Grid.ColumnProperty, column);
            border.SetValue(Grid.RowProperty, row);
            border.Child = control;
            shuffled[i].Bind(border);
            grid.Children.Add(border);
        }
    }

    private Border TileBorder() {
        Border border = new Border();
        border.SetValue(Border.MarginProperty, new Thickness(5));
        border.SetValue(Border.CornerRadiusProperty, new CornerRadius(10));
        border.SetValue(Border.BackgroundProperty, new SolidColorBrush(Color.Parse("LightBlue")));
        border.AddHandler(Border.TappedEvent, HandleTileTapped, RoutingStrategies.Bubble);
        return border;
    }

    private TextBlock TileText() {
        TextBlock control = new TextBlock();
        control.SetValue(TextBlock.TextAlignmentProperty, TextAlignment.Center);
        control.SetValue(TextBlock.VerticalAlignmentProperty, VerticalAlignment.Center);
        control.SetValue(TextBlock.FontSizeProperty, 25);
        control.SetValue(TextBlock.FontWeightProperty, FontWeight.Bold);
        return control;
    }

    private void HandleTileTapped(object sender, RoutedEventArgs e) {
        Debug.Assert(sender != null, "The ministry has fallen, we received a null sender");
        if (isOver) {
            new EndWindow(settings, players);
            window.Close();
        }
        if (secondUncoveredTile != null) {
            HandleKeyReleased(null, null);
            return;
        }
        Tile target = (Tile) ((Control) sender).Tag;
        if (firstUncoveredTile != null && target.Equals(firstUncoveredTile)) {
            return;
        }
        target.ChangeState(Tile.UNCOVERED_TILE);
        if (firstUncoveredTile == null) {
            firstUncoveredTile = target;
        } else {
            secondUncoveredTile = target;
        }

        if (secondUncoveredTile != null && firstUncoveredTile.Other.Equals(secondUncoveredTile)) {
            ClaimPairForCurrentPlayer();
        }
        
    }

    private void ClaimPairForCurrentPlayer() {
        if (!singlePlayer) {
            players[playerAtTurnIndex].Points++;
        }
        ClaimAndClearTiles();
    }

    private void HandleKeyReleased(object sender, RoutedEventArgs e) {
        if (isOver) {
            new EndWindow(settings, players);
            window.Close();
        }
        // the user is expected to select a field via mouse until two fields are uncovered 
        if (secondUncoveredTile == null) {
            return;
        }
        HideAndClearTiles();
        SwitchToNextPlayer();
    }

    private void HideAndClearTiles() {
        firstUncoveredTile.ChangeState(Tile.HIDDEN_TILE);
        secondUncoveredTile.ChangeState(Tile.HIDDEN_TILE);
        ClearTiles();
        if (singlePlayer) {
            players[playerAtTurnIndex].Points++;
        }
    }

    private void ClaimAndClearTiles() {
        firstUncoveredTile.ChangeState(Tile.CLAIMED_TILE);
        secondUncoveredTile.ChangeState(Tile.CLAIMED_TILE);
        ClearTiles();
        claimedTilesNum += 2;
        if (claimedTilesNum == tiles.Length) {
           isOver = true;
        }
    }

    private void ClearTiles() {
        firstUncoveredTile = null;
        secondUncoveredTile = null;
    }

    private void SwitchToNextPlayer() {
        playerAtTurnIndex = (playerAtTurnIndex + 1) % players.Length;
        window.Title = $"Pexeso - {players[playerAtTurnIndex].Name}'s turn";
    }

    private void InitGameGridDimensions(int rows, int columns) {
        Grid grid = window.GetGrid();
        for (int i = 0; i < rows; i++) {
            grid.RowDefinitions.Add(new RowDefinition());
        }
        for (int i = 0; i < columns; i++) {
            grid.ColumnDefinitions.Add(new ColumnDefinition());
        }
    }

}



class Tile {
    public const int HIDDEN_TILE = 0;
    public const int UNCOVERED_TILE = 1;
    public const int CLAIMED_TILE = 2;
    public string Content {get;}
    public bool IsGraphic {get;}
    public Tile Other { get; set; }
    [Obsolete]
    private int state = HIDDEN_TILE;
    private Border UIControl;

    public Tile(string content, bool graphic) {
        this.Content = content;
        this.IsGraphic = graphic;
    }

    public void ChangeState(int state) {
        switch (state) {
            case HIDDEN_TILE:
                SetStateHidden();
                break;
            case UNCOVERED_TILE:
                SetStateUncovered();
                break;
            case CLAIMED_TILE:
                SetStateClaimed();
                break;
        }
    }

    private void SetStateHidden() {
        if (IsGraphic) {
            UIControl.Child.SetValue(Image.SourceProperty, null);
        } else {
            UIControl.Child.SetValue(TextBlock.TextProperty, "");
        }
        UIControl.SetValue(Border.BackgroundProperty, new SolidColorBrush(Color.Parse("DarkBlue")));
    }

    private void SetStateUncovered() {
        if (IsGraphic) {
            UIControl.Child.SetValue(Image.SourceProperty, new Bitmap(AssetLoader.Open(new Uri(GameInstance.BASE_ASSETS_URI, Content))));
        } else {
            UIControl.Child.SetValue(TextBlock.TextProperty, Content);
        }
        UIControl.SetValue(Border.BackgroundProperty, new SolidColorBrush(Color.Parse("LightBlue")));
    }

    private void SetStateClaimed() {
        UIControl.SetValue(Border.BackgroundProperty, new SolidColorBrush(Color.Parse("LightGreen")));
        if (IsGraphic) {
            UIControl.Child.SetValue(Image.IsEnabledProperty, false);
        } else {
            UIControl.Child.SetValue(TextBlock.IsEnabledProperty, false);
        }
        UIControl.SetValue(Border.IsEnabledProperty, false);
        
    }

    public void Bind(Border control) {
        Debug.Assert(control.Child != null, "border child is null, we've lost the TextBlock");
        UIControl = control;
        if (IsGraphic) {
            UIControl.Child = new Image();
        }
        SetStateHidden();
    }
}