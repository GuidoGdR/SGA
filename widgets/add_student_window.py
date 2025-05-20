from tkinter import Toplevel, Label, Entry, Button

from main import App
from tools.calculate_average import calculate_average

class AddStudentWindow(Toplevel):
    def __init__(self, root:App):
        super().__init__(root)

        self.root = root

        self.title("Agregar Nuevo Alumno")

        self.config(padx="20", pady="10")
        self.resizable(False, False)

        self._create_add_student_form()

    def _create_add_student_form(self):

        validate_grade_cmd = self.root.validateions_cmd["grade"]
        
        Label(self, text="Nombre:").grid(row=0, column=0, padx=5, pady=10)
        self.name_entry = Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=10)

        Label(self, text="Materia:").grid(row=1, column=0, padx=5, pady=10)
        self.subject_entry = Entry(self)
        self.subject_entry.grid(row=1, column=1, padx=5, pady=10)

        Label(self, text="Nota 1:").grid(row=2, column=0, padx=5, pady=10)
        self.grade1_entry = Entry(self, validate="key", validatecommand=validate_grade_cmd)
        self.grade1_entry.grid(row=2, column=1, padx=5, pady=10)

        Label(self, text="Nota 2:").grid(row=3, column=0, padx=5, pady=10)
        self.grade2_entry = Entry(self, validate="key", validatecommand=validate_grade_cmd)
        self.grade2_entry.grid(row=3, column=1, padx=5, pady=10)

        Label(self, text="Nota 3:").grid(row=4, column=0, padx=5, pady=10)
        self.grade3_entry = Entry(self, validate="key", validatecommand=validate_grade_cmd)
        self.grade3_entry.grid(row=4, column=1, padx=5, pady=10)

        save_button = Button(self, text="Guardar", command=self._on_click_save)
        save_button.grid(row=5, column=0, columnspan=2, pady=10)
    
    def _on_click_save(self):
        name = self.name_entry.get()
        subject = self.subject_entry.get()
        
        grade_1 = self.grade1_entry.get()
        grade_2 = self.grade2_entry.get()
        grade_3 = self.grade3_entry.get()

        average = calculate_average(grade_1, grade_2, grade_3)

        new_row = [name, subject, grade_1, grade_2, grade_3, average]

        data = [] or self.root.get_state("students")

        data.append(new_row)
        
        self.root.set_state("students", data)

        self.destroy()

