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
        window_width = 1200
        window_height = 600

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

        tk.Label(self.window, text="Type in the id of book to withdraw").grid(row=5, column=1, columnspan=2)
        self.id_withdraw = tk.Entry(self.window, width=40)
        self.id_withdraw.grid(row=6, column=1, columnspan=2)

        tk.Label(self.window, text="Type in the id of book to submit").grid(row=7, column=1, columnspan=2)
        self.id_submit = tk.Entry(self.window, width=40)
        self.id_submit.grid(row=8, column=1, columnspan=2)

        self.text_box = tk.Text(self.window, height=15, width=110, font=10)
        self.text_box.grid(row=4, column=2, columnspan=3, padx=10, pady=10)
        self.text_box.config(bg='#D9D8D8', state="disabled", font=('Courier', 10, 'italic'))

        self.sb = tk.Scrollbar(self.window, orient=tk.VERTICAL)
        self.sb.grid(row=4, column=5, sticky=tk.NS)
        self.text_box.config(yscrollcommand=self.sb.set)
        self.sb.config(command=self.text_box.yview)

    def buttons(self):

        self.submit_button = tk.Button(self.window, text="submit", command=self.submit)
        self.submit_button.grid(row=8, column=3, padx=10, pady=10)

        self.withdraw_button = tk.Button(self.window, text="Withdraw", command=self.withdraw)
        self.withdraw_button.grid(row=6, column=3, padx=10, pady=10)

        self.search_button = tk.Button(self.window, text="Search", command=self.search_data)
        self.search_button.grid(row=8, column=4, padx=10, pady=10)

        self.exit_button = tk.Button(self.window, text="Exit", command=self.window.destroy)
        self.exit_button.grid(row=8, column=5, padx=10, pady=10)

    # To set the availaible property of a book to no
    def withdraw(self):
        id = self.id_withdraw.get()
        self.id_withdraw.delete("0", "end")
        cur = self.db.cursor()
        cur.execute("""UPDATE books_table SET available=0 WHERE id={}""".format(id))

    # To set the availaible property of a book to yes
    def submit(self):
        id = self.id_submit.get()
        self.id_submit.delete("0", "end")
        cur = self.db.cursor()
        cur.execute("""UPDATE books_table SET available=1 WHERE id={}""".format(id))

    # To search data in the books.db file
    def search_data(self):

        self.text_box.config(state="normal")
        self.text_box.delete('1.0', "end")

        # To fetch the data from text box and save it in variables to use it for searching in database
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

        # search for data in the database and fetch the data from the database
        c = self.db.cursor()
        if self.book_n != '':
            c.execute("SELECT * from books_table where book=:book", {'book': self.book_n})
        elif self.author != '':
            c.execute("SELECT * from books_table where author=:author", {'author': self.author})
        elif self.publication != '':
            c.execute("SELECT * from books_table where publication=:publication", {'publication': self.publication})
        elif self.department != '':
            c.execute("SELECT * from books_table where department=:department", {'department': self.department})
        elif self.topic != '':
            c.execute("SELECT * from books_table where topic=:topic", {'topic': self.topic})
        self.book_data = list(c.fetchall())

        # To give prompt if no data is found
        if self.book_data == []:
            self.text_box.insert('1.0', "No books found")
            return

        # To check if the book is availaible in database
        def is_availaible():
            if book[5] == '1':
                return "yes"
            return "no"

        # To display the data in the window in a text box
        self.no = 1.0
        self.num = 1
        for book in self.book_data:
            self.text_box.insert(self.no,
                                 "{}] id:- {} Book:- {} author:- {} publication:- {} department:- {} \n".format(
                                     self.num, book[6], book[0], book[1],
                                     book[2], book[3]))

            self.text_box.insert(self.no + 1, "rack:- {} row:- {} column:- {} available;- {}\n".format(book[7],
                                                                                                       book[8], book[9],
                                                                                                       is_availaible()))
            self.no += 2
            self.num += 1

        self.text_box.config(state="disabled")
        self.book_data = []
