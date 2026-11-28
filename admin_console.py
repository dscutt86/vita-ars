
from tkinter import *
from tkinter import ttk
from enum import Enum, auto
from functools import partial


def start_console():
    window = Tk()
    window.title("VITA ARS Admin Console")
    window.geometry("1020x800")
    return window


def convert_month_code(code):
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    return months[code]


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
    def __init__(self, window, db):
        # Reference the console window
        self._window_ref = window

        # Database reference
        self._db = db

        # Window frame - allows us to contain and position elements as a group
        self.frame = ttk.Frame(
            window,
            borderwidth=2,
            relief="solid",
            padding=20
        )
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Window elements - the things we put into the window and frame
        self.elements = []

        # Quit Button
        self.quit_button = Button(
            self._window_ref,
            text="Quit",
            command=self._window_ref.destroy
        )
        self.quit_button.place(relx=1.0, x=-10, y=10, anchor="ne")

        # Show admin login on-start
        self.show_login_menu()
    

    # Destroy all elements and start fresh
    def destroy_elements(self):
        try:
            for element in self.elements:
                element.destroy()
            self.elements = []
        except Exception as err:
            print(f"destroy_elements() failed: {err}")
            raise
    

    # Sift through search results
    def sift_search_results(self, results, key, value):
        sifted = []
        for result in results:
            if result[key] == value:
                sifted.append(result)
        return sifted
    

    # Create form
    def create_form(
        self,
        element_data:[[str]],
        starting_row
    ):
        self.destroy_elements()
        elements = []
        current_row = starting_row
        for data in element_data:
            element = None
            colspan = 1
            match data[0]:
                case "label":
                    if len(data) == 3:
                        colspan = data[2]
                    element = Label(self.frame, text=data[1])
                    element.grid(row=current_row, column=0, columnspan=colspan)
                    current_row += 1
                case "field":
                    element = FormField(self.frame, data[1], current_row, 0)
                    element.show(FieldTitlePlacement.LEFT)
                    current_row += 1
                case "button":
                    element = Button(
                        self.frame,
                        text=data[1],
                        command=data[2]
                    )
                    element.grid(row=current_row, column=0)
                    current_row += 1
            
            # Insert into own elements
            if element is not None:
                current_row += 1
                self.elements.append(element)


    """
            LOGIN and LOGOUT METHODS
    """

    # Show the login menu
    def show_login_menu(self):
        # Login Fields
        self.create_form(
            [
                ["field", "Username"],
                ["field", "Password"],
                ["button", "Log In", self._poc_login],
                ["label", "PoC - Username: 'admin'; Password: 'taxes'", 2]
            ],
            0
        )
    

    # Proof of Concept Login - later, will utilize cryptographically signed
    #   and stored credentials for authorized site coordinators.
    #   Cryptographically signed and stored credentials out of scope.
    def _poc_login(self):
        username = self.elements[0].get_text()
        password = self.elements[1].get_text()

        valid_username = "admin"
        valid_password = "taxes"

        if username == valid_username and password == valid_password:
            self.show_admin_menu()
            print(f"Login with {password} @ {username}")
            print("Future implementations will not utilize default logins.")
            print("Nor will they ever print login credentials to the terminal.")
        else:
            print(f"Login unsuccessful - {password} @ {username}")
    

    # Log out
    def logout(self):
        # Since are not holding admin sessions in memory, we can simply change
        #   context back to the login menu, where the only option is to try to
        #   log back in again.
        self.show_login_menu()
    


    """
            ADMIN MENU
    """

    # Show the main menu
    def show_admin_menu(self):
        print("Showing admin menu")
        self.create_form(
            [
                ["label", "Main Menu"],
                ["button", "VITA Sites", self.show_sites_menu],
                ["button", "Site Schedules", self.show_blocks_menu],
                ["button", "Log Out", self.logout]
            ],
            0
        )
    


    """
            SITES METHODS
    """
    

    # VITA Sites Menu
    def show_sites_menu(self):
        print("Showing site menu")
        fields = [
            ["label", "VITA Sites", 2]
        ]

        # Sites
        results = []
        try:
            results = self._db.dump_table_contents("sites")
            for row in results:
                fields.append(
                    [
                        "label",
                        f"{row['street']}, {row['town']} - {row['phone']}",

                    ]
                )
        except Exception as err:
            print(f"show_sites_menu() failed: {err}")

        # Add site button
        fields.append(["button", "Add Site", self.show_add_site_form])

        # Main Menu
        fields.append(["label", ""])
        fields.append(["button", "Main Menu", self.show_admin_menu])

        # Create the form
        self.create_form(fields, 0)
    

    # Show the 'add site' form
    def show_add_site_form(self):
        print("Showing add site form")
        fields = [
            ["label", "Add New Site", 2],
            ["field", "Street"],
            ["field", "Town"],
            ["field", "State"],
            ["field", "Zipcode"],
            ["field", "Phone"],
            ["button", "Create Location", self.create_site]
        ]

        # Main Menu
        fields.append(["label", ""])
        fields.append(["button", "Main Menu", self.show_admin_menu])

        # Create the form
        self.create_form(fields, 0)
    

    # Create a new site
    def create_site(self):
        print("Creating new site")
        self._db.insert_site(
            self.elements[1].get_text(),
            self.elements[2].get_text(),
            self.elements[3].get_text(),
            self.elements[4].get_text(),
            self.elements[5].get_text()
        )
        print("New site created.")
        
        self.show_sites_menu()
    

    # Edit a site
    def show_edit_site_form(self):
        print("Showing edit site form")
        fields = [
            ["label", "You want to edit a site..."],
            ["label", "But it isn't currently implemented."]
        ]

        # Main Menu
        fields.append(["label", ""])
        fields.append(["button", "Main Menu", self.show_admin_menu])

        # Create the form
        self.create_form(fields, 0)
    


    """
            Schedule Blocks METHODS
    """

    # Show 'add block' form
    def show_blocks_menu(self):
        print("Showing blocks menu")
        fields = [
            ["label", "VITA Site Schedules", 2]
        ]
        
        # Get existing sites
        results = []
        try:
            results = self._db.dump_table_contents("sites")
            for row in results:
                fields.append(
                    [
                        "button",
                        f"{row['street']}, {row['town']} - {row['phone']}",
                        partial(self.view_site_schedule, row)
                    ]
                )
        except Exception as err:
            print(f"show_blocks_menu() failed: {err}")
            raise
            
        # Main menu button
        fields.append(["label", ""])
        fields.append(["button", "Main Menu", self.show_admin_menu])

        # Create the form
        self.create_form(fields, 0)
    

    # View the schedule for a site
    def view_site_schedule(self, site):
        print("Showing site schedule blocks")
        site_id = site['id']

        fields = [
            ["label", "Schedule Blocks"],
            ["label", f"{site['street']} {site['town']}"]
        ]

        # Sift through dumped results
        results = self._db.dump_table_contents("schedule_blocks")
        results = self.sift_search_results(results, "site_id", site_id)
        
        # Loop tracking
        grid_row = 2
        day = None
        month = None
        year = None
        time = None

        # Loop!
        for block in results:
            print(block['id'])
            print(block['scheduled_day'], block['scheduled_month'])
            print(block['scheduled_year'], block['start_time'])

            # New date header if on new date
            if (
                day != block['scheduled_day'] or
                month != block['scheduled_month'] or
                year != block['scheduled_year']
            ):
                # Update tracked date
                day = block['scheduled_day']
                month = block['scheduled_month']
                year = block['scheduled_year']

                fields.append(["label", f"{day} {convert_month_code(month)}"])

            # New section header
            fields.append(
                [
                    "button",
                    f"{block['start_time']}",
                    partial(self.view_block, site, block)
                ]
            )
        
        # Create a new block button
        fields.append(
            [
                "button",
                "Create New Block",
                partial(self.show_create_block_form, site)
            ]
        )

        # Main Menu
        fields.append(["label", ""])
        fields.append(["button", "Main Menu", self.show_admin_menu])

        # Create the form
        self.create_form(fields, 0)
    

    # View a block
    def view_block(self, site, block):
        print("Showing block")
        fields = [
            ["label", "Block Appointments"],
            [
                "label",
                f"{block['start_time']} - {site['street']} {site['town']}"
            ],
            ["button", "Edit Block", partial(self.show_edit_block_form, block)]
        ]

        # Get Block Appointments Bridges
        block_apps = self._db.dump_table_contents("block_appointments")
        block_apps = self.sift_search_results(
            block_apps, 'block_id', block['id']
        )

        # Get Block Appointments Bridges
        appointments = self._db.dump_table_contents("appointments")
        appointments = self.sift_search_results(
            appointments, 'block_id', block['id']
        )
        
        # Loop!
        for app in appointments:
            fields.append(
                [
                    "button",
                    f"{app['last_name']}, {app['first_name']}",
                    partial(self.view_appointment, block, app)
                ]
            )

        # Main Menu
        fields.append(["label", ""])
        fields.append(["button", "Main Menu", self.show_admin_menu])

        # Create the form
        self.create_form(fields, 0)
    

    # Create a new block
    def show_create_block_form(self, site):
        print("Show Create Block Form")
        fields = [
            ["label", "Create Block Appointment", 2],
            ["label", f"{site['street']} {site['town']}"],
            ["field", "Time"],
            ["field", "Day"],
            ["field", "Month"],
            ["field", "Year"],
            ["field", "Capacity"],
            ["button", "Create Block", partial(self.create_block, site['id'])],
            ["label", ""]
        ]

        # Main Menu
        fields.append(["label", ""])
        fields.append(["button", "Main Menu", self.show_admin_menu])

        # Create the form
        self.create_form(fields, 0)


    # Create a new block
    def create_block(self, site_id):
        print("Create Block")
        time = self.elements[2].get_text()
        day = self.elements[3].get_text()
        month = self.elements[4].get_text()
        year = self.elements[5].get_text()
        capacity = self.elements[6].get_text()

        # Insert
        self._db.insert_block(site_id, month, day, year, time, capacity, False)

        # Show sites menu
        self.show_blocks_menu()
    

    # Edit a block
    def show_edit_block_form(self, block):
        subtxt = f"{block['start_time']} - {block['scheduled_day']}"
        subtxt += f" {block['scheduled_month']}, {block['scheduled_year']}"
        fields = [
            ["label", "Edit a Block"],
            ["label", subtxt],
        ]

        check_appts = self._db.dump_table_contents("block_appointments")
        if len(self.sift_search_results(
            check_appts,
            "block_id",
            block['id']
        )) > 0:
            # Cannot edit
            fields.append(["label", "There are appointments for this block."])
            fields.append(["label", "It cannot be edited."])
        else:
            fields.append(["field", "Month"])
            fields.append(["field", "Day"])
            fields.append(["field", "Year"])
            fields.append(["field", "Time"])
            fields.append(["field", "Capacity"])
            fields.append(["field", "Available"])
            fields.append(["button", "Edit", partial(self.edit_block, block)])

        # Main Menu
        fields.append(["label", ""])
        fields.append(["button", "Main Menu", self.show_admin_menu])

        # Create the form
        self.create_form(fields, 0)

        # Prefill fields
        self.elements[2].text_area.insert(0, block['scheduled_month'])
        self.elements[3].text_area.insert(0, block['scheduled_day'])
        self.elements[4].text_area.insert(0, block['scheduled_year'])
        self.elements[5].text_area.insert(0, block['start_time'])
        self.elements[6].text_area.insert(0, block['capacity'])
        self.elements[7].text_area.insert(0, block['available'])
    

    # Edit a block
    def edit_block(self, block):
        fields = []

        self._db.edit_block(
            block['id'],
            self.elements[2].get_text(),
            self.elements[3].get_text(),
            self.elements[4].get_text(),
            self.elements[5].get_text(),
            self.elements[6].get_text(),
            self.elements[7].get_text()
        )

        results = self._db.dump_table_contents("schedule_blocks")
        find = self.sift_search_results(results, "id", block['id'])

        for c, name in enumerate([
            "scheduled_month", "scheduled_day", "scheduled_year", "start_time",
            "capacity", "available"
        ]):
            fields.append(
                ["label", f"{name} {find[0][name]}"]
            )
        
        # Main Menu
        fields.append(["label", ""])
        fields.append(["button", "Main Menu", self.show_admin_menu])

        # Create the form
        self.create_form(fields, 0)
    


    """
            SHOW APPOINTMENT METHODS
    """

    # View a single appoinment
    def view_appointment(self, block, appt):
        fields = [
            ["label", "Appointment"],
            ["label", f"{appt['first_name']}, {appt['last_name']}"],
            ["label", f"Phone: {appt['phone']}"],
            ["label", f"Confirmation Number: {appt['confirmation_number']}"],
            ["button", "Edit", partial(self.show_edit_appointment_form, appt)]
        ]
        
        # Main Menu
        fields.append(["label", ""])
        fields.append(["button", "Main Menu", self.show_admin_menu])

        # Create the form
        self.create_form(fields, 0)
    
    
    # Edit an appointment
    def show_edit_appointment_form(self, appointment):
        fields = [
            ["label", "You want to edit an appointment..."],
            ["label", "But it isn't currently implemented."]
        ]

        # Main Menu
        fields.append(["label", ""])
        fields.append(["button", "Main Menu", self.show_admin_menu])

        # Create the form
        self.create_form(fields, 0)


