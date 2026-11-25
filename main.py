

import sqlite3
from pydantic import BaseModel, Field

from backend import DB
from admin_console import Console, start_console
from web_app import WebApp

import time


def db_testing(db):
    print("Testing database")
    return True

if __name__ == "__main__":

    # Database Backend
    db = DB()
    db.wipe()
    db.setup()
    
    # Admin Console
    window = start_console()
    console = Console(window)

    # Client Web App
    webapp = WebApp()
    app = webapp.app
    webapp.start()

    # Start console
    try:
        db_testing(db)
        window.mainloop()
    finally:
        print("Admin console closed, shutting down...")
        webapp.stop()