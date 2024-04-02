import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import csv

def calculate_age(birthdate):
    today = datetime.now()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def calculate_upcoming_birthdays():
    upcoming_birthdays = []
    for item in listbox_data.get_children():
        birthday_str, first_name, last_name, *_ = listbox_data.item(item, "values")
        birthday = datetime.strptime(birthday_str, "%d/%m/%Y").date()
        next_birthday = birthday.replace(year=datetime.now().year)
        if next_birthday < datetime.now().date():
            next_birthday = next_birthday.replace(year=datetime.now().year + 1)
        days_remaining = (next_birthday - datetime.now().date()).days
        upcoming_birthdays.append((next_birthday, days_remaining, first_name, last_name))
    return sorted(upcoming_birthdays, key=lambda x: x[0])

def calculate_upcoming_birthdays_from_csv():
    upcoming_birthdays = []
    with open("data.csv", newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            birthday_str, first_name, last_name, *_ = row
            birthday = datetime.strptime(birthday_str, "%d/%m/%Y").date()
            next_birthday = birthday.replace(year=datetime.now().year)
            if next_birthday < datetime.now().date():
                next_birthday = next_birthday.replace(year=datetime.now().year + 1)
            days_remaining = (next_birthday - datetime.now().date()).days
            upcoming_birthdays.append((next_birthday, days_remaining, first_name, last_name))
    return sorted(upcoming_birthdays, key=lambda x: x[0])

def generate_greeting():
    selected_item = listbox_data.selection()
    if not selected_item:
        return

    selected_values = listbox_data.item(selected_item[0], "values")
    first_name = selected_values[1]
    greeting = f"Happy Birthday, {first_name}!"
    greeting_text.config(state=tk.NORMAL)
    greeting_text.delete(1.0, tk.END)
    greeting_text.insert(tk.END, greeting)
    greeting_text.config(state=tk.DISABLED)

def update_upcoming_birthdays():
    upcoming_birthdays = calculate_upcoming_birthdays_from_csv()
    upcoming_birthdays_text.config(state=tk.NORMAL)
    upcoming_birthdays_text.delete(1.0, tk.END)
    for birthday, days_remaining, first_name, last_name in upcoming_birthdays:
        upcoming_birthdays_text.insert(tk.END, f"{birthday.strftime('%d/%m')} - {first_name} {last_name} - {days_remaining} days\n")
    upcoming_birthdays_text.config(state=tk.DISABLED)

def save_info():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    birthday = entry_birthday.get_date()
    age = calculate_age(birthday)
    data_entry = (birthday.strftime("%d/%m/%Y"), first_name, last_name, age)

    # Save the data to the CSV file
    with open("data.csv", "a", newline="") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",")
        csv_writer.writerow(data_entry)

    # Update the Treeview
    listbox_data.insert('', 'end', values=data_entry)

    # Update upcoming birthdays section
    update_upcoming_birthdays()

def load_data_from_csv():
    try:
        with open("data.csv", newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                listbox_data.insert('', 'end', values=row)
    except FileNotFoundError:
        pass


app = tk.Tk()
app.title("Birthday App")
app.geometry("1000x1000")

# Create a style for ttk widgets
style = ttk.Style()
style.configure("TLabel", padding=10)
style.configure("TEntry", padding=6)
style.configure("TButton", padding=8)

# Labels
label_first_name = ttk.Label(app, text="First Name:")
label_last_name = ttk.Label(app, text="Last Name:")
label_birthday = ttk.Label(app, text="Birthday:")

# Entry widgets
entry_first_name = ttk.Entry(app)
entry_last_name = ttk.Entry(app)

# DateEntry widget with a calendar format
entry_birthday = DateEntry(app, date_pattern='dd/mm/yyyy', showweeknumbers=False)

# Save button
btn_save = ttk.Button(app, text="Save", command=save_info)

# Treeview to display saved data with column names
columns = ("Birthday", "First Name", "Last Name", "Age")
listbox_data = ttk.Treeview(app, columns=columns, show="headings", selectmode="browse")
listbox_data.grid(row=4, column=0, columnspan=2, padx=10, pady=2, sticky="ew")

# Add column names to the Treeview
for col in columns:
    listbox_data.heading(col, text=col)
    listbox_data.column(col, width=100, anchor='center')

# Grid layout
label_first_name.grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_first_name.grid(row=0, column=1, padx=10, pady=5, sticky="w")
label_last_name.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_last_name.grid(row=1, column=1, padx=10, pady=5, sticky="w")
label_birthday.grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_birthday.grid(row=2, column=1, padx=10, pady=5, sticky="w")
btn_save.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Adjust column weights to expand horizontally
app.columnconfigure(0, weight=1)
app.columnconfigure(1, weight=1)

# Upcoming birthdays section
upcoming_birthdays_label = ttk.Label(app, text="Upcoming Birthdays:", font=("Helvetica", 12, "bold"))
upcoming_birthdays_label.grid(row=5, column=0, columnspan=2, padx=10, pady=2, sticky="w")

upcoming_birthdays_frame = ttk.Frame(app, padding=5, borderwidth=1, relief="solid")
upcoming_birthdays_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=2)

upcoming_birthdays_text = tk.Text(upcoming_birthdays_frame, width=45, height=4, state=tk.DISABLED, wrap=tk.WORD)
upcoming_birthdays_text.pack()

# Greeting message section
greeting_label = ttk.Label(app, text="Greeting:", font=("Helvetica", 12, "bold"))
greeting_label.grid(row=7, column=0, columnspan=2, padx=10, pady=2, sticky="w")

greeting_frame = ttk.Frame(app, padding=5, borderwidth=1, relief="solid")
greeting_frame.grid(row=8, column=0, columnspan=2, padx=10, pady=2)

greeting_text = tk.Text(greeting_frame, width=45, height=2, state=tk.DISABLED, wrap=tk.WORD)
greeting_text.pack()

# Generate Greetings button
btn_generate_greeting = ttk.Button(app, text="Generate Greeting", command=generate_greeting)
btn_generate_greeting.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

# Call function to load data from CSV and insert into the Treeview
load_data_from_csv()

# Update upcoming birthdays section
update_upcoming_birthdays()

app.mainloop()
