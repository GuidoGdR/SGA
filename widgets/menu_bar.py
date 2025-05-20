
from tkinter import Menu, DISABLED, NORMAL, Toplevel, Label, Entry, Button, StringVar
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
import csv
import copy

from typing import Literal
import matplotlib.pyplot as plt
from main import App
from tools.cancel_for_changes_protection import cancel_for_changes_protection

from tools.order_by import order_by_dict
from tools.make_img_from_matrix import make_img_from_matrix

from widgets.add_student_window import AddStudentWindow

def test():
    pass

class MenuBar(Menu):
    def __init__(self, root:App):
        super().__init__(root)

        self.root = root

        self.file_menu = self._create_file_menu()
        self.add_cascade(label="Archivo", menu=self.file_menu)

        self.edit_menu = self._create_edit_menu()
        self.add_cascade(label="Editar", menu=self.edit_menu)
        
        self.order_menu = self._create_order_menu()
        self.add_cascade(label="Orden", menu=self.order_menu)

        self.reports_menu = self._create_reports_menu()
        self.add_cascade(label="Generar informes", menu=self.reports_menu, state=DISABLED)

        self.settings_window = None
        self.add_command(label="Configuración", command=self.on_click_settings)


        root.suscribe_to_state("students", self.on_update_students)
        root.suscribe_to_state("allow_save", self.on_update_allow_save)
        root.suscribe_to_state("allow_delete", self.on_update_allow_delete)


    # FILE
    def _create_file_menu(self)->Menu:

        # Crear el menú "Archivo" y sus opciones
        file_menu = Menu(self, tearoff=0)
        file_menu.add_command(label="Nuevo", command=self.on_click_new, state=DISABLED)
        file_menu.add_command(label="Abrir", command=self.on_click_open)
        file_menu.add_command(label="Guardar", command=self.on_click_save, state=DISABLED)
        file_menu.add_command(label="Guardar como...", command=self.on_click_save_as, state=DISABLED)
        file_menu.add_separator()  # Agrega una línea separadora
        file_menu.add_command(label="Salir", command=self.on_click_quit)
        
        return file_menu
    
    def on_click_new(self):

        if cancel_for_changes_protection(self.root):
            return
            
        self.root.set_state("students", [])
        self.root.set_state("file", {"path": "", "data": []})

    def on_click_open(self):
        
        if cancel_for_changes_protection(self.root):
            return
        
        file_path = askopenfilename(defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")])
        
        if file_path:
            try:
                with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                    
                    file_data=[]
                    reader = csv.reader(csvfile)
                    next(reader)
                    for row in reader:
                        file_data.append(row)

            except Exception as e:
                messagebox.showerror("Error al abrir el archivo", f"Ocurrió un error al abrir el archivo:\n{e}")
                return
            
            self.root.set_state("file", {"path": file_path, "data": copy.deepcopy(file_data)})
            self.root.set_state("students", file_data)

    def on_click_save(self):

        file_path = self.root.get_state("file")["path"]

        if file_path:
            
            students = self.root.get_state("students")

            try:
                with open(file_path, 'w', newline='', encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Nombre", "Materia", "Nota1", "Nota2", "Nota3", "NotaFinal"])
                    writer.writerows(students)

                self.root.set_state("allow_save", False)
                self.root.set_state("file", {"path": file_path, "data": students})

            except Exception as e:
                messagebox.showerror("Error al guardar los cambios", f"Ocurrió un error al guardar los cambios:\n{e}")

    def on_click_save_as(self):

        file_path = asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
            title="Guardar como..."
            )

        if file_path:
            
            students = self.root.get_state("students")

            try:
                with open(file_path, 'w', newline='', encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Nombre", "Materia", "Nota1", "Nota2", "Nota3", "NotaFinal"])
                    writer.writerows(students)

                messagebox.showinfo("Archivo Guardado", f"Se ha guardado el archivo:\n{file_path}")

            except Exception as e:
                messagebox.showerror("Error al abrir el archivo", f"Ocurrió un error al abrir el archivo:\n{e}")

    def on_click_quit(self):

        if cancel_for_changes_protection(self.root):
            return
        
        self.root.quit()


    # EDIT
    def _create_edit_menu(self)->Menu:
        # Crear el menú "Editar" y sus opciones
        edit_menu = Menu(self, tearoff=0)
        
        edit_menu.add_command(label="Agregar alumno", command=lambda: AddStudentWindow(self.root))
        edit_menu.add_command(label="Eliminar alumno/s", command=self.on_click_delete_students, state=DISABLED)

        return edit_menu
    
    def on_click_delete_students(self):

        are_sure = messagebox.askyesno("Eliminar Alumno", "¿desea ELIMINAR los alumnos seleccionados?")
        
        if not(are_sure):
            return
        
        students_table = self.root.students_table

        students_data:list = self.root.get_state("students")

        for index in students_table.students_selected_index:
            students_data.pop(index)
            
        self.root.set_state("students", students_data)
    

    # ORDER
    def _create_order_menu(self)->Menu:

        # Crear el menú "Ayuda" y sus opciones
        order_menu = Menu(self, tearoff=0)
        
        order_menu.add_radiobutton(label="no ordenar", variable=self.root.order_by, value="unordered", command=self.on_click_order_by_option)
        order_menu.add_radiobutton(label="alfabetico", variable=self.root.order_by, value="alphabetical", command=self.on_click_order_by_option)
        order_menu.add_radiobutton(label="mejor promedio", variable=self.root.order_by, value="best_average", command=self.on_click_order_by_option)

        return order_menu

    def on_click_order_by_option(self):

        order_by = self.root.order_by.get()
        if order_by == self.root.last_order_by_selected:
            return
        
        students_ordered = order_by_dict[order_by](self.root.get_state("students"))

        self.root.set_state("students", students_ordered)

        self.root.last_order_by_selected = order_by


    # GENERATE REPORTS
    def _create_reports_menu(self)->Menu:

        generate_reports_menu = Menu(self, tearoff=0)

        generate_reports_menu.add_command(label="Tabla de alumnos", command=self.on_click_make_students_table_img)
        generate_reports_menu.add_command(label="Tabla de alumnos con al menos un examen desaprobado", command=self.on_click_make_one_subject_disapproved_students_table_img)
        generate_reports_menu.add_command(label="Tabla de alumnos aptos para promocionar", command=self.on_click_make_promotable_students_table_img)
        generate_reports_menu.add_command(label="Promedio de notas finales por materia", command=self.on_click_make_final_grade_averages_per_subject_report)
        generate_reports_menu.add_command(label="tabla de probados y desaprobados por materia", command=self.on_click_make_approved_unapproved_per_subject_table_img)

        return generate_reports_menu

    def on_click_make_students_table_img(self):

        path = asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Archivos PNG", "*.png"), ("Todos los archivos", "*.*")],
            title="Guardar como...",
            initialfile="Tabla_de_alumnos.png"
            )
        
        if not path:
            return
        
        students:list = copy.deepcopy(self.root.get_state("students"))
        students.insert(0, ["Nombre", "Materia", "Nota1", "Nota2", "Nota3", "NotaFinal"])
        
        make_img_from_matrix(path, students)

    def on_click_make_one_subject_disapproved_students_table_img(self):
        
        path = asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Archivos PNG", "*.png"), ("Todos los archivos", "*.*")],
            title="Guardar como...",
            initialfile="Tabla_de_alumnos_con_al_menos_una_desaprobada.png"
            )
        
        if not path:
            return
        
        students = self.root.get_state("students")

        filtred_students = [["Nombre", "Materia", "Nota1", "Nota2", "Nota3", "NotaFinal"]]
        
        for student in students:
            
            if student[2]:
                if int(student[2]) < int(self.root.settings["approve_at"]):
                    filtred_students.append(student)
                    continue

            if student[3]:
                if int(student[3]) < int(self.root.settings["approve_at"]):
                    filtred_students.append(student)
                    continue

            if student[4]:
                if int(student[4]) < int(self.root.settings["approve_at"]):
                    filtred_students.append(student)
                    continue
        
        make_img_from_matrix(path, filtred_students)

    def on_click_make_promotable_students_table_img(self):
        
        path = asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Archivos PNG", "*.png"), ("Todos los archivos", "*.*")],
            title="Guardar como...",
            initialfile="Tabla_de_alumnos_promocionables.png"
            )
        
        if not path:
            return
        
        students = self.root.get_state("students")

        filtred_students = [["Nombre", "Materia", "Nota1", "Nota2", "Nota3", "NotaFinal"]]
        for student in students:

            if student[2]:
                if int(student[2]) >= int(self.root.settings["promote_at"]):

                    if student[3]:
                        if int(student[3]) >= int(self.root.settings["promote_at"]):

                            if student[4]:
                                if int(student[4]) >= int(self.root.settings["promote_at"]):
                                    filtred_students.append(student)
                                    continue

                            else:
                                filtred_students.append(student)
                                continue
                    
                    else:
                        filtred_students.append(student)
                        continue
            
        
        make_img_from_matrix(path, filtred_students)

    def on_click_make_final_grade_averages_per_subject_report(self):

        path = asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Archivos PNG", "*.png"), ("Todos los archivos", "*.*")],
            title="Guardar como...",
            initialfile="Promedio_de_notas_finales_por_materia.png"
            )
        
        if not path:
            return
        
        data = self.root.get_state("students")

        averages_in_subject:dict[str,list[int]] = {}
        for student in data:
            
            subject = student[1]
            average = student[5]

            if not average:
                continue

            average = int(average)

            if not(subject in averages_in_subject.keys()):
                averages_in_subject[subject] = []
            
            averages_in_subject[subject].append(average)

        #x
        subjects = []
        #y
        averages_of_subjects = []

        for subject in averages_in_subject.keys():

            subjects.append(subject)
            averages_of_subjects.append( sum(averages_in_subject[subject]) / averages_in_subject[subject].__len__() )




        # Crear el gráfico de barras
        plt.figure(figsize=(10, 6))  # Define el tamaño de la figura
        plt.bar(subjects, averages_of_subjects, color='skyblue')  # Crea las barras

        # Añadir etiquetas y título
        plt.xlabel('Materia')
        plt.ylabel('Promedio')
        plt.title('Promedio de Notas Finales por materia')

        # Mostrar el gráfico
        plt.grid(axis='y', linestyle='--')  # Añade una cuadrícula horizontal opcional

        plt.savefig(path)
        plt.close()
    
    def on_click_make_approved_unapproved_per_subject_table_img(self):
        
        path = asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Archivos PNG", "*.png"), ("Todos los archivos", "*.*")],
            title="Guardar como...",
            initialfile="Tabla_de_aprobados_y_desaprobados_por_materia.png"
            )
        
        if not path:
            return
        
        students = self.root.get_state("students")

        subjects:dict[str, dict[Literal["total", "approve", "unapprove"], int]] = {}

        for student in students:
            if not (student[1] in subjects.keys()):
                subjects[student[1]] = {
                    "total": 0,
                    "approve": 0,
                    "unapprove": 0,
                }
            
            condition_list = [
                int(student[2]) >= int(self.root.settings["approve_at"]) if student[2] else None, 
                int(student[3]) >= int(self.root.settings["approve_at"]) if student[3] else None, 
                int(student[4]) >= int(self.root.settings["approve_at"]) if student[4] else None, 
            ]

            if condition_list[0] == None:
                continue

            if False in condition_list:
                subjects[student[1]]["total"] += 1
                subjects[student[1]]["unapprove"] += 1

            else:
                subjects[student[1]]["total"] += 1
                subjects[student[1]]["approve"] += 1


        filtred_subjects = [["Materia", "Aprobados", "Desaprobados", "Total"]]

        for subject in subjects.keys():
            filtred_subjects.append([subject, subjects[subject]["approve"], subjects[subject]["unapprove"], subjects[subject]["total"]])
        
        make_img_from_matrix(path, filtred_subjects)


    # SETTINGS
    def on_click_settings(self):

        if self.settings_window != None:
            return
        
        
        def on_close_settings():
            self.settings_window.destroy()
            self.settings_window = None
            
        def on_click_save_settings():
            self.root.settings["approve_at"] = str(int(approve_at.get()))
            self.root.settings["promote_at"] = str(int(promote_at.get()))
            self.root.save_settings()
            self.settings_window.destroy()
            self.settings_window = None

        self.settings_window = Toplevel()
        
        #self.settings_window.geometry("200x100")
        self.settings_window.config(padx="50", pady="10")
        self.settings_window.resizable(False, False)
        self.settings_window.title("Configuración")
        self.settings_window.protocol("WM_DELETE_WINDOW", on_close_settings)

        validate_grade_cmd = self.root.validateions_cmd["grade"]

        # approve
        approve_at = StringVar(value=str(self.root.settings["approve_at"]))

        approve_label = Label(self.settings_window, text="Se aprueba con:")
        approve_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        approve_input = Entry(self.settings_window, textvariable=approve_at, width=5, validate="key", validatecommand=validate_grade_cmd)
        approve_input.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        # promote
        promote_at = StringVar(value=str(self.root.settings["promote_at"]))

        promote_label = Label(self.settings_window, text="Se promociona con:")
        promote_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        promote_input = Entry(self.settings_window, textvariable=promote_at, width=5, validate="key", validatecommand=validate_grade_cmd)
        promote_input.grid(row=1, column=1, padx=10, pady=10, sticky="e")


        # save
        save_button = Button(self.settings_window, text="Guardar", command=on_click_save_settings )
        save_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    ##
    def on_update_allow_save(self, allow:bool):

        if allow:
            self.file_menu.entryconfig("Guardar", state=NORMAL)

        else:
            self.file_menu.entryconfig("Guardar", state=DISABLED)
    
    def on_update_students(self, students:list):

        if students:
            self.file_menu.entryconfig("Nuevo", state=NORMAL)
            self.file_menu.entryconfig("Guardar como...", state=NORMAL)

            file = self.root.get_state("file")
            
            have_changes = self.root.set_state("have_changes", students != file["data"])
            
            self.root.set_state("allow_save", file["path"] and have_changes)

            self.entryconfig("Generar informes", state=NORMAL)
            return

        self.file_menu.entryconfig("Nuevo", state=DISABLED)
        self.file_menu.entryconfig("Guardar como...", state=DISABLED)
        self.file_menu.entryconfig("Guardar", state=DISABLED)
        self.entryconfig("Generar informes", state=DISABLED)

    def on_update_allow_delete(self, allow:bool):

        if allow:
            self.edit_menu.entryconfig("Eliminar alumno/s", state=NORMAL)

        else:
            self.edit_menu.entryconfig("Eliminar alumno/s", state=DISABLED)
    