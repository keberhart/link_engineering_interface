import tkinter as tk
from tkinter import filedialog
import json
import os

from link_engineering.src.link_engineering.units import Temperature, Frequency, Distance, Angle, Power

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
        self.device_listbox = tk.Listbox(self.list_frame, width=30, height=20, selectmode=tk.SINGLE)
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

        self.update_device_listbox(active_index=0)

    def update_device_listbox(self, active_index=None):
        """Update the device listbox with the current devices."""
        # clear the current devices from the listbox
        self.device_listbox.delete(0, tk.END)
        # add the current devices to the listbox
        for device in self.app.device_library["devices"].keys():
            self.device_listbox.insert(tk.END, device)
        self.device_listbox.selection_set(active_index)
        self.device_listbox.activate(active_index)
        self.device_listbox.yview_moveto(0)

    def add_device(self):
        """Add a new device to the device library."""
        # create a window to add a new device, if the user clicks cancel, do nothing
        add_window = DeviceWindow(self, self.app)
        if add_window.result:
            self.update_device_listbox(active_index="end")

    def edit_device(self):
        """Edit an existing device in the device library."""
        # get the selected device from the listbox
        selected_device = self.device_listbox.get(tk.ACTIVE)
        # get the index of the selected device in the listbox
        index = self.device_listbox.index(tk.ACTIVE)
        # create a window to edit the device
        DeviceWindow(self, self.app, selected_device)
        self.update_device_listbox(index)

    def delete_device(self):
        """Delete an existing device from the device library."""
        # get the selected device from the listbox
        selected_device = self.device_listbox.get(tk.ACTIVE)
        # remove the selected device from the library
        self.app.device_library["devices"].pop(selected_device)
        self.app.save_device_library()
        # update the device listbox
        self.update_device_listbox(active_index=0)


class DeviceWindow(WindowHelpers):
    """A window to create a new device."""
    def __init__(self, parent, app, selected_device=None):
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

        # create a parameter list for lookups of the widgets, this is alist of tuples. The first element of the tuple is the points tothe parameter_name widget, the second element is theparameter_value widget.
        self.parameter_list = []

        # add a main frame for everything else to live in
        self.main_frame = tk.Frame(self, padx=15, pady=5)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        # create a frame for the add parameter button and dropdown menu also for the save and cancel buttons
        top_frame = tk.Frame(self.main_frame, padx=15, pady=5)
        top_frame.grid(row=0, column=0, sticky="nsew")
        # add widgets for creating a device here
        self.parameter_type_var = tk.StringVar()
        self.parameter_type_var.set("String")
        add_button = tk.Button(top_frame, text="Add Parameter")
        
        add_button.pack(side=tk.LEFT)
        parameter_type_menu = tk.OptionMenu(top_frame, self.parameter_type_var, "String", "Number", "Temerature", "Frequency", "Angle", "Distance", "Power")
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
        next_row = self.parameters_frame.grid_size()[1] + 1

        # create a label and entry for the device name
        name_label = tk.Label(self.parameters_frame, text="Name:")
        name_label.grid(row=next_row, column=0, sticky="w")
        self.name_entry = tk.Entry(self.parameters_frame)
        self.name_entry.grid(row=next_row, column=1, sticky="ew")

        add_button.config(command=lambda: self.add_parameter(self.parameters_frame, self.parameter_type_var, self.parameter_list, depth=0))
        # center the dialog on the parent window
        self.center_on_parent()

        if selected_device is not None:
            # get the device data from the device library
            device_data = self.app.device_library["devices"][selected_device]
            # load the device data into the entry fields
            self.name_entry.insert(0, selected_device)
            for key in device_data.keys():
                if type(device_data[key]) is str:
                    self.add_parameter(self.parameters_frame, "String", self.parameter_list, depth=0, data=[key, device_data[key]])
                elif type(device_data[key]) is int or type(device_data[key]) is float:
                    self.add_parameter(self.parameters_frame, "Number", self.parameter_list, depth=0, data=[key, device_data[key]])
                elif type(device_data[key]) is bool:
                    self.add_parameter(self.parameters_frame, "Boolean", self.parameter_list, depth=0, data=[key, device_data[key]])
                elif type(device_data[key]) is dict:
                    if key == "Frequency":   
                        self.add_parameter(self.parameters_frame,"Dictionary", self.parameter_list, depth=0, data=[key, device_data[key]])
                    elif key == "Temperature":
                        self.add_parameter(self.parameters_frame,"Dictionary", self.parameter_list, depth=0, data=[key, device_data[key]])
                    elif key == "Distance":
                        self.add_parameter(self.parameters_frame,"Dictionary", self.parameter_list, depth=0, data=[key, device_data[key]])
                    elif key == "Angle":
                        self.add_parameter(self.parameters_frame,"Dictionary", self.parameter_list, depth=0, data=[key, device_data[key]])
                    elif key == "Power":
                        self.add_parameter(self.parameters_frame,"Dictionary", self.parameter_list, depth=0, data=[key, device_data[key]])
                else:
                    raise ValueError("Unsupported data type for device parameter: {}".format(type(device_data[key])))

        parent.wait_window(self)

    def add_parameter(self, target_frame, type_var, storage_list, depth=0, data=None):
        """Add a new parameter to the device."""
        # what type of parameter to add?
        if data:
            parameter_type = type_var
        else:
            parameter_type = type_var.get()
        # add the parameter based on its type
        if parameter_type == "Dictionary":
            self.add_dictionary_object(target_frame, storage_list, depth, data)
        else:
            self.add_simple_object(target_frame, parameter_type, storage_list, depth, data)


    def add_simple_object(self, target_frame, object_type, storage_list, depth, data=None):
        """Add a new string object to the device."""
        next_row = target_frame.grid_size()[1] + 1

        descriptor_label = tk.Label(target_frame, text="Descriptor:")
        descriptor_label.grid(row=next_row, column=depth, sticky="w")
        value_label = tk.Label(target_frame, text=object_type)
        value_label.grid(row=next_row, column=depth+1, sticky="w")
        next_row += 1
        parameter_descriptor_entry = tk.Entry(target_frame,width=20)
        parameter_descriptor_entry.grid(row=next_row, column=depth,sticky="ew")
        parameter_value_entry = tk.Entry(target_frame, width=40)
        parameter_value_entry.grid(row=next_row, column=depth+1,sticky="ew")
        # append the parameter value label and entry widgets to a 2 elementlist and append that to the parameter_list.
        temp_list = [parameter_descriptor_entry, parameter_value_entry]
        if data:
            parameter_descriptor_entry.insert(0, data[0])
            parameter_value_entry.insert(0, data[1])
        storage_list.append(temp_list)

    def add_dictionary_object(self, target_frame, storage_list, depth, data=None):
        """Add a dictionary object to the parameters list."""
        next_row = target_frame.grid_size()[1] + 1
        dictionary_label = tk.Label(target_frame, text="Dictionary")
        dictionary_label.grid(row=next_row, column=depth,sticky="ew")
        dictionary_name_entry = tk.Entry(target_frame, width=40)
        dictionary_name_entry.grid(row=next_row, column=depth+1,sticky="ew")
        next_row += 1
        dictionary_contents = []
        # add a button to add key, value pairs to the dictionary object. Add a tk.StringVar() to hold the object type.
        parameter_type_var = tk.StringVar(value="Dictionary")
        # add a frame to hold the key, value pairs of the dictionary object.
        dictionary_frame = tk.Frame(target_frame)
        dictionary_frame.grid(row=next_row, column=depth+1,sticky="ew")
        # add a button to add key, value pairs to the dictionary object. Add a tk.StringVar() to hold the object type.
        parameter_type_var = tk.StringVar(value="Dictionary")
        next_row = dictionary_frame.grid_size()[1] + 1
        add_item_button = tk.Button(dictionary_frame, text="Add Item",command=lambda: self.add_parameter(dictionary_frame, parameter_type_var,dictionary_contents, depth+1))
        add_item_button.grid(row=next_row, column=depth,sticky="ew")
        parameter_type_menu = tk.OptionMenu(dictionary_frame, parameter_type_var, "String", "Number", "Boolean", "Dictionary")
        parameter_type_menu.grid(row=next_row, column=depth+1,sticky="ew")
        # append the parameter value label and entry widgets to a 2 elementlist and append that to the parameter_list.
        temp_list = ["Dictionary", dictionary_name_entry, dictionary_contents]
        if data:
            dictionary_name_entry.insert(0, data[0])
            device_data = data[1]
            for key in device_data.keys():
                if type(device_data[key]) is str:
                    self.add_parameter(dictionary_frame, "String", dictionary_contents, depth=depth+1, data=[key, device_data[key]])
                elif type(device_data[key]) is int or type(device_data[key]) is float:
                    self.add_parameter(dictionary_frame, "Number", dictionary_contents, depth=depth+1, data=[key, device_data[key]])
                elif type(device_data[key]) is bool:
                    self.add_parameter(dictionary_frame,"Boolean", dictionary_contents, depth=depth+1, data=[key, device_data[key]])
                elif type(device_data[key]) is dict:
                    self.add_parameter(dictionary_frame, "Dictionary", dictionary_contents, depth=depth+1, data=[key, device_data[key]])
                else:
                    ErrorWindow("Error", "Unsupported data type for device parameter: {}".format(type(device_data[key])))
        storage_list.append(temp_list)

    def save_device(self):
        """Save the device and close the window."""
        device_name = self.name_entry.get()
        # build a dictionary out of our parameter list.
        device_dict = {}
        for parameter in self.parameter_list:
            if type(parameter[0]) == str:
                dictionary_name_entry = parameter[1]
                dictionary_contents = parameter[2]
                device_dict[dictionary_name_entry.get()] = self.traverse_serial_dictionary(dictionary_contents)
            else:
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

    def traverse_serial_dictionary(self, dictionary_contents):
        """Traverse a serial dictionary and return a python dictionary."""
        temp_dictionary = {}
        for parameter in dictionary_contents:
            if type(parameter[0]) == str:
                dictionary_name_entry = parameter[1]
                dictionary_contents = parameter[2]
                temp_dictionary[dictionary_name_entry.get()] = self.traverse_serial_dictionary(dictionary_contents)
            else:
                descriptor = parameter[0].get()
                value = parameter[1].get()
                # set the value to the correct type.
                if value.isdigit():
                    value = int(value)
                elif "." in value:
                    value = float(value)
                else:
                    value = str(value)
                temp_dictionary[descriptor] = value
        return temp_dictionary


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