from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
import importlib.resources as templates
import sqlite3
from pydantic import BaseModel, Field



# Globals
app = FastAPI(title="VITA Appointment Reservation System")
wip = True



# Server Helper Methods

def db_connect():
    db_conn = sqlite3.connect("vita_ars.db")
    db_cursor = db_conn.cursor()
    return {"conn": db_conn, "cursor": db_cursor}

def import_template(fname:str):
    return templates.files("templates").joinpath(fname).read_text()

def wipe_database(db, wip):
    if(wip):
        tables = [
            "sites", "appointments", "site_appointments"
        ]
        for table in tables:
            db["cursor"].execute(f"DROP TABLE IF EXISTS {table}")

def create_sites(db):
    db["cursor"].execute("""
        CREATE TABLE IF NOT EXISTS sites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            street TEXT NOT NULL,
            town TEXT NOT NULL,
            state TEXT NOT NULL,
            zipcode TEXT NOT NULL,
            phone INTEGER NOT NULL
        )
    """)
    db["conn"].commit()

def detail_sites(db):
    db["cursor"].execute("PRAGMA table_info(sites)")
    return db["cursor"].fetchall()

def create_schedule_slots(db):
    db["cursor"].execute("""
        CREATE TABLE IF NOT EXISTS schedule_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site_id INTEGER NOT NULL,
            appointment_id INTEGER NULL,
            month INTEGER NOT NULL,
            day INTEGER NOT NULL,
            year INTEGER NOT NULL,
            time INTEGER NOT NULL,
            reserved BOOL
        )
    """)
    db["conn"].commit()

def create_scheduled_appointments(db):
    db["cursor"].execute("""
        CREATE TABLE IF NOT EXISTS scheduled_appointments (
            schedule_slot_id INT NOT NULL,
            appointment_id INT NOT NULL,
            PRIMARY KEY (schedule_slot_id, appointment_id)
        )
    """)
    db["conn"].commit()

def create_appointments(db):
    db["cursor"].execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fname TEXT NULL,
            lname TEXT NULL,
            zipcode INTEGER NULL,
            phone INTEGER NULL,
            confirmed BOOL NOT NULL
        )
    """)
    db["conn"].commit()


def detail_appointments(db):
    db["cursor"].execute("PRAGMA table_info(appointments)")
    return db["cursor"].fetchall()



# FastAPI Methods

@app.get("/", response_class=HTMLResponse)
def root():
    if wip:
        return import_template("wip.html")
    else:
        return import_template("wip.html")


db = db_connect()
wipe_database(db, wip)
create_sites(db)
print(detail_sites(db))
create_appointments(db)
print(detail_appointments(db))

