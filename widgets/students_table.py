from tkinter import ttk
from tkinter import ttk, Entry, StringVar

from main import App
from tools.calculate_average import calculate_average

class StudentsTable(ttk.Treeview):
    def __init__(self, parent, root:App):
        super().__init__(parent, columns=("name", "subjects", "grade1", "grade2", "grade3", "average"))
        
        self.root = root

        self.students_selected_ids = []
        self.students_selected_index = []

        self.column("#0", width=50, anchor="w")
        self.column("name", width=140, anchor="w")
        self.column("subjects", width=100, anchor="center")
        self.column("grade1", width=70, anchor="center")
        self.column("grade2", width=70, anchor="center")
        self.column("grade3", width=70, anchor="center")
        self.column("average", width=70, anchor="center")

        self.heading("#0", text="Nº", anchor="center")
        self.heading("name", text="Nombre", anchor="center")
        self.heading("subjects", text="Materia", anchor="center")
        self.heading("grade1", text="Nota 1", anchor="center")
        self.heading("grade2", text="Nota 2", anchor="center")
        self.heading("grade3", text="Nota 3", anchor="center")
        self.heading("average", text="Promedio", anchor="center")

        
        self.active_entry = None
        self.current_row = None
        self.current_column = None
        self.entry_var = StringVar()

        root.suscribe_to_state("students", self.on_update_students)

        self.bind("<Double-1>", self.on_double_click)
        self.bind('<<TreeviewSelect>>', self.on_select_item)

    def on_select_item(self, event):

        selecteds = self.selection()

        if selecteds == self.students_selected_ids:
            # dont have changes
            return
        
        self.students_selected_index = []
        self.students_selected_ids = selecteds

        if selecteds:
                
            for column_id in selecteds:
                self.students_selected_index.insert(0, int(self.item(column_id)['text']) - 1)

            self.root.set_state("allow_delete", True)

        else:
            self.root.set_state("allow_delete", False)

    def on_double_click(self, event):
        item = self.identify_row(event.y)
        column = self.identify_column(event.x)

        if item and not(column in ("#0", "#6")):
            self.current_row = item
            self.current_column = column
            x, y, width, height = self.bbox(item, column)
            
            current_value = self.item(item, 'text') if column == '#0' else self.set(item, column)

            if self.active_entry:
                self.active_entry.destroy()

            self.entry_var.set(current_value)
            
            if column in ('#2', '#3', '#4'):
                self.active_entry = Entry(self, textvariable=self.entry_var, validate="key", validatecommand=self.root.validateions_cmd["grade"], width=10, justify="center")
            
            else:
                self.active_entry = Entry(self, textvariable=self.entry_var, width=10, justify="center")
                #only_numbers_validate_command = (root.register(onlyNumbers), '%P')
                
                """
                self.active_entry = Entry(self, textvariable=self.entry_var, width=10, justify="center",
                    validate="key", validatecommand=only_numbers_validate_command)
                """
            
            self.active_entry.place(x=x, y=y, width=width, height=height)
            self.active_entry.select_range(0, 'end')
            self.active_entry.focus_set()
            self.active_entry.bind("<Return>", self.save_edit)
            self.active_entry.bind("<FocusOut>", self.cancel_edit)
            self.active_entry.bind("<Escape>", self.cancel_edit)

    def save_edit(self, event=None):
        if self.active_entry:
            new_value = self.entry_var.get()
            
            self.set(self.current_row, self.current_column, new_value)

            students_new_data = self.root.get_state("students")

            student_index = int(self.item(self.current_row)['text']) - 1
            column_index = int(self.current_column.replace("#", "")) - 1

            students_new_data[student_index][column_index] = new_value

            if self.current_column in ("#3", "#4", "#5"):
                #calculate average
                
                grade_1:str = self.set(self.current_row, "grade1")
                grade_2:str = self.set(self.current_row, "grade2")
                grade_3:str = self.set(self.current_row, "grade3")

                
                students_new_data[student_index][5] = calculate_average(grade_1, grade_2, grade_3)
            
            self.root.set_state("students", students_new_data)
            
            self.active_entry.destroy()
            self.active_entry = None
            self.current_row = None
            self.current_column = None

    def cancel_edit(self, event=None):
        if self.active_entry:
            self.active_entry.destroy()
            self.active_entry = None
            self.current_row = None
            self.current_column = None

    def on_update_students(self, data:list):
        
        for item in self.get_children():
            self.delete(item)

        for index in range(data.__len__()):
            row = data[index]
            self.insert("", "end", text=(index + 1), values=(row[0], row[1],row[2],row[3],row[4],row[5]))
            