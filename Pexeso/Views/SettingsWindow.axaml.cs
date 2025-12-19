using Avalonia.Controls;
using Avalonia.Interactivity;
using Pexeso.Game;
using Pexeso.Game.ContentProviders;
using System.Collections.Generic;

namespace Pexeso.Views;

public partial class SettingsWindow : Window {
    private static readonly string DEFAULT = "Default";
    private readonly Dictionary<string, IContentProvider> availableProviders = GetAvailableContentProviders();
    private MainWindow parent;
    private int NumPairs;
    private int NumPlayers;
    private IContentProvider ContentProvider;
    public SettingsWindow(MainWindow parent) {
        this.parent = parent;
        InitializeComponent();
        this.SetValue(Window.HeightProperty, 180);
        this.SetValue(Window.WidthProperty, 450);
        this.ContentSelectionSpinner.SetValue(ComboBox.ItemsSourceProperty, availableProviders.Keys);
        this.ContentSelectionSpinner.SelectedIndex = 0;
        ShowDialog(parent);
    }

    private void ApplySettingsButton_OnClick(object? sender, RoutedEventArgs e) {
        if (!ValidateInputs()) {
            return;
        }
        parent.settings = new GameSettings(NumPairs, NumPlayers, ContentProvider);
        Close();
    }

    private bool ValidateInputs() {
        if (!int.TryParse(PairsNumBox.GetValue(TextBox.TextProperty), out NumPairs) || NumPairs < 1) {
            return false;
        }
        if (!int.TryParse(PlayersNumBox.GetValue(TextBox.TextProperty), out NumPlayers) || NumPlayers < 1) {
            return false;
        }
        IContentProvider selectedProvider;
        availableProviders.TryGetValue((string)this.ContentSelectionSpinner.SelectedItem, out selectedProvider);
        ContentProvider = (selectedProvider == null) ? availableProviders[DEFAULT] : selectedProvider;
        return true;
    }

    private static Dictionary<string, IContentProvider> GetAvailableContentProviders() {
        Dictionary<string, IContentProvider> providers = new Dictionary<string, IContentProvider>();
        providers.Add(DEFAULT, new DefaultContentProvider());
        providers.Add("Czech", new CzechContentProvider());
        providers.Add("Age of Empires II", new AOEIIContentProvider());
        providers.Add("Cuphead", new CupheadContentProvider());
        providers.Add("StarGate", new StarGateContentProvider());
        return providers;
    }


}