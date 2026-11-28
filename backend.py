

import sqlite3


class DB():
    def __init__(self):
        self.name = ("vita_ars.db")

        self.table_names = [
            "block_appointments",
            "appointments",
            "schedule_blocks",
            "sites"
        ]
    
    
    def _is_valid_table_name(self, table_name):
        print(f"Validating user input: {table_name}")

        if table_name in self.table_names:
            print(f"Table name validated.")
            return True
        
        print(f"Invalid table name.")
        return False
    

    def connect(self):
        conn = None

        try:
            conn = sqlite3.connect(self.name)
            conn.execute("PRAGMA foreign_keys=ON")
            conn.execute("PRAGMA busy_timeout=5000")
            return conn
        
        except sqlite3.Error:
            if conn is not None:
                conn.close()
            raise
    

    def setup(self):
        print("Setting up database")

        conn = None

        try:
            # Connect to the database
            conn = self.connect()

            # Create service sites table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    street TEXT NOT NULL,
                    town TEXT NOT NULL,
                    state TEXT NOT NULL,
                    zipcode TEXT NOT NULL,
                    phone TEXT NOT NULL
                )
            """)

            # Create schedule blocks table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS schedule_blocks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    site_id INTEGER NOT NULL REFERENCES sites(id),
                    scheduled_month INTEGER NOT NULL,
                    scheduled_day INTEGER NOT NULL,
                    scheduled_year INTEGER NOT NULL,
                    start_time TEXT NOT NULL,
                    capacity INTEGER NOT NULL,
                    available INTEGER NOT NULL
                )
            """)

            # Create appointments table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    block_id INTEGER NOT NULL REFERENCES schedule_blocks(id),
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    confirmation_number
                )
            """)

            # Create block appointments bridge table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS block_appointments (
                    block_id INTEGER NOT NULL REFERENCES schedule_blocks(id),
                    appointment_id INTEGER NOT NULL REFERENCES appointments(id),
                    PRIMARY KEY (block_id, appointment_id),
                    UNIQUE (appointment_id)
                )
            """)
        
        except sqlite3.Error as err:
            print(f"setup() failed: {err}")
            raise

        finally:
            # Close connection
            if conn is not None:
                conn.close()
    

    def wipe(self):
        print("Wiping database...")

        conn = None

        try:
            # Connect to the database
            conn = self.connect()

            for table in self.table_names:
                conn.execute(f"DROP TABLE IF EXISTS {table}")
            
            print("Setting up clean database.")
            self.setup()
        
        except sqlite3.Error as err:
            print(f"wipe() failed: {err}")
            raise

        finally:
            # Close connection
            if conn is not None:
                conn.close()

    
    def get_table_details(self, table_name:str):
        print(f"Getting table details for {table_name}")

        if not self._is_valid_table_name(table_name):
            print("Failed to get table details.")
            return []
        
        conn = None

        try:
            # Connect to the database
            conn = self.connect()
            conn.row_factory = sqlite3.Row
            
            results = conn.execute(
                "SELECT * FROM pragma_table_info(?)",
                (table_name,)
            )
            return [dict(row) for row in results]
        
        except sqlite3.Error as err:
            print(f"get_table_details() failed: {err}")
            raise

        finally:
            # Close connection
            if conn is not None:
                conn.close()
    

    def dump_table_contents(self, table_name:str):
        print(f"Dumping contents of table {table_name}")

        if not self._is_valid_table_name(table_name):
            print("Failed to get table contents.")
            return []

        conn = None

        try:
            # Connect to the database
            conn = self.connect()
            conn.row_factory = sqlite3.Row
            
            cmd = f"SELECT * FROM {table_name}"
            results = conn.execute(cmd)
            return [dict(row) for row in results]
        
        except sqlite3.Error as err:
            print(f"dump_table_contents() failed: {err}")
            raise

        finally:
            # Close connection
            if conn is not None:
                conn.close()
    

    # Add a new site to the database
    def insert_site(
        self,
        street:str,
        town:str,
        state:str,
        zipcode:str,
        phone:str
    ):
        print(f"Adding new site to database")
        print("--", street, town, state, zipcode, phone)

        conn = None

        try:
            # Connect to the database
            conn = self.connect()
            
            row_id = conn.execute(
                """
                INSERT INTO sites (street, town, state, zipcode, phone)
                VALUES (?, ?, ?, ?, ?)
                """,
                (street, town, state, zipcode, phone)
            ).lastrowid

            conn.commit()
            return row_id
        
        except sqlite3.Error as err:
            print(f"insert_site() failed: {err}")
            raise

        finally:
            # Close connection
            if conn is not None:
                conn.close()
    
    
    # Add a new schedule block to the database
    def insert_block(
        self,
        site_id:int,
        scheduled_month:int,
        scheduled_day:int,
        scheduled_year:int,
        start_time:str,
        capacity:int,
        available:bool
    ):
        print(f"Adding new schedule block to database")
        print(
            f"""
            -- {site_id}, {scheduled_month}, {scheduled_day}, {scheduled_year}
            -- {start_time}, {capacity}, {available}
            """
        )

        if available:
            available = 1
        else:
            available = 0

        conn = None

        try:
            # Connect to the database
            conn = self.connect()
            
            row_id = conn.execute(
                """
                INSERT INTO schedule_blocks (
                    site_id, scheduled_month, scheduled_day, scheduled_year,
                    start_time, capacity, available
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    site_id, scheduled_month, scheduled_day, scheduled_year,
                    start_time, capacity, available
                )
            ).lastrowid

            conn.commit()
            return row_id
        
        except sqlite3.Error as err:
            print(f"insert_block() failed: {err}")
            raise

        finally:
            # Close connection
            if conn is not None:
                conn.close()


    # Add a new appointment to the database
    def insert_appointment(
        self,
        block_id:int,
        first_name:str,
        last_name:str,
        phone:str,
        confirmation_number:str
    ):
        print(f"Adding new appointment to database")
        print(
            f"-- {block_id}, {first_name}, {last_name}, {phone}, "
            f"{confirmation_number}"
        )

        conn = None

        try:
            # Connect to the database
            conn = self.connect()
            
            row_id = conn.execute(
                """
                INSERT INTO appointments (
                    block_id, first_name, last_name, phone, confirmation_number
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (block_id, first_name, last_name, phone, confirmation_number)
            ).lastrowid

            conn.commit()
            return row_id
        
        except sqlite3.Error as err:
            print(f"insert_appointment() failed: {err}")
            raise

        finally:
            # Close connection
            if conn is not None:
                conn.close()


    # Add a new block appointment bridge to the database
    def insert_block_appointment(
        self,
        block_id:int,
        appointment_id:int
    ):
        print(f"Adding new block appointment to database")
        print(f"-- {block_id}, {appointment_id}")

        conn = None

        try:
            # Connect to the database
            conn = self.connect()
            
            row_id = conn.execute(
                """
                INSERT INTO block_appointments (
                    block_id, appointment_id
                )
                VALUES (?, ?)
                """,
                (block_id, appointment_id)
            ).lastrowid

            conn.commit()
            return row_id
        
        except sqlite3.Error as err:
            print(f"insert_block_appointment() failed: {err}")
            raise

        finally:
            # Close connection
            if conn is not None:
                conn.close()
    
    # Edit an existing block
    def edit_block(
        self,
        id,
        new_month,
        new_day,
        new_year,
        new_time,
        new_capacity,
        new_availability
    ):
        print(f"Modifying block {id}")
        print(new_month, new_day, new_year, new_time, new_capacity, new_availability)

        conn = None

        if new_availability and new_availability != "0":
            new_availability = 1
        else:
            new_availability = 0

        try:
            conn = self.connect()

            conn.execute("""
                UPDATE schedule_blocks
                SET scheduled_month = ?,
                    scheduled_day = ?,
                    scheduled_year = ?,
                    start_time = ?,
                    capacity = ?,
                    available = ?
                WHERE id = ?
                """,
                (
                    new_month, new_day, new_year, new_time, new_capacity,
                    new_availability, id
                )
            )

            conn.commit()
        
        except sqlite3.Error as err:
            print(f"edit_block() failed: {err}")
            raise
        
        finally:
            # Close connection
            if conn is not None:
                conn.close()



    """
            GET METHODS
    """


    # Get a single site
    def get_site(self, site_id: int):
        conn = None
        try:
            conn = self.connect()
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM sites WHERE id = ?", (site_id,)
            ).fetchone()
            return dict(row) if row else None
        finally:
            if conn is not None:
                conn.close()

    # Get a single block
    def get_block(self, block_id: int):
        conn = None
        try:
            conn = self.connect()
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM schedule_blocks WHERE id = ?", (block_id,)
            ).fetchone()
            return dict(row) if row else None
        finally:
            if conn is not None:
                conn.close()
    

    # Count block appointments
    def count_block_appointments(self, block_id: int):
        conn = None
        try:
            conn = self.connect()
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT a.*
                FROM block_appointments ba
                JOIN appointments a ON a.id = ba.appointment_id
                WHERE ba.block_id = ?
                """,
                (block_id,)
            )
            return len([dict(r) for r in rows])
        except sqlite3.Error as err:
            print(f"count_block_appointments() failed: {err}")
            raise
        finally:
            if conn is not None:
                conn.close()


    # Get a block and all of its appointments
    def get_block_appointments(self, block_id: int):
        conn = None
        try:
            conn = self.connect()
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT a.*
                FROM block_appointments ba
                JOIN appointments a ON a.id = ba.appointment_id
                WHERE ba.block_id = ?
                """,
                (block_id,)
            )
            return [dict(r) for r in rows]
        except sqlite3.Error as err:
            print(f"get_block_appointments() failed: {err}")
            raise
        finally:
            if conn is not None:
                conn.close()
