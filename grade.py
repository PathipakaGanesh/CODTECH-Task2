import tkinter as tk
from tkinter import messagebox, font

class GradeManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grade Tracker")

        # Set window size and center it
        window_width = 400
        window_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        # Initialize data
        self.grades = []
        self.current_subject_index = 0

        # UI Elements
        self.create_initial_ui()

    def create_initial_ui(self):
        title_font = font.Font(family="Arial", size=16, weight="bold")
        label_font = font.Font(family="Arial", size=12)
        entry_font = font.Font(family="Arial", size=12)

        # User Name
        self.name_label = tk.Label(self.root, text="Enter your name:", font=label_font, fg="darkred")
        self.name_label.grid(row=0, column=0, sticky="e", padx=5, pady=10)

        self.name_entry = tk.Entry(self.root, font=entry_font)
        self.name_entry.grid(row=0, column=1, padx=5, pady=10)

        # Number of Subjects
        self.num_subjects_label = tk.Label(self.root, text="Enter number of subjects:", font=label_font, fg="darkgreen")
        self.num_subjects_label.grid(row=1, column=0, sticky="e", padx=5, pady=10)

        self.num_subjects_entry = tk.Entry(self.root, font=entry_font)
        self.num_subjects_entry.grid(row=1, column=1, padx=5, pady=10)

        # Next button
        self.next_button = tk.Button(self.root, text="Next", command=self.initialize_subject_entry, font=label_font, bg="orange", fg="white")
        self.next_button.grid(row=2, column=0, columnspan=2, pady=10)

    def initialize_subject_entry(self):
        self.user_name = self.name_entry.get()
        try:
            self.num_subjects = int(self.num_subjects_entry.get())
            if self.num_subjects > 0:
                self.clear_initial_ui()
                self.create_subject_ui()
            else:
                messagebox.showerror("Invalid Input", "Number of subjects should be greater than 0")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the number of subjects")

    def clear_initial_ui(self):
        self.name_label.grid_forget()
        self.name_entry.grid_forget()
        self.num_subjects_label.grid_forget()
        self.num_subjects_entry.grid_forget()
        self.next_button.grid_forget()

    def create_subject_ui(self):
        label_font = font.Font(family="Arial", size=12)
        entry_font = font.Font(family="Arial", size=12)

        # Subject Name
        self.subject_label = tk.Label(self.root, text="Enter subject name:", font=label_font, fg="darkred")
        self.subject_label.grid(row=0, column=0, sticky="e", padx=5, pady=10)

        self.subject_entry = tk.Entry(self.root, font=entry_font)
        self.subject_entry.grid(row=0, column=1, padx=5, pady=10)

        # Grade
        self.grade_label = tk.Label(self.root, text="Enter grade:", font=label_font, fg="darkgreen")
        self.grade_label.grid(row=1, column=0, sticky="e", padx=5, pady=10)

        self.grade_entry = tk.Entry(self.root, font=entry_font)
        self.grade_entry.grid(row=1, column=1, padx=5, pady=10)

        # Add button
        self.add_button = tk.Button(self.root, text="Add Grade", command=self.add_grade, font=label_font, bg="orange", fg="white")
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

    def add_grade(self):
        subject = self.subject_entry.get()
        try:
            grade = float(self.grade_entry.get())
            if 0 <= grade <= 100:
                self.grades.append((subject, grade))
                self.subject_entry.delete(0, tk.END)
                self.grade_entry.delete(0, tk.END)
                self.current_subject_index += 1
                if self.current_subject_index == self.num_subjects:
                    self.clear_subject_ui()
                    self.calculate_average()
            else:
                messagebox.showerror("Invalid Input", "Grade should be between 0 and 100")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the grade")

    def clear_subject_ui(self):
        self.subject_label.grid_forget()
        self.subject_entry.grid_forget()
        self.grade_label.grid_forget()
        self.grade_entry.grid_forget()
        self.add_button.grid_forget()

    def calculate_average(self):
        total = sum(grade for subject, grade in self.grades)
        average = total / len(self.grades)
        
        letter_grade = self.get_letter_grade(average)
        cgpa = self.get_cgpa(average)

        title_font = font.Font(family="Arial", size=16, weight="bold")
        label_font = font.Font(family="Arial", size=12)
        result_font = font.Font(family="Arial", size=12, weight="bold")

        result_frame = tk.Frame(self.root, padx=10, pady=10)
        result_frame.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        self.result_label = tk.Label(result_frame, text="Result Summary", font=title_font, fg="darkred")
        self.result_label.pack()

        info_frame = tk.Frame(result_frame)
        info_frame.pack(anchor="center", pady=5)

        self.create_info_row(info_frame, "Student", ":", self.user_name, "darkblue")
        self.create_info_row(info_frame, "Average Grade", ":", f"{average:.2f}", "darkgreen")
        self.create_info_row(info_frame, "Letter Grade", ":", letter_grade, "purple")
        self.create_info_row(info_frame, "CGPA", ":", f"{cgpa:.2f}", "darkorange")

        subjects_header = tk.Label(result_frame, text="Subjects and Grades:", font=result_font, fg="black")
        subjects_header.pack(anchor="center", pady=5)

        for subject, grade in self.grades:
            subject_grade_frame = tk.Frame(result_frame)
            subject_grade_frame.pack(anchor="center", pady=2)

            subject_label = tk.Label(subject_grade_frame, text=subject, font=result_font, fg="darkgreen")
            subject_label.pack(side="left", padx=10)

            grade_label = tk.Label(subject_grade_frame, text=f"{grade}", font=result_font, fg="darkred")
            grade_label.pack(side="left", padx=10)

    def create_info_row(self, parent, label_text, colon_text, value_text, fg_color):
        row_frame = tk.Frame(parent)
        row_frame.pack(anchor="center", pady=5)

        label = tk.Label(row_frame, text=label_text, font=("Arial", 12, "bold"), fg=fg_color)
        label.pack(side="left", padx=5)

        label_spacing = " " * (max(0, 20 - len(label_text)))
        label_space = tk.Label(row_frame, text=label_spacing, font=("Arial", 12, "bold"), fg=fg_color)
        label_space.pack(side="left", padx=5)

        colon = tk.Label(row_frame, text=colon_text, font=("Arial", 12, "bold"), fg=fg_color)
        colon.pack(side="left", padx=5)

        colon_spacing = " " * (max(0, 5 - len(colon_text)))
        colon_space = tk.Label(row_frame, text=colon_spacing, font=("Arial", 12, "bold"), fg=fg_color)
        colon_space.pack(side="left", padx=5)

        value_space = " " * (max(0, 20 - len(value_text)))
        value = tk.Label(row_frame, text=value_space + value_text, font=("Arial", 12, "bold"), fg=fg_color)
        value.pack(side="right", padx=5)

    def get_letter_grade(self, average):
        if average >= 90:
            return 'A'
        elif average >= 80:
            return 'B'
        elif average >= 70:
            return 'C'
        elif average >= 60:
            return 'D'
        else:
            return 'F'
    
    def get_cgpa(self, average):
        if average >= 90:
            return 4.0
        elif average >= 80:
            return 3.0
        elif average >= 70:
            return 2.0
        elif average >= 60:
            return 1.0
        else:
            return 0.0

if __name__ == "__main__":
    root = tk.Tk()
    app = GradeManager(root)
    root.mainloop()
