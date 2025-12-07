# main.py
import sys
import traceback
from ui.dashboard_librarian import LibrarianDashboard
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)

try: 
    from dao.user_dao import UserDAO
    from ui.dashboard_librarian import LibrarianDashboard
    from ui.dashboard_member import MemberDashboard
    print("DEBUG: All modules imported successfully!")
except ImportError as e:
    print(f"DEBUG: Import error - {e}")
    # Fallback: Create dummy classes if modules missing
    class UserDAO:
        @staticmethod
        def login(username, password):
            print(f"DEBUG: Fake login for '{username}'")
            if username == "admin@limkokwing.edu" and password == "admin123":
                class FakeUser:
                    username = username
                    def is_librarian(self): return True
                return FakeUser()
            return None

    class LibrarianDashboard(QWidget):
        def __init__(self, user):
            super().__init__()
            self.setWindowTitle(f"Fallback Librarian: {user.username}")
            layout = QVBoxLayout()
            layout.addWidget(QLabel("Librarian Dashboard - Working! (Fallback)"))
            self.setLayout(layout)

    class MemberDashboard(QWidget):
        def __init__(self, user):
            super().__init__()
            self.setWindowTitle(f"Fallback Member: {user.username}")
            layout = QVBoxLayout()
            layout.addWidget(QLabel("Member Dashboard - Working! (Fallback)"))
            self.setLayout(layout)
    print("DEBUG: Using fallback modules")

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Library - Login")
        self.setGeometry(500, 400, 400, 500)
        self.setStyleSheet("background-color: #2ECCF0;")

        layout = QVBoxLayout()

        title = QLabel("SMART LIBRARY LOGIN")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username (email)")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("LOGIN")
        login_btn.setStyleSheet("background-color: #3498db; color: Black; padding: 12px; font-size: 18px;")
        login_btn.clicked.connect(self.handle_login)

        layout.addWidget(title)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password)
        layout.addWidget(login_btn)
        self.setLayout(layout)

    def handle_login(self):
        print(f"DEBUG: Login attempt - Username: {self.username_input.text().strip()}")
        try:
            user = UserDAO.login(self.username_input.text().strip(), self.password.text())
            print(f"DEBUG: Login result → {user} (type: {type(user)})")

            if not user:
                QMessageBox.critical(self, "Login Failed", "Invalid username or password!")
                return

            self.close()
            print("DEBUG: Login successful! Opening correct dashboard...")


            is_librarian = False

            # Case 1: Dictionary with "role" key (most common in real projects)
            if isinstance(user, dict):
                role = user.get("role", "").lower()
                if role == "librarian":
                    is_librarian = True

            # Case 2: Object with .role attribute
            elif hasattr(user, "role"):
                is_librarian = (str(getattr(user, "role")).lower() == "librarian")

            # Case 3: Your fallback FakeUser with is_librarian() method
            elif hasattr(user, "is_librarian") and callable(getattr(user, "is_librarian", None)):
                is_librarian = user.is_librarian()

            # Final decision
            if is_librarian:
                print("Opening LIBRARIAN Dashboard")
                self.librarian_win = LibrarianDashboard(user)
                self.librarian_win.show()
            else:
                print("Opening MEMBER Dashboard")   # ← This will now appear!
                self.member_win = MemberDashboard(user)
                self.member_win.show()
            # ─────────────────────────────────────────────────────────────────────

        except Exception as e:
            error_msg = f"Login error: {str(e)}\n\nDetails:\n{traceback.format_exc()}"
            print(error_msg)
            QMessageBox.critical(self, "Error", error_msg)

if __name__ == "__main__":
    print("DEBUG: Starting app...")
    app = QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    print("DEBUG: Login window shown. Run 'python main.py' and check console for logs.")
    sys.exit(app.exec_())