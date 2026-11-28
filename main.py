

from backend import DB
from admin_console import Console, start_console
from web_app import WebApp


def db_testing(db):
    print("Testing database")

    """
    db.wipe()
    
    db.insert_site(
        "1 Main Street",
        "Oneonta",
        "NY",
        "13851",
        "6078907654"
    )
    db.insert_site(
        "6 Alt Street",
        "Oneonta",
        "NY",
        "13851",
        "6071237890"
    )
    db.insert_site(
        "13 Elm Street",
        "Oneonta",
        "NY",
        "13851",
        "7894513"
    )

    db.insert_block(1, 1, 15, 2027, "2:00 PM", 8, True)
    db.insert_block(1, 1, 15, 2027, "3:00 PM", 8, True)
    db.insert_block(1, 1, 16, 2027, "2:00 PM", 8, True)

    db.insert_block(2, 1, 17, 2027, "2:00 PM", 8, True)
    db.insert_block(2, 1, 18, 2027, "2:00 PM", 8, True)
    db.insert_block(2, 1, 18, 2027, "3:00 PM", 8, True)

    db.insert_appointment(
        1,
        "Daniel",
        "Scutt",
        "6072961848",
        "876543"
    )
    db.insert_block_appointment(
        1,
        1
    )
    """





if __name__ == "__main__":

    # Database Backend
    db = DB()
    db.setup()
    
    # Admin Console
    window = start_console()
    console = Console(window, db)

    # Client Web App
    webapp = WebApp()
    app = webapp.app
    webapp.start()

    # Start console
    try:
        db_testing(db)
        window.mainloop()
    
    except Exception as err:
        print(f"Failed to start console: {err}")
    
    finally:
        print("Admin console closed, shutting down...")
        webapp.stop()