from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import importlib.resources as templates
import sqlite3



# Globals
db_conn = sqlite3.connect("vita_ars.db")
db_cursor = db_conn.cursor()
app = FastAPI()
wip = True



# Server Helper Methods

def import_template(fname:str):
    return templates.files("templates").joinpath(fname).read_text()

def create_appointments():
    db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT
            fname TEXT NOT NULL
            lname TEXT NOT NULL
            zipcode INTEGER NOT NULL
            phone INTEGER NOT NULL
        )
    """)

create_appointments()


# FastAPI Methods

@app.get("/", response_class=HTMLResponse)
def root():
    if wip:
        return import_template("wip.html")
    else:
        return import_template("wip.html")


"""
def main():
    print("??")
if __name__ == "__main__":
    main()
"""