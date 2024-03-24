import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedStyle



class TimetableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timetable Tool")

        style = ThemedStyle(self.root)
        style.set_theme("adapta")  # You can try different themes

        self.file_path_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.department_var = tk.StringVar()
        self.selected_courses = []

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.grid(row=0, column=0, padx=20, pady=20)

        file_path_label = ttk.Label(frame, text="Enter CSV File Path:")
        file_path_entry = ttk.Entry(frame, textvariable=self.file_path_var, width=40)
        browse_button = ttk.Button(frame, text="Browse", command=self.browse_file)

        year_label = ttk.Label(frame, text="Select Year:")
        year_options = [str(i) for i in range(1, 6)]  # Options: 1 to 5
        year_combobox = ttk.Combobox(frame, textvariable=self.year_var, values=year_options, state="readonly")

        department_label = ttk.Label(frame, text="Select Department:")
        department_options = ['CHI', 'CS', 'ECE', 'ECON', 'EE', 'EECS', 'ENGR', 'FRE', 'GER', 'IE', 'ISE', 'LIFE', 'MATH', 'MGT', 'UNI']
        department_combobox = ttk.Combobox(frame, textvariable=self.department_var, values=department_options, state="readonly")

        display_button = ttk.Button(frame ,text="Display", command=self.display_timetable, )
        clear_button = ttk.Button(frame, text="Clear", command=self.clear_timetable)
        save_button = ttk.Button(frame, text="Save", command=self.save_timetable)

        self.course_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, height=10, width=50,exportselection=0, borderwidth=0, highlightthickness=0, selectborderwidth=0)
        self.selected_courses_label = tk.Text(frame, wrap=tk.WORD, height=10, width=40)
        self.selected_courses_label.insert(tk.END, "Selected Courses:")
        self.selected_courses_label.config(state=tk.DISABLED)

        self.warning_label = ttk.Label(frame, text="")

        file_path_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        file_path_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        browse_button.grid(row=0, column=2, padx=10, pady=10, sticky=tk.W)

        year_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        year_combobox.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        department_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        department_combobox.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        display_button.grid(row=3, column=0, padx=10, pady=10)
        clear_button.grid(row=3, column=1, padx=10, pady=10)
        save_button.grid(row=3, column=2, padx=10, pady=10)

        self.course_listbox.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky=tk.W)
        self.selected_courses_label.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)

        self.warning_label.grid(row=5, column=0, columnspan=3, pady=10)

        self.course_listbox.bind('<<ListboxSelect>>', self.update_selected_courses)

        # Add some border radius to the Listbox
        self.root.after(1, lambda: self.course_listbox.configure(borderwidth=1))

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        self.file_path_var.set(file_path)

    def display_timetable(self):
        file_path = self.file_path_var.get()
        year = self.year_var.get()
        department = self.department_var.get()

        if not file_path:
            self.warning_label.config(text="Please choose a CSV file.")
            return
        else:
            self.warning_label.config(text="")

        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                courses = [line.strip() for line in lines if
                           line.startswith(department + " ") and line.split(',')[0][-3] == year]

                if not courses:
                    self.warning_label.config(text="There is no course that suits your requirements.")
                else:
                    # Display the courses in listbox
                    self.course_listbox.delete(0, tk.END)
                    for course in courses:
                        self.course_listbox.insert(tk.END, course)

        except Exception as e:
            self.warning_label.config(text=f"Error reading CSV file: {str(e)}")

    def clear_timetable(self):
        self.course_listbox.delete(0, tk.END)
        self.clear_selected_courses_label()
        self.warning_label.config(text="Timetable cleared.")

    def save_timetable(self):
        selected_courses = self.course_listbox.curselection()

        if not selected_courses:
            self.warning_label.config(text="No courses selected. Add courses before saving.")
            return
        elif len(selected_courses) > 6:
            self.warning_label.config(text="Select at most 6 courses.")
            return
        else:
            self.warning_label.config(text="")

        try:
            with open('timetable.csv', 'w') as file:
                for course_index in selected_courses:
                    course = self.course_listbox.get(course_index)
                    file.write(f"{course}\n")

            self.warning_label.config(text="Timetable saved to 'timetable.csv'.")
            self.course_listbox.delete(0, tk.END)  # Clear the courses
            self.clear_selected_courses_label()

        except Exception as e:
            self.warning_label.config(text=f"Error saving timetable: {str(e)}")

    def update_selected_courses(self, event):
        selected_courses_indices = self.course_listbox.curselection()
        selected_courses_text = "\n".join([f"Added \"{self.course_listbox.get(i)}\"" for i in selected_courses_indices])
        self.selected_courses_label.config(state=tk.NORMAL)
        self.selected_courses_label.delete(1.0, tk.END)
        self.selected_courses_label.insert(tk.END, f"Selected Courses:\n{selected_courses_text}")
        self.selected_courses_label.config(state=tk.DISABLED)

    def clear_selected_courses_label(self):
        self.selected_courses_label.config(state=tk.NORMAL)
        self.selected_courses_label.delete(1.0, tk.END)
        self.selected_courses_label.insert(tk.END, "Selected Courses:")
        self.selected_courses_label.config(state=tk.DISABLED)

# Main Section
if __name__ == "__main__":
    root = tk.Tk()
    app = TimetableApp(root)
    root.mainloop()