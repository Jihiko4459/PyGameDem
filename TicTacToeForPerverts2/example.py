import tkinter as tk
from tkinter import messagebox

def open_dialog():
    root = tk.Tk()
    root.title("Dialog Window")

    def analyze_response(response):
        if response:
            print("User selected Yes")
            # Add your code here to handle the "Yes" response
        else:
            print("User selected No")
            # Add your code here to handle the "No" response

    def button_clicked():
        response = messagebox.askyesno("Question", "Do you want to proceed?")
        analyze_response(response)

    button = tk.Button(root, text="Ask Question", command=button_clicked)
    button.pack()

    root.mainloop()

open_dialog()