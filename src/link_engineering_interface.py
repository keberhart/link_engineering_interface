import tkinter as tk
from tkinter import filedialog
import json
import os


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
        edit_menu.add_command(label="Create Device", command=self.create_device)
        edit_menu.add_command(label="Add Device", command=self.add_device)
        edit_menu.add_command(label="Remove Device", command=self.remove_device)
        edit_menu.add_command(label="Edit Device", command=self.edit_device)
        edit_menu.add_separator()
        edit_menu.add_command(label="Preferences", command=self.preferences)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        # add a help menu to the window
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About")
        menu_bar.add_cascade(label="Help", menu=help_menu)

        # load the preferences json file if it exists
        if os.path.exists("preferences.json"):
            with open("preferences.json", "r") as f:
                self.preferences = json.load(f)
        else:
            self.preferences = {}

        label = tk.Label(self.root, text="Welcome to the Link Engineering Interface!", font=("Helvetica", 16))
        label.pack(pady=20)

        button = tk.Button(self.root, text="Click Me", command=lambda: print("Button         clicked!"))
        button.pack(pady=10)

    def run(self):
        self.root.mainloop()

    # add methods for opening and saving projects here.
    def load_project(self):
        """Using a File dialog, open a project file and load its contents into the interface."""
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r") as f:
                data = json.load(f)
                # load the data into the interface here.
                pass
            print(f"Loaded data: {data}")
    
    def save_project(self):
        """Save the current project to a json file."""
        pass

    def save_project_as(self):
        """Save the current project to a new file."""
        pass

    # add methods for adding, removing, and editing devices here
    def create_device(self):
        """Create a new device and save it for later use."""
        CreateDeviceWindow(self.root, self)
        
    def add_device(self):
        """Add an existing device to the project."""
        pass

    def remove_device(self):
        """Remove a device from the project."""
        pass

    def edit_device(self):
        """Edit an existing device in the project."""
        pass

    def preferences(self):
        """Open the preferences window."""
        PreferencesWindow(self.root, self)


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


class WindowHelpers(tk.Toplevel):
    """A class for helper functions."""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def center_on_parent(self):
        """Center the dialog on the parent window."""
        self.parent.update_idletasks()  # update geometry to get correct size
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        self.update_idletasks()  # update geometry to get correct size
        dialog_width = self.winfo_reqwidth()
        dialog_height = self.winfo_reqheight()
        x = (parent_width - dialog_width) // 2 + self.parent.winfo_x()
        y = (parent_height - dialog_height) // 2 + self.parent.winfo_y()
        self.geometry(f"+{x}+{y}")


class CreateDeviceWindow(WindowHelpers):
    """A window to create a new device."""
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.title("Create Device")
        # set the dialog size
        self.geometry()
        # set the dialog to be modal
        self.transient(parent)
        self.grab_set()
        self.focus_set()
        # add widgets for creating a device here
        top_frame = tk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="ew")
        save_button = tk.Button(top_frame, text="Save", command=self.save_device)
        save_button.grid(row=0, column=0)
        cancel_button = tk.Button(top_frame, text="Cancel", command=self.destroy)
        cancel_button.grid(row=0, column=1)

        name_label = tk.Label(self, text="Name:")
        name_label.grid(row=1, column=0, sticky="w")
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=1, column=1, sticky="ew")

        self.device_type_var = tk.StringVar(self)
        device_types = ['Amplifier', 'Attenuator']
        self.device_type_var.set(device_types[0])
        device_type_dropdown = tk.OptionMenu(self, self.device_type_var, *device_types)
        device_type_dropdown.grid(row=2, column=0, columnspan=2, sticky="ew")    
        self.gain_label = tk.Label(self, text="Gain (dB):")
        self.gain_label.grid(row=3, column=0, sticky="w")
        self.gain_spinbox = tk.Spinbox(self, from_=0, to=100)
        self.gain_spinbox.grid(row=3, column=1, sticky="ew")
        self.device_type_var.trace_add("write", self.set_device_type)

        input_frequency_label = tk.Label(self, text="Input Frequency (MHz):")
        input_frequency_label.grid(row=4, column=0, sticky="w")
        self.input_frequency_entry = tk.Entry(self)
        self.input_frequency_entry.grid(row=4, column=1, sticky="ew")

        output_frequency_label = tk.Label(self, text="Output Frequency (MHz):")
        output_frequency_label.grid(row=5, column=0, sticky="w")
        self.output_frequency_entry = tk.Entry(self)
        self.output_frequency_entry.grid(row=5, column=1, sticky="ew")

        # center the dialog on the parent window
        self.center_on_parent()

    def set_device_type(self, name, index, mode):
        """Set the device type based on the selected option in the dropdown."""

        if self.device_type_var.get() == 'Amplifier':
            self.gain_label.config(text="Gain (dB):")
            self.gain_spinbox.config(from_=0, to=100)
        else:
            self.gain_label.config(text="Attenuation (dB):")
            self.gain_spinbox.config(from_=-100, to=0)

    def save_device(self):
        """Save the device and close the window."""
        name = self.name_entry.get()
        type = self.device_type_var.get()
        input_frequency = float(self.input_frequency_entry.get())
        output_frequency = float(self.output_frequency_entry.get())
        gain = float(self.gain_spinbox.get())

        # create a dictionary with the device data
        device = {'name': name,
                    'type': type,
                    'input_frequency': input_frequency,
                    'output_frequency': output_frequency,
                    'gain': gain}
        
        # figure out the full path to the devices folder
        # check the self.parent.preferences.devices_folder attribute to get the path to the devices folder.
        devices_folder = self.app.preferences["devices_folder"]
        # make sure the devices folder exists
        if not os.path.exists(devices_folder):
            os.makedirs(devices_folder)
        # make sure the devices folder is writable
        if not os.access(devices_folder, os.W_OK):
            raise PermissionError(f'Cannot write to {devices_folder}')
        # join the devices folder and the device name to get the full path to the device json file.
        device_path = os.path.join(devices_folder, f'{name}.json')
        # write the device to the json file.
        with open(device_path, 'w') as f:
            json.dump(device, f, indent=4)
        # close the window
        self.destroy()


class PreferencesWindow(WindowHelpers):
    """A dialog for setting preferences."""
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.title("Preferences")
        self.geometry()
        self.grab_set()
        self.focus_set()

        # check if a preferences file exists
        if os.path.exists('preferences.json'):
            with open('preferences.json', 'r') as f:
                self.app.preferences = json.load(f)
        else:
            self.app.preferences = {}
        # create a frame for the preferences
        preferences_frame = tk.Frame(self)
        preferences_frame.pack(padx=10, pady=10)
        # create a label and entry for the Devices folder path
        devices_folder_label = tk.Label(preferences_frame, text="Devices folder path:")
        devices_folder_label.grid(row=0, column=0, sticky=tk.W)
        self.devices_folder_entry = tk.Entry(preferences_frame, width=50)
        self.devices_folder_entry.insert(0, self.app.preferences.get('devices_folder', 'devices/'))
        self.devices_folder_entry.grid(row=0, column=1, padx=10)
        # add folder selection button for Devices folder path
        devices_folder_button = tk.Button(preferences_frame, text="Browse", command=self.browse_devices_folder)
        devices_folder_button.grid(row=0, column=2, padx=5)

        # create a label and entry for the Project folder path
        project_folder_label = tk.Label(preferences_frame, text="Project folder path:")
        project_folder_label.grid(row=1, column=0, sticky=tk.W)
        self.project_folder_entry = tk.Entry(preferences_frame, width=50)
        self.project_folder_entry.insert(0, self.app.preferences.get('project_folder', 'projects/'))
        self.project_folder_entry.grid(row=1, column=1, padx=10)
        # add folder selection button for Project folder path
        project_folder_button = tk.Button(preferences_frame, text="Browse", command=self.browse_project_folder)
        project_folder_button.grid(row=1, column=2, padx=5)

        # create a frame for the save and cancel buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        # create a button to save the preferences
        save_button = tk.Button(button_frame, text="Save", command=self.save_preferences)
        save_button.pack(side=tk.LEFT, pady=10)
        # create a cancel button to cancel the preferences
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, pady=10)
        
        self.center_on_parent()

    def browse_devices_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.devices_folder_entry.delete(0, tk.END)
            self.devices_folder_entry.insert(0, folder_selected)

    def browse_project_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.project_folder_entry.delete(0, tk.END)
            self.project_folder_entry.insert(0, folder_selected)

    def save_preferences(self):
        self.app.preferences = {
            'devices_folder': self.devices_folder_entry.get(),
            'project_folder': self.project_folder_entry.get()
        }
        with open('preferences.json', 'w') as f:
            json.dump(self.app.preferences, f, indent=4)
        self.destroy()


def main():
    root = tk.Tk()
    interface = LinkEngineeringInterface(root)
    interface.run()

if __name__ == "__main__":
    main()
