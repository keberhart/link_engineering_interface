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


class WindowHelpers(tk.Toplevel):
    """A class for helper functions."""
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app

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

    def update_status_bar(self, message):
        """Update the status bar with a message."""
        self.app.statusbar.config(text=message)


class BrowseDeviceWindow(WindowHelpers):
    """A window to browse and maintain our device library"""
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.parent = parent
        self.app = app
        self.title("Browse Device Library")
        # set the dialog size
        self.geometry()
        # set the dialog to be modal
        self.transient(parent)
        self.grab_set()
        self.focus_set()
        # add a main frame for everything else to live in
        self.main_frame = tk.Frame(self, padx=15, pady=5)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        # add a frame on the left side for the device list
        self.list_frame = tk.Frame(self.main_frame)
        self.list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # add a listbox to the left side frame for the device list
        self.device_listbox = tk.Listbox(self.list_frame, width=30, height=20)
        self.device_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # add a frame on the right side for our control buttons. Add, Edit, and Delete.
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        # add the buttons to the control frame
        self.add_button = tk.Button(self.control_frame, text="Add", command=self.add_device)
        self.edit_button = tk.Button(self.control_frame, text="Edit", command=self.edit_device)
        self.delete_button = tk.Button(self.control_frame, text="Delete", command=self.delete_device)
        self.cancel_button = tk.Button(self.control_frame, text="Cancel", command=self.destroy)
        self.add_button.pack(side=tk.TOP, fill=tk.X)
        self.edit_button.pack(side=tk.TOP, fill=tk.X)
        self.delete_button.pack(side=tk.TOP, fill=tk.X)
        self.cancel_button.pack(side=tk.TOP, fill=tk.X)
        self.center_on_parent()

        self.update_device_listbox()

    def update_device_listbox(self):
        """Update the device listbox with the current devices."""
        # clear the current devices from the listbox
        self.device_listbox.delete(0, tk.END)
        # add the current devices to the listbox
        for device in self.app.device_library["devices"].keys():
            self.device_listbox.insert(tk.END, device)

    def add_device(self):
        """Add a new device to the device library."""
        # create a window to add a new device, if the user clicks cancel, do nothing
        add_window = CreateDeviceWindow(self, self.app)
        if add_window.result:
            self.update_device_listbox()

    def edit_device(self):
        """Edit an existing device in the device library."""
        # get the selected device from the listbox
        selected_device = self.device_listbox.get(tk.ACTIVE)
        # create a window to edit the device
        CreateDeviceWindow(self, self.app, selected_device)
        self.update_device_listbox()

    def delete_device(self):
        """Delete an existing device from the device library."""
        # get the selected device from the listbox
        selected_device = self.device_listbox.get(tk.ACTIVE)
        # remove the selected device from the library
        self.app.device_library["devices"].pop(selected_device)
        self.app.save_device_library()
        # update the device listbox
        self.update_device_listbox()


class CreateDeviceWindow(WindowHelpers):
    """A window to create a new device."""
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.parent = parent
        self.app = app
        self.result = None
        self.title("Create Device")
        # set the dialog size
        self.geometry()
        # set the dialog to be modal
        self.transient(parent)
        self.grab_set()
        self.focus_set()

        # add a main frame for everything else to live in
        self.main_frame = tk.Frame(self, padx=15, pady=5)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        # create a frame for the add parameter button and dropdown menu also for the save and cancel buttons
        top_frame = tk.Frame(self.main_frame, padx=15, pady=5)
        top_frame.grid(row=0, column=0, sticky="nsew")
        # add widgets for creating a device here
        add_button = tk.Button(top_frame, text="Add Parameter", command=self.add_parameter)
        add_button.pack(side=tk.LEFT)
        self.parameter_type_var = tk.StringVar()
        self.parameter_type_var.set("String")
        parameter_type_menu = tk.OptionMenu(top_frame, self.parameter_type_var, "String", "Number", "Boolean", "Dictionary")
        parameter_type_menu.pack(side=tk.LEFT)
        # add an empty label to separate the buttons
        empty_label = tk.Label(top_frame, text="", width=2) 
        empty_label.pack(side=tk.LEFT, expand=True) 
        # add the save and cancel buttons
        cancel_button = tk.Button(top_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT)
        save_button = tk.Button(top_frame, text="Save", command=self.save_device)
        save_button.pack(side=tk.RIGHT)

        # add a frame for the device parameters
        self.parameters_frame = tk.Frame(self.main_frame, padx=15, pady=5)
        self.parameters_frame.grid(row=1, column=0, sticky="nsew")

        # add a class variable to keep track of which row we are on inside the parameters frame

        self.grid_row_number = 0

        # create a label and entry for the device name
        name_label = tk.Label(self.parameters_frame, text="Name:")
        name_label.grid(row=self.grid_row_number, column=0, sticky="w")
        self.name_entry = tk.Entry(self.parameters_frame)
        self.name_entry.grid(row=self.grid_row_number, column=1, sticky="ew")
        self.grid_row_number += 1

        # create a parameter list for lookups of the widgets, this is a list of tuples. The first element of the tuple is the points to the parameter_name widget, the second element is the parameter_value widget.
        self.parameter_list = []

        # center the dialog on the parent window
        self.center_on_parent()
        parent.wait_window(self)

    def add_parameter(self):
        """Add a new parameter to the device."""
        # what type of parameter to add?
        parameter_type = self.parameter_type_var.get()
        if parameter_type == "String":
            self.add_string_object()
        elif parameter_type == "Number":
            self.add_number_object()
        elif parameter_type == "Boolean":
            self.add_boolean_object()
        elif parameter_type == "Dictionary":
            self.add_dictionary_object()
        elif parameter_type == "None":
            pass

    def add_string_object(self):
        """Add a new string object to the device."""
        # add entry widgets for "descritor" and "value"
        descriptor_label = tk.Label(self.parameters_frame,text="Descriptor:")
        descriptor_label.grid(row=self.grid_row_number, column=0,sticky="w")
        value_label = tk.Label(self.parameters_frame, text="String:")
        value_label.grid(row=self.grid_row_number, column=1, sticky="w")
        self.grid_row_number += 1
        parameter_descriptor_entry = tk.Entry(self.parameters_frame,width=20)
        parameter_descriptor_entry.grid(row=self.grid_row_number, column=0,sticky="ew")
        parameter_value_entry = tk.Entry(self.parameters_frame, width=40)
        parameter_value_entry.grid(row=self.grid_row_number, column=1,sticky="ew")
        self.grid_row_number += 1
        # append the parameter value label and entry widgets to a 2 elementlist and append that to the parameter_list.
        temp_list = [parameter_descriptor_entry, parameter_value_entry]
        self.parameter_list.append(temp_list)
        
    def add_number_object(self):
        """Add a number object to the parameters frame."""
        # add entry widgets for "descritor" and "value"
        descriptor_label = tk.Label(self.parameters_frame,text="Descriptor:")
        descriptor_label.grid(row=self.grid_row_number, column=0,sticky="w")
        value_label = tk.Label(self.parameters_frame, text="Number:")
        value_label.grid(row=self.grid_row_number, column=1, sticky="w")
        self.grid_row_number += 1
        parameter_descriptor_entry = tk.Entry(self.parameters_frame,width=20)
        parameter_descriptor_entry.grid(row=self.grid_row_number, column=0,sticky="ew")
        parameter_value_entry = tk.Entry(self.parameters_frame, width=40)
        parameter_value_entry.grid(row=self.grid_row_number, column=1,sticky="ew")
        self.grid_row_number += 1
        # append the parameter value label and entry widgets to a 2 elementlist and append that to the parameter_list.
        temp_list = [parameter_descriptor_entry, parameter_value_entry]
        self.parameter_list.append(temp_list)

    def add_boolean_object(self):
        """Add a boolean object to the parameters list. This is used for parameters that have a true or false value."""
        # add entry widgets for "descritor" and "value"
        descriptor_label = tk.Label(self.parameters_frame,text="Descriptor:")
        descriptor_label.grid(row=self.grid_row_number, column=0,sticky="w")
        value_label = tk.Label(self.parameters_frame, text="Boolean:")
        value_label.grid(row=self.grid_row_number, column=1, sticky="w")
        self.grid_row_number += 1
        parameter_descriptor_entry = tk.Entry(self.parameters_frame,width=20)
        parameter_descriptor_entry.grid(row=self.grid_row_number, column=0,sticky="ew")
        parameter_value_entry = tk.Entry(self.parameters_frame, width=40)
        parameter_value_entry.grid(row=self.grid_row_number, column=1,sticky="ew")
        self.grid_row_number += 1
        # append the parameter value label and entry widgets to a 2 elementlist and append that to the parameter_list.
        temp_list = [parameter_descriptor_entry, parameter_value_entry]
        self.parameter_list.append(temp_list)

    def add_dictionary_object(self):
        """Add a dictionary object to the parameters list."""
        # Adding a dictinary means we need a new set of widgets for each key-value pair.
        pass

    def save_device(self):
        """Save the device and close the window."""
        device_name = self.name_entry.get()
        # build a dictionary out of our parameter list.
        device_dict = {}
        for parameter in self.parameter_list:
            descriptor = parameter[0].get()
            value = parameter[1].get()
            # set the value to the correct type.
            if value.isdigit():
                value = int(value)
            elif "." in value:
                value = float(value)
            else:
                value = str(value)
            device_dict[descriptor] = value
        self.app.device_library["devices"][device_name] = device_dict
        self.app.save_device_library()
        self.result = True
        self.destroy()


class PreferencesWindow(WindowHelpers):
    """A dialog for setting preferences."""
    def __init__(self, parent, app):
        super().__init__(parent, app)
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
                self.update_status_bar(f'Preferences loaded from {os.getcwd()}\\preferences.json')
        else:
            self.app.preferences = {}
            self.update_status_bar(f'No preferences file found. Using default settings.')
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
        try:
            with open('preferences.json', 'w') as f:
                json.dump(self.app.preferences, f, indent=4)
                self.update_status_bar("Preferences saved successfully")
        except Exception as e:
            self.update_status_bar(f"Error saving preferences: {e}")
            ErrorWindow(f"Error saving preferences: {e}")
        self.destroy()


class ErrorWindow(tk.Toplevel):
    def __init__(self, parent, message):
        super().__init__(parent)
        self.title("Error")
        self.geometry()
        label = tk.Label(self, text=message, font=("Helvetica", 12))
        label.pack(pady=20)
        button = tk.Button(self, text="OK", command=self.destroy)
        button.pack(pady=10)


def main():
    root = tk.Tk()
    interface = LinkEngineeringInterface(root)
    interface.run()

if __name__ == "__main__":
    main()
