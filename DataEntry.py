import tkinter as tk
import sqlite3 as sql



class DataEntry:
    def __init__(self, parent, title):
        # initializing all variables
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
        self.rack = tk.StringVar()
        self.row = tk.StringVar()
        self.column = tk.StringVar()

        self.db = sql.connect("books.db")
        self.cur = self.db.cursor()
        self.initialize()
        self.location_panel()
        self.buttons()


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
        # to create the various lables and text boxes and create the ui
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

    # creates the row column and rack labels and boxes
    def location_panel(self):
        tk.Label(self.window, text="Location").grid(row=4, column=1, padx=10, pady=10)

        tk.Label(self.window, text="Rack no").grid(row=5, column=1, padx=10, pady=10)
        self.rack_tb = tk.Entry(self.window, width=40)
        self.rack_tb.grid(row=5, column=2, padx=10, pady=10)

        tk.Label(self.window, text="Row no").grid(row=6, column=1, padx=10, pady=10)
        self.row_tb = tk.Entry(self.window, width=40)
        self.row_tb.grid(row=6, column=2, padx=10, pady=10)

        tk.Label(self.window, text="Column no").grid(row=5, column=3, padx=10, pady=10)
        self.column_tb = tk.Entry(self.window, width=40)
        self.column_tb.grid(row=5, column=4, padx=10, pady=10)

        self.no_of_book =tk.Label(self.window)
        self.no_of_book.grid(row=10,column=2)

        self.no_of_books=0
        self.cur.execute("SELECT book FROM books_table")
        for book in self.cur.fetchall():
            self.no_of_books +=1
        print(self.no_of_books)
        self.no_of_book.config(text="We have total {} books in library".format(self.no_of_books))

    # create the buttons and place them on the grid
    def buttons(self):
        self.submit_button = tk.Button(self.window, text="Submit", command=self.save_data)
        self.submit_button.grid(row=10, column=3, padx=10, pady=10)

        self.exit_button = tk.Button(self.window, text="Exit", command=self.window.destroy)
        self.exit_button.grid(row=10, column=4, padx=10, pady=10)

    # A prompt window to be used when all mandatory data is not filled
    def prompt(self):
        self.prompt_window = tk.Toplevel()
        # set the attributes of window
        window_width = 200
        window_height = 100

        # get the screen dimension
        screen_width = self.prompt_window.winfo_screenwidth()
        screen_height = self.prompt_window.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int((screen_height / 2 - window_height / 2) - 100)

        # set the position of the window to the center of the screen
        self.prompt_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.prompt_window.resizable(False, False)

        tk.Label(self.prompt_window, text="Please enter mandatory data").pack(anchor="center")
        tk.Button(self.prompt_window, text="Close", command=self.prompt_window.destroy).pack(anchor="s")

    # A function to save the data
    def save_data(self):

        # fetching data from the text boxes
        self.book_n = self.book_tb.get().lower()
        self.author = self.author_tb.get().lower()
        self.publication = self.publication_tb.get().lower()
        self.department = self.department_tb.get().lower()
        self.topic = self.topic_tb.get().lower()
        self.rack = self.rack_tb.get().lower()
        self.row = self.row_tb.get().lower()
        self.column = self.column_tb.get().lower()


        # To check if the books_table exists if not then create one
        self.cur.execute("""SELECT count(name) FROM sqlite_master WHERE type='table' AND name='books_table'""")
        if self.cur.fetchone()[0] == 0:
            self.cur.execute("""CREATE TABLE books_table(
                            book text,
                            author text,
                            publication text,
                            department text,
                            topic text,
                            available text,
                            id integer,
                            rack integer,
                            row integer,
                            column integer
                            )""")
            self.db.commit()

        if self.book_n == '' or self.rack == '' or self.row == '' or self.column == '':
            self.prompt()
            return


        print(self.no_of_books)
        self.no_of_book.config(text=self.no_of_books)
        self.cur.execute(
            "INSERT INTO books_table VALUES (:book,:author,:publication,:department,:topic,:availaible,:id,:rack,:row,"
            ":column)",
            {'book': self.book_n, 'author': self.author, 'publication': self.publication,
             'department': self.department, 'topic': self.topic,'availaible':1,'id':5250+self.no_of_books, 'rack': self.rack, 'row': self.row,
             'column': self.column})
        self.db.commit()

        # To clear all the text in text boxes for new data to be filled

        '''self.book_tb.delete("0", "end")
        self.author_tb.delete("0", "end")
        self.publication_tb.delete("0", "end")
        self.department_tb.delete("0", "end")
        self.topic_tb.delete("0", "end")
        self.rack_tb.delete("0", "end")
        self.row_tb.delete("0", "end")
        self.column_tb.delete("0", "end")'''

