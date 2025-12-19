using System.Collections.ObjectModel;

namespace Pexeso.ViewModels;

public partial class EndWindowViewModel : ViewModelBase {
    private ObservableCollection<string> results = new ObservableCollection<string>();
    public ObservableCollection<string> Results {
        get => results;
        set =>  this.SetProperty(ref results, value);
    }
}
