using Avalonia.Controls;
using Avalonia.Interactivity;
using System.Diagnostics;
using System;
using Avalonia.Input;

namespace Pexeso.Views;

public partial class GameWindow : Window {
    public GameWindow() {
        InitializeComponent();
        PostInit();
    }

    private void PostInit() {
        //this.GameGrid.SetValue(Grid.ShowGridLinesProperty, true);
    }

    public Grid GetGrid() {
        return this.GameGrid;
    }

}