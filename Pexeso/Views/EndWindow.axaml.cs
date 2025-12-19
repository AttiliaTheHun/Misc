using Avalonia.Controls;
using Avalonia.Interactivity;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System;

using Pexeso.Game;
using System.Collections;
using Pexeso.ViewModels;

namespace Pexeso.Views;

public partial class EndWindow : Window {
    private GameSettings settings;
    private Player[] players;
    
    public EndWindow(GameSettings settings, Player[] players) {
        this.settings = settings;
        this.players = players;
        this.SetValue(Window.HeightProperty, 400);
        this.SetValue(Window.WidthProperty, 600);
        DataContextChanged += OnDataContextChanged;
        this.DataContext = new EndWindowViewModel();
        InitializeComponent();
        Show();
    }

    private void OnDataContextChanged(object? sender, EventArgs e) {
        InitResultsListView(players);
    }

    private void InitResultsListView(Player[] players) {
        Debug.Assert(this.DataContext != null, "EndWindow.DataContext is null");
        foreach (Player player in players) {
            ((EndWindowViewModel) this.DataContext).Results.Add($"{player.Name} - {player.Points}");
        }
    }

    private void RematchButton_OnClick(object? sender, RoutedEventArgs e) {
        new GameInstance(settings);
        Close();
    }

    private void MainTitleButton_OnClick(object? sender, RoutedEventArgs e) {
        new MainWindow();
        Close();
    }
}

public class ListViewModel : INotifyPropertyChanged, IEnumerable {
    public ObservableCollection<ItemModel> Items { get; } = new();

    public void AddItem(string name, string points) {
        Items.Add(new ItemModel { PlayerName = name, PlayerPoints = points });
        OnPropertyChanged(nameof(Items));
    }

    public event PropertyChangedEventHandler? PropertyChanged;
    protected void OnPropertyChanged(string propertyName) =>
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));

    public IEnumerator GetEnumerator() {
        return Items.GetEnumerator();
    }
}

public class ItemModel {
    public string PlayerName { get; set; } = string.Empty;
    public string PlayerPoints { get; set; } = string.Empty;
}