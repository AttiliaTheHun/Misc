using Avalonia.Controls;
using Avalonia.Interactivity;
using Pexeso.Game;

namespace Pexeso.Views;

public partial class MainWindow : Window {
    public GameSettings settings { get; set; } = GameSettings.DefaultSettings();
    public MainWindow() {
        InitializeComponent();
        this.SetValue(Window.HeightProperty, 140);
        this.SetValue(Window.WidthProperty, 450);
        Show();
    }

    private void PlayButton_OnClick(object? sender, RoutedEventArgs e) {
        new GameInstance(settings);
        Close();
    }

    private void SettingsButton_OnClick(object? sender, RoutedEventArgs e) {
        new SettingsWindow(this);
    }
}