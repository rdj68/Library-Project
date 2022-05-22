import tkinter as tk
import DataEntry as de
import SearchWindow as se

root = tk.Tk()
root.withdraw()

def welcome_window():
    welcome_win = tk.Toplevel()

    # Set title
    welcome_win.title("Welcome")

    # set the attributes of window
    window_width = 300
    window_height = 150

    # get the screen dimension
    screen_width = welcome_win.winfo_screenwidth()
    screen_height = welcome_win.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int((screen_height / 2 - window_height / 2) - 100)

    # set the position of the window to the center of the screen
    welcome_win.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    welcome_win.resizable(False, False)

    data_entry_button = tk.Button(welcome_win, text="Data Entry", command=data_entry).pack(pady=5,padx=10)
    search_window_button = tk.Button(welcome_win, text="Search Window", command=search).pack(pady=5)
    exit_button = tk.Button(welcome_win, text="Exit", command=welcome_win.quit).pack(pady=5)



def data_entry():
    # create data entry window
    data_entry_win = de.DataEntry(root, "Data Entry")

def search():
    search_win = se.SearchWindow(root,"Search")

welcome_window()

root.mainloop()
