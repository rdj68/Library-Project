import tkinter as tk
import sqlite3 as sql

class SearchWindow:

    def __init__(self, parent, title):
        self.parent = parent
        self.window = tk.Toplevel()
        self.title = title

        self.is_location_panel_active = False
        self.book_data = None
        self.book_n = tk.StringVar()
        self.author = tk.StringVar()
        self.publication = tk.StringVar()
        self.department = tk.StringVar()
        self.topic = tk.StringVar()

        self.initialize()
        self.buttons()


        self.db = sql.connect("books.db")

    def initialize(self):
        # Set title
        self.window.title(self.title)

        # set the attributes of window
        window_width = 800
        window_height = 500

        # get the screen dimension
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int((screen_height / 2 - window_height / 2) - 100)

        # set the position of the window to the center of the screen
        self.window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.window.resizable(False, False)

        head = tk.Label(self.window, text=self.title, anchor="center")
        head.grid(row=0, column=3)

        # #######################################################################################################################
        tk.Label(self.window, text="Book Name").grid(row=1, column=1)
        self.book_tb = tk.Entry(self.window, width=40)
        self.book_tb.grid(row=1, column=2)

        tk.Label(self.window, text="Author Name").grid(row=2, column=1, padx=10, pady=10)
        self.author_tb = tk.Entry(self.window, width=40)
        self.author_tb.grid(row=2, column=2, padx=10, pady=10)

        tk.Label(self.window, text="Publication Name").grid(row=1, column=3, padx=10, pady=10)
        self.publication_tb = tk.Entry(self.window, width=40)
        self.publication_tb.grid(row=1, column=4, padx=10, pady=10)

        tk.Label(self.window, text="Department Name").grid(row=2, column=3, padx=10, pady=10)
        self.department_tb = tk.Entry(self.window, width=40)
        self.department_tb.grid(row=2, column=4, padx=10, pady=10)

        tk.Label(self.window, text="Topic").grid(row=3, column=1, padx=10, pady=10)
        self.topic_tb = tk.Entry(self.window, width=40)
        self.topic_tb.grid(row=3, column=2, padx=10, pady=10)

    def buttons(self):
        self.search_button = tk.Button(self.window, text="Search", command=self.search_data)
        self.search_button.grid(row=10, column=3, padx=10, pady=10)

        self.exit_button = tk.Button(self.window, text="Exit", command=self.window.destroy)
        self.exit_button.grid(row=10, column=4, padx=10, pady=10)


    def search_data(self):

        self.book_n = self.book_tb.get().lower()
        self.book_tb.delete("0", "end")

        self.author = self.author_tb.get().lower()
        self.author_tb.delete("0", "end")

        self.publication = self.publication_tb.get().lower()
        self.publication_tb.delete("0", "end")

        self.department = self.department_tb.get().lower()
        self.department_tb.delete("0", "end")

        self.topic = self.topic_tb.get().lower()
        self.topic_tb.delete("0", "end")


        c = self.db.cursor()

        c.execute("SELECT * from books_table where book=:book",{'book':self.book_n})
        self.book_data =list(c.fetchall()[0])
        tk.Label(self.window,text="Book {} author {} publication {} rack {}".format(self.book_data[0],
                                                                                   self.book_data[1],self.book_data[2],
                                                                                   self.book_data[5])).grid(row=11,column=2)

