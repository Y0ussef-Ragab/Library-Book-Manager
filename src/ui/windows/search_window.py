from tkinter import ttk


class SearchWindow(ttk.Frame):
    def __init__(self, parent: ttk.Frame, store) -> None:
        super().__init__(parent)
        self.store = store

        style = ttk.Style(self)
        style.configure("Books.Treeview", rowheight=28, font=("Helvetica", 10))
        style.configure("Books.Treeview.Heading", font=("Helvetica", 10, "bold"))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        ttk.Label(self, text="Search Books", style="Title.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 10)
        )

        top = ttk.Frame(self)
        top.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        top.columnconfigure(0, weight=1)

        self.search_entry = ttk.Entry(top)
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ttk.Button(top, text="Search", command=self.refresh).grid(row=0, column=1)

        table_frame = ttk.Frame(self)
        table_frame.grid(row=2, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("id", "title", "author", "year", "status"),
            show="headings",
            style="Books.Treeview",
        )
        self.tree.grid(row=0, column=0, sticky="nsew")

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        y_scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=y_scroll.set)

        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("author", text="Author")
        self.tree.heading("year", text="Year")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=50, anchor="center", stretch=False)
        self.tree.column("title", width=280, stretch=True)
        self.tree.column("author", width=220, stretch=True)
        self.tree.column("year", width=80, anchor="center", stretch=False)
        self.tree.column("status", width=110, anchor="center", stretch=False)

    def refresh(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        keyword = self.search_entry.get().strip()
        books = self.store.search_books(keyword)

        for book in books:
            status = "Borrowed" if book.is_borrowed else "Available"
            self.tree.insert(
                "",
                "end",
                values=(book.book_id, book.title, book.author, book.year, status),
            )
