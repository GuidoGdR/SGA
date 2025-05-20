#

import json
from tkinter import Tk, StringVar, ttk
from tkinter import messagebox

from typing import Union, Any, Callable
import os

from custom_types.states_dict_type import StatesDictType, states_dict_keysType
from custom_types.settings_types import SettingsDictType

from tools.vars import SETTINGS_PATH

class App(Tk):
    
    def __init__(self):
        from widgets.students_table import StudentsTable
        
        #
        from widgets.menu_bar import MenuBar 

        super().__init__()
        
        # Standar config
        self.title("SGA")
        
        try:
            icon_relative_path = os.path.join('_internal', 'media', 'icons', 'SGA.ico')
            icon_absolute_path = os.path.abspath(icon_relative_path)
            self.iconbitmap(icon_absolute_path)

        except Exception:
            messagebox.showwarning("Icono no encontrado.", "El logo de la aplicación no fue encontrado.")

        # Custom config
        self.settings = self._init_settings()

        self._states:StatesDictType = {
            "students": {
                "data": [],
                "suscriptions":[]
            }, 
            "have_changes": {
                "data": False,
                "suscriptions":[]
                },
            "allow_save": {
                "data": False,
                "suscriptions":[]
                },
            "allow_delete": {
                "data": False,
                "suscriptions":[]
                },
            "file": {
                "data":  {"path": "", "data": []},
                "suscriptions":[]
            }}

        self.validateions_cmd = {
            "grade": (self.register(self._validate_grade), '%P'),
        }

        self.order_by = StringVar(value="unordered")
        self.last_order_by_selected = "unordered"

        self.students_table:StudentsTable = None

        # MenuBar
        self.menu_bar = MenuBar(self)
        self.config(menu=self.menu_bar)
        


        # frame main
        self.main_frame = self.make_general_users_page(self)
        self.main_frame.pack(expand=True, fill="both")

    # Make frames
    def make_general_users_page(self, parent)->ttk.Frame:
        
        from widgets.students_table import StudentsTable

        frame = ttk.Frame(parent)
        
        # tabla estudiantes
        self.students_table = StudentsTable(parent=frame, root=self)
        self.students_table.pack(expand=True, fill="both")
        
        return frame
     
    # States
    def get_state(self, key:states_dict_keysType)->Union[None, Any]:
        if key in self._states.keys():
            return self._states[key]["data"]
        return None

    def _exist_or_create_state(self, key):
        if not(key in self._states.keys()):
            self._states[key]={}
            self._states[key]["suscriptions"] = []
            self._states[key]["data"] = []
    
    def set_state(self, key:states_dict_keysType, data:any)->any:
        
        self._exist_or_create_state(key)
        self._states[key]["data"] = data
        
        for i in self._states[key]["suscriptions"]:
            i(data)
        
        return data
    
    def suscribe_to_state(self, key:states_dict_keysType, on_update:Callable[[Any], None]):
        self._exist_or_create_state(key)
        self._states[key]["suscriptions"].append(on_update)
    
    # Validators
    def _validate_grade(self, new_value:str):
        if not new_value:
            return True
        
        if new_value.__len__() > 1 and new_value[0] == "0":
            return False
        
        try:
            value_int = int(new_value)
            return 0 <= value_int <= 10
        except ValueError:
            return False

    # Settings
    def _init_settings(self)-> SettingsDictType:

        settings = {
            "approve_at": "4",
            "promote_at": "8"
        }

        try:
            with open(SETTINGS_PATH, 'r') as settings_file:
                settings = json.load(settings_file)

            return settings

        except FileNotFoundError:
            return settings
        
        except json.JSONDecodeError:
            messagebox.showerror("Error cargar la configuración", f"Ocurrió un al interpretar los datos, formato erroneo.")
            return settings
        
        except Exception as e:
            messagebox.showerror("Error cargar la configuración", f"Ocurrió un error inesperado:\n{e}")
            return settings

    def save_settings(self):
        try:
            with open(SETTINGS_PATH, 'w') as settings_file:
                json.dump(self.settings, settings_file, indent=2)

        except Exception as e:
            messagebox.showerror("Error al guardar el archivo de configuración", f"Ocurrió un error inesperado:\n{e}")



if __name__ == "__main__":
    my_app = App()
    my_app.mainloop()
