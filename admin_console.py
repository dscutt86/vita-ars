
from tkinter import *
from tkinter import ttk
from enum import Enum, auto


def start_console():
    window = Tk()
    window.title("VITA ARS Admin Console")
    window.geometry("1020x800")
    return window


class FieldTitlePlacement(Enum):
    NONE = auto()
    TOP = auto()
    LEFT = auto()
    RIGHT = auto()
    BOTTOM = auto()


class FormField():
    def __init__(self, container, title:None|str, row:int, col:int):
        self.row = row
        self.col = col
        self.text_area = Entry(container)
        if title is not None:
            self.label = Label(container, text=title)
        else:
            self.label = None
    
    def show(self, placement:FieldTitlePlacement):
        match placement:
            case FieldTitlePlacement.NONE:
                self.text_area.grid(row=self.row, column=self.col)
                return
            case FieldTitlePlacement.TOP:
                self.label.grid(row=self.row, column=self.col)
                self.text_area.grid(row=self.row+1, column=self.col)
                return
            case FieldTitlePlacement.LEFT:
                self.label.grid(row=self.row, column=self.col)
                self.text_area.grid(row=self.row, column=self.col+1)
                return
            case FieldTitlePlacement.RIGHT:
                self.label.grid(row=self.row, column=self.col+1)
                self.text_area.grid(row=self.row, column=self.col)
                return
            case FieldTitlePlacement.BOTTOM:
                self.label.grid(row=self.row+1, column=self.col)
                self.text_area.grid(row=self.row, column=self.col)
                return
    
    def get_text(self):
        return self.text_area.get()
    
    def hide(self):
        if self.label is not None:
            self.label.grid_forget()
        self.text_area.grid_forget()
    
    def destroy(self):
        if self.label is not None:
            self.label.destroy()
        self.text_area.destroy()


class Console():
    def __init__(self, window):
        # Reference the console window
        self._window_ref = window

        # Window frame
        self.frame = ttk.Frame(
            window,
            borderwidth=2,
            relief="solid",
            padding=20
        )
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Login form fields
        self.login_username = None
        self.login_password = None
        self.login_button = None
        self.login_info = None

        # Admin menu
        self.menu_item = None

        self.quit_button = Button(
            self._window_ref,
            text="Quit",
            command=self._window_ref.destroy
        )
        self.quit_button.place(relx=1.0, x=-10, y=10, anchor="ne")

        # Show admin login on-start
        self.show_admin_login()
    
    # Show the admin login form
    def show_admin_login(self):
        # Create login fields
        self.login_username = FormField(self.frame, "Username", 0, 0)
        self.login_password = FormField(self.frame, "Password", 1, 0)
        # Show login fields
        self.login_username.show(FieldTitlePlacement.LEFT)
        self.login_password.show(FieldTitlePlacement.LEFT)
        # Show login button
        self.login_button = Button(
            self.frame,
            text = "Admin Login",
            command = self._poc_login
        )
        self.login_button.grid(row=2, column=0)

        # Proof of Concept Only - remove this for production development
        self.login_info = Label(
            self.frame,
            text="PoC - Username: 'admin'; Password: 'taxes'"
        )
        self.login_info.grid(row=3, column=0, columnspan=2)
    
    # Hide the admin login form
    def hide_admin_login(self):
        self.login_username.destroy()
        self.login_password.destroy()
        self.login_button.destroy()
        self.login_info.destroy()
    
    # Proof of Concept Login - later, will utilize cryptographically signed
    #   and stored credentials for authorized site coordinators.
    #   Cryptographically signed and stored credentials out of scope.
    def _poc_login(self):
        username = self.login_username.get_text()
        password = self.login_password.get_text()

        valid_username = "admin"
        valid_password = "taxes"

        if username == valid_username and password == valid_password:
            self.hide_admin_login()
            self.show_admin_menu()
            print(f"Login with {password} @ {username}")
            print("Future implementations will not utilize default logins.")
            print("Nor will they ever print login credentials to the terminal.")
        else:
            print(f"Login unsuccessful - {password} @ {username}")
    
    def show_admin_menu(self):
        self.menu_item = Label(
            self.frame,
            text="Welcome to the Admin Menu"
        )
        self.menu_item.grid(row=0, column=0)