from src.gui.link_engineering_interface import LinkEngineeringInterface, PreferencesWindow

def test_link_engineering_interface():
    interface = LinkEngineeringInterface()
    assert isinstance(interface, LinkEngineeringInterface)
def test_preferences_window():
    window = PreferencesWindow()
    # check if the window is an instance of PreferencesWindow
    assert isinstance(window, PreferencesWindow)

