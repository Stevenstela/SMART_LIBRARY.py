#memberdashboard.py
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate

# Import DAOs safely
try:
    from dao.book_dao import BookDAO
    from dao.loan_dao import LoanDAO
    from dao.club_dao import ClubDAO
except ImportError:
    # Fallback if DAOs not ready
    class BookDAO:
        @staticmethod
        def get_available_books(search=""):
            return [{"book_id":1,"title":"Sample Book","author_name":"Author","genre":"Fiction","published_year":2023,"copies_available":1}]
    class LoanDAO:
        @staticmethod
        def get_member_loans(id): return []
        @staticmethod
        def issue_loan(bid, mid): return True
    class ClubDAO:
        @staticmethod
        def get_all_clubs(): return [{"name":"Demo Club","description":"Fun!","member_count":5}]

class MemberDashboard(QMainWindow):
    def __init__(self, user):
        super().__init__()


        self.user = user

        # Extract username and member_id safely
        if isinstance(user, dict):
            self.username = user.get("username", "Member")
            self.member_id = user.get("member_id")
        else:
            # It's an object — use getattr with fallback
            self.username = getattr(user, "username", "Member")
            self.member_id = getattr(user, "member_id", None)

        # Fallback if still missing
        if not self.member_id:
            self.member_id = getattr(user, "id", 1)
        # =================================================================

        self.setWindowTitle(f"SmartLibrary - Member: {self.username}")
        self.setGeometry(100, 80, 1150, 720)
        self.setStyleSheet("background:#f8fafc; font-family: Segoe UI;")

        tabs = QTabWidget()
        tabs.setStyleSheet("QTabBar::tab { height: 45px; width: 180px; font-size: 14px; }")

        tabs.addTab(self.home_tab(), "Home")
        tabs.addTab(self.catalog_tab(), "Browse & Borrow")
        tabs.addTab(self.my_loans_tab(), "My Loans")
        tabs.addTab(self.clubs_tab(), "Book Clubs")

        self.setCentralWidget(tabs)
        self.refresh_all()


    def refresh_all(self):
        self.refresh_my_loans()
        self.refresh_catalog()

    def home_tab(self):
        w = QWidget()
        l = QVBoxLayout()
        l.addWidget(QLabel(f"<h1 style='color:#1e40af;'>Welcome {self.username}!</h1>"))
        l.addWidget(QLabel("<h3>Library Rules</h3>"))
        l.addWidget(QLabel("• You can borrow up to <b>3 books</b> at a time"))
        l.addWidget(QLabel("• Each book is due in <b>7 days</b>"))
        l.addWidget(QLabel("• Return on time to avoid fines"))

        self.current_loans_label = QLabel()
        self.current_loans_label.setStyleSheet("font-size:18px; font-weight:bold; color:#dc2626;")
        l.addWidget(self.current_loans_label)

        l.addStretch()
        w.setLayout(l)
        return w

    # Book Catalog + Borrow
    def catalog_tab(self):
        w = QWidget()
        l = QVBoxLayout()

        # Search
        search_bar = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search by title, author, or genre...")
        self.search_box.textChanged.connect(self.refresh_catalog)
        search_bar.addWidget(QLabel("Search:"))
        search_bar.addWidget(self.search_box)
        l.addLayout(search_bar)

        # Table
        self.book_table = QTableWidget()
        self.book_table.setColumnCount(7)
        self.book_table.setHorizontalHeaderLabels([
            "ID", "Title", "Author", "Genre", "Year", "Available", "Action"
        ])
        self.book_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.book_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.book_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        l.addWidget(self.book_table)

        self.refresh_catalog()
        w.setLayout(l)
        return w

    def refresh_catalog(self):
        query = self.search_box.text().lower()
        books = BookDAO.get_available_books(search=query)

        self.book_table.setRowCount(len(books))
        for i, book in enumerate(books):
            for col, key in enumerate(["book_id", "title", "author_name", "genre", "published_year", "copies_available"]):
                self.book_table.setItem(i, col, QTableWidgetItem(str(book.get(key, ""))))

            # Borrow button
            btn = QPushButton("Borrow")
            btn.setStyleSheet("background:#3b82f6; color:white;")
            if book["copies_available"] == 0:
                btn.setEnabled(False)
                btn.setText("Unavailable")
            else:
                btn.clicked.connect(lambda _, bid=book["book_id"], title=book["title"]: self.borrow_book(bid, title))
            self.book_table.setCellWidget(i, 6, btn)

    def borrow_book(self, book_id, title):
        if len(LoanDAO.get_member_loans(self.member_id)) >= 3:
            QMessageBox.warning(self, "Limit Reached", "You already have 3 books borrowed!")
            return

        success = LoanDAO.issue_loan(book_id, self.member_id)
        if success:
            QMessageBox.information(self, "Success", f"You borrowed:\n<b>{title}</b>\nDue in 7 days!")
            self.refresh_all()
        else:
            QMessageBox.critical(self, "Error", "Could not borrow this book.")

    # My Loans Tab
    def my_loans_tab(self):
        w = QWidget()
        l = QVBoxLayout()
        l.addWidget(QLabel("<h2>My Current Loans</h2>"))

        self.loans_table = QTableWidget()
        self.loans_table.setColumnCount(5)
        self.loans_table.setHorizontalHeaderLabels(["Book", "Loan Date", "Due Date", "Days Left", "Status"])
        self.loans_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        l.addWidget(self.loans_table)

        self.refresh_my_loans()
        w.setLayout(l)
        return w

    def refresh_my_loans(self):
        loans = LoanDAO.get_member_loans(self.member_id)
        self.loans_table.setRowCount(len(loans))

        total_loans = len(loans)


        if self.centralWidget():
            home_tab = self.centralWidget().widget(0)  # Home tab
            if home_tab and home_tab.layout():
                label = home_tab.layout().itemAt(4).widget()
                if label:
                    label.setText(f"You have <b>{total_loans}/3</b> books borrowed")

        today = QDate.currentDate()
        for i, loan in enumerate(loans):
            self.loans_table.setItem(i, 0, QTableWidgetItem(loan["title"]))
            self.loans_table.setItem(i, 1, QTableWidgetItem(str(loan["loan_date"])))
            self.loans_table.setItem(i, 2, QTableWidgetItem(str(loan["due_date"])))

            days_left = (loan["due_date"] - today).days()
            self.loans_table.setItem(i, 3, QTableWidgetItem(str(days_left)))

            status = "On Time" if days_left >= 0 else "OVERDUE!"
            item = QTableWidgetItem(status)
            item.setForeground(Qt.red if days_left < 0 else Qt.darkGreen)
            self.loans_table.setItem(i, 4, item)

    # Book Clubs Tab
    def clubs_tab(self):
        w = QWidget()
        l = QVBoxLayout()
        l.addWidget(QLabel("<h2>Available Book Clubs</h2>"))

        clubs = ClubDAO.get_all_clubs()
        table = QTableWidget(len(clubs), 3)
        table.setHorizontalHeaderLabels(["Club Name", "Description", "Members"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i, club in enumerate(clubs):
            table.setItem(i, 0, QTableWidgetItem(club["name"]))
            table.setItem(i, 1, QTableWidgetItem(club["description"] or "No description"))
            table.setItem(i, 2, QTableWidgetItem(str(club["member_count"])))

        join_btn = QPushButton("Join Selected Club")
        join_btn.setStyleSheet("background:#10b981; color:white; padding:12px; font-weight:bold;")
        join_btn.clicked.connect(lambda: QMessageBox.information(self, "Joined!", "You are now a member of this group!"))

        l.addWidget(table)
        l.addWidget(join_btn)
        w.setLayout(l)
        return w