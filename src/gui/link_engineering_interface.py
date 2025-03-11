import tkinter as tk
from tkinter import filedialog
import json
import os

from .windows import PreferencesWindow, ErrorWindow, BrowseDeviceWindow


class LinkEngineeringInterface:
    """
    A simple GUI application using Tkinter.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Link Engineering Interface")
        self.root.geometry("800x600")
        
        # add a menu bar to the window
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Load Project", command=self.load_project)
        file_menu.add_command(label="Save Project", command=self.save_project)
        file_menu.add_command(label="Save As...", command=self.save_project_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu_bar)
        # add an edit menu to the window
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut")
        edit_menu.add_command(label="Copy")
        edit_menu.add_command(label="Paste")
        edit_menu.add_separator()
        edit_menu.add_command(label="Browse Devices", command=self.browse_devices)
        edit_menu.add_separator()
        edit_menu.add_command(label="Preferences", command=self.preferences)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        # add a help menu to the window
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About")
        menu_bar.add_cascade(label="Help", menu=help_menu)

        label = tk.Label(self.root, text="Welcome to the Link Engineering Interface!", font=("Helvetica", 16))
        label.pack(pady=20)

        button = tk.Button(self.root, text="Click Me", command=lambda: print("Button         clicked!"))
        button.pack(pady=10)

        # add a statusbar at the bottom of the window
        self.statusbar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.load_preferences()
        self.load_device_library()

    def load_preferences(self):
        """Load the preferences from a json file if it exists. If not, use default settings."""
        if os.path.exists("preferences.json"):
            with open("preferences.json", "r") as f:
                self.preferences = json.load(f)
            self.statusbar.config(text=f"Preferences loaded from {os.path.basename(os.getcwd())}/preferences.json")
        else:
            self.preferences = {}
            self.statusbar.config(text="No preferences found. Using default settings.")

    # add methods for opening and saving projects here.
    def load_project(self):
        """Using a File dialog, open a project file and load its contents into the interface."""
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r") as f:
                data = json.load(f)
                # load the data into the interface here.
                pass
            self.statusbar.config(text=f"Project loaded from {file_path}")

    def load_device_library(self):
        """Load the device library from a json file and store it in a dictinoary"""
        self.device_library = {}
        # figure out the full path to the devices folder
        # check the self.parent.preferences.devices_folder attribute to get the path to the devices folder.
        devices_folder = self.preferences["devices_folder"]
        # make sure the devices folder exists
        if not os.path.exists(devices_folder):
            os.makedirs(devices_folder)
            self.statusbar.config(text=f'Created devices folder at {devices_folder}')
        # join the devices folder and the device name to get the full path to the device json file.
        device_path = os.path.join(devices_folder, f'device_library.json')
        try:
            with open(device_path, 'r') as f:
                self.device_library = json.load(f)
                self.statusbar.config(text=f"Device library loaded from {device_path}")
        except FileNotFoundError:
            ErrorWindow(f'Cannot read device library', f'No file found at {device_path}')
            return
        
    def save_device_library(self):
        """Save the current device library to a json file."""
        devices_folder = self.preferences["devices_folder"]
        device_path = os.path.join(devices_folder, f'device_library.json')
        try:
            with open(device_path, 'w') as f:
                json.dump(self.device_library, f, indent=4)
                self.statusbar.config(text=f"Device library saved to {device_path}")
        except Exception as e:
            ErrorWindow(f'Cannot save device library', str(e))
            return
    
    def save_project(self):
        """Save the current project to a json file."""
        pass

    def save_project_as(self):
        """Save the current project to a new file."""
        pass

    def browse_devices(self):
        """Browse the devices library and Create new, Edit or Delete Them."""
        BrowseDeviceWindow(self.root, self)

    def preferences(self):
        """Open the preferences window."""
        PreferencesWindow(self.root, self)

    def run(self):
        self.root.mainloop()

class Device():
    """A class to represent a device in the project."""
    def __init__(self, json_data):
        """Initialize a device from json data."""
        self.json_data = json_data
        self.name = json_data['name']

    def __repr__(self):
        return f"Device(name={self.name})"
    
    def __str__(self):
        return f"Device(name={self.name})"


class Project():
    """A class to represent a project."""
    def __init__(self, json_data):
        """Initialize a project from json data."""
        self.json_data = json_data
        self.devices = [Device(device) for device in json_data['devices']]


def main():
    root = tk.Tk()
    interface = LinkEngineeringInterface(root)
    interface.run()

if __name__ == "__main__":
    main()
