

import importlib.resources as import_resources
import threading
from fastapi import FastAPI, status, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn
import uuid
import time
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import backend
from html import escape
from random import randint
from datetime import datetime, timedelta



def import_web_template(fname:str):
    return import_resources.files("templates").joinpath(fname).read_text()



class WebApp():
    def __init__(self):
        self.block = True
        self.app = FastAPI(
            title="VITA Appointment Reservation System"
        )
        static_dir = Path(__file__).parent / "static"
        self.app.mount("/static", StaticFiles(
            directory=static_dir
        ), name="static")
        self.sessions = {}
        self.TTL = 900
        self._register_routes()
        self.server = None
        self.server_thread = None
        self.db = backend.DB()

        self.income_limit = 89000



    """
            HTTP RESPONDING AND ROUTING
    """

    # Expired - client took longer than 15 minutes to complete
    def expired(self):
        return RedirectResponse("/", status_code=303)


    ### Register Routes
    def _register_routes(self):

        # Respond to any HTTP request
        @self.app.get("/", response_class = HTMLResponse)
        def root(request: Request):
            self.purge_expired_sessions()

            # Get cookie session id
            sid = request.cookies.get("sid")

            if self.get_session(request) is None:
                sid = self.new_session()
            
            response = HTMLResponse(import_web_template("main.html"))
            response.set_cookie("sid", sid, httponly=True)
            return response
        

        # Request to start screening
        @self.app.post("/start_screening/", response_class = HTMLResponse)
        async def start_screening(request: Request):
            # Session expired
            if self.get_session(request) is None:
                return self.expired()
            return import_web_template("screening.html")


        # No to household question (more than $89000)
        @self.app.post(
            "/screening/disqualified/",
            response_class = HTMLResponse
        )
        async def disqualified(request: Request):
            # Session expired
            if self.get_session(request) is None:
                return self.expired()
            # Next page
            return import_web_template("requirements_failed.html")


        # Yes to household question (less than $89000)
        @self.app.post(
            "/screening/qualified/",
            response_class = HTMLResponse
        )
        async def qualified(request: Request):
            # Session expired
            if self.get_session(request) is None:
                return self.expired()
            # Next page
            return import_web_template("client_information.html")
        

        # College client information and show all available sites
        @self.app.post(
            "/screening/sites/",
            response_class = HTMLResponse
        )
        async def show_sites(
            request: Request,
            first_name:str = Form(...),
            last_name:str = Form(...),
            zipcode:str = Form(...),
            phone:str = Form(...)
        ):
            session = self.get_session(request)
            
            # Session expired
            if session is None:
                return self.expired()
            
            page = import_web_template("view_sites.html")
            
            # Client info
            session['first_name'] = first_name.strip()
            session['last_name'] = last_name.strip()
            session['zipcode'] = zipcode.strip()
            session['phone'] = phone.strip()

            # Next page
            sites = self.db.dump_table_contents("sites")
            parts = []
            for site in sites:
                label = f"{site['street']}, {site['town']},"
                label += f" {site['state']} {site['zipcode']}"
                parts.append(
                    f'<form action="/screening/site/{site["id"]}/"'
                    f' method="post">'
                    f'<input type="submit" value="{escape(label)}"></form>'
                )
            contents = "\n".join(parts) or "<p>No sites available.</p>"

            return page.replace("{{SITES}}", contents)
        

        # Show all available sites
        @self.app.post(
            "/screening/sites/alt/",
            response_class = HTMLResponse
        )
        async def show_sites_alt(request: Request):
            session = self.get_session(request)
            
            # Session expired
            if session is None:
                return self.expired()
            
            page = import_web_template("view_sites.html")

            # Next page
            sites = self.db.dump_table_contents("sites")
            parts = []
            for site in sites:
                label = f"{site['street']}, {site['town']},"
                label += f" {site['state']} {site['zipcode']}"
                parts.append(
                    f'<form action="/screening/site/{site["id"]}/"'
                    f' method="post">'
                    f'<input type="submit" value="{escape(label)}"></form>'
                )
            contents = "\n".join(parts) or "<p>No sites available.</p>"

            return page.replace("{{SITES}}", contents)


        # Show a site
        @self.app.post(
            "/screening/site/{site_id}/",
            response_class=HTMLResponse
        )
        async def view_site(request: Request, site_id: int):
            session = self.get_session(request)

            if session is None:
                return self.expired()
            page = import_web_template("site_schedule.html")


            blocks = [
                block for block in self.db.dump_table_contents(
                    "schedule_blocks"
                )
                if block['site_id'] == site_id and block['available']
            ]
            blocks.sort(key=lambda block: (
                block['scheduled_year'], block['scheduled_month'],
                block['scheduled_day'], block['start_time']
            ))

            parts, last_date = [], None
            cutoff = datetime.now() + timedelta(hours=24)
            for block in blocks:
                # Do not show blocks that are full
                if (self.db.count_block_appointments(block['id']) >=
                block['capacity']):
                    continue

                # Do not show blocks that are within 24 hours
                start = datetime.strptime(
                    f"{block['scheduled_year']}-{block['scheduled_month']}-"
                    f"{block['scheduled_day']} {block['start_time']}",
                    "%Y-%m-%d %I:%M %p",
                )
                if start <= cutoff:
                    continue

                # Get current date
                date = (
                    block['scheduled_year'],
                    block['scheduled_month'],
                    block['scheduled_day']
                )

                # Check against last date - print new date header
                if date != last_date:
                    parts.append(
                        f"<h4>{block['scheduled_month']}"
                        f"/{block['scheduled_day']}"
                        f"/{block['scheduled_year']}</h4>"
                    )
                    last_date = date
                
                # Build new form
                parts.append(
                    f'<form action="/screening/block/{block["id"]}/"'
                    f' method="post">'
                    f'<input type="submit"'
                    f' value="{escape(block["start_time"])}">'
                    f'</form>'
                )

            # Combine and return
            contents = "\n".join(parts) or "<p>No open blocks at this site.</p>"
            return page.replace("{{BLOCKS}}", contents)
    

        # Show block appointment scheduling page
        @self.app.post(
            "/screening/block/{block_id}/",
            response_class=HTMLResponse
        )
        async def show_appointment_scheduling(request: Request, block_id: int):
            session = self.get_session(request)

            # Session expired
            if session is None:
                return self.expired()

            # Page template
            page = import_web_template("appointment_scheduling.html")

            """ Do the stuff that fills the page out"""
            contents = f"""
                <form action="/screening/appt/{block_id}/" method="post">
                <input type="submit" value="Yes">
                </form>
                <form action="/screening/sites/alt/" method="post">
                <input type="submit" value="No">
                </form>
            """

            # Fill in and return
            return page.replace("{{APPT}}", contents)


        # Show block appointment request confirmation page
        @self.app.post(
            "/screening/appt/{block_id}/",
            response_class=HTMLResponse
        )
        async def schedule_appointment(request: Request, block_id: int):
            session = self.get_session(request)

            # Session expired
            if session is None:
                return self.expired()

            # Page template
            page = import_web_template("show_confirmation.html")

            block = self.db.get_block(block_id)
            site = self.db.get_site(block['site_id'])

            """ Do the stuff that fills the page out"""
            contents = f"""
                Name: {session['first_name']} {session['last_name']}
                <br/>Zipcode: {session['zipcode']}
                <br/>Phone: {session['phone']}
                <br/>Service Site: {site['street']} {site['town']}
                <br/>Service Time: {block['start_time']}
                <form action="/screening/confirmed/{block_id}/" method="post">
                    <input type="submit" value="Yes">
                </form>
            """

            # Fill in and return
            return page.replace("{{CONFIRMATION}}", contents)


        # Show confirmation page
        @self.app.post(
            "/screening/confirmed/{block_id}/",
            response_class=HTMLResponse
        )
        async def show_confirmation(request: Request, block_id: int):
            session = self.get_session(request)
            sid = request.cookies.get("sid")

            # Session expired
            if session is None:
                return self.expired()

            # Page template
            page = import_web_template("confirmed.html")

            block = self.db.get_block(block_id)
            site = self.db.get_site(block['site_id'])

            # Create appointment
            if self.db.count_block_appointments(block_id) >= block['capacity']:
                print("Someone sniped your appointment!")
                return import_web_template("view_sites.html")
            
            # Remove session - appointment booked
            self.sessions.pop(sid, None)
            
            # Confirmation Number
            confirmation_number = randint(100000, 999999)
            
            # Create appointment
            appt_id = self.db.insert_appointment(
                block_id,
                escape(session['first_name']),
                escape(session['last_name']),
                escape(session['phone']),
                confirmation_number
            )

            # Bridge appointment and block
            bridge_id = self.db.insert_block_appointment(
                block_id,
                appt_id
            )

            """ Do the stuff that fills the page out"""
            contents = f"""
                Name: {session['first_name']} {session['last_name']}
                <br/>Zipcode: {session['zipcode']}
                <br/>Phone: {session['phone']}
                <br/>Service Site: {site['street']} {site['town']}
                <br/>Service Time: {block['start_time']}
                <br/>Confirmation Code: {confirmation_number}
                <br/><br/>
                Please keep your confirmation code. This will allow you to
                access your appointment on this website again later.
                <form action="/" method="get">
                    <input type="submit" value="Click Here When Finished">
                </form>
            """

            # Fill in and return
            return page.replace("{{CONFIRMATION}}", contents)


    """
            SESSION HANDLING
    """
    
    # Create new session cookie
    def new_session(self):
        sid = str(uuid.uuid4())
        self.sessions[sid] = {
            'data': {
                'first_name': None,
                'last_name': None,
                'zipcode': None,
                'phone': None
            },
            'updated': time.time()
        }
        return sid
    

    # Delete in-memory session
    def get_session(self, request):
        sid = request.cookies.get("sid")
        session = self.sessions.get(sid)

        if session is None:
            return None
        
        if time.time() - session['updated'] > self.TTL:
            del self.sessions[sid]
            return None
        
        session['updated'] = time.time()
        return session['data']
    

    # Purge expired sessions
    def purge_expired_sessions(self):
        now = time.time()
        for sid, session in list(self.sessions.items()):
            if now - session["updated"] > self.TTL:
                self.sessions.pop(sid, None)
    


    """
            Start and Stop the Web Server
    """

    # Start
    def start(self):
        config = uvicorn.Config(
            self.app,
            host = "127.0.0.1",
            port = 8000
        )
        self.server = uvicorn.Server(config)
        self.server_thread = threading.Thread(target=self.server.run)
        self.server_thread.start()
    

    # Stop
    def stop(self):
        if self.server:
            self.server.should_exit = True
        if self.server_thread:
            self.server_thread.join()




