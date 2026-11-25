

import importlib.resources as import_resources
import threading
from fastapi import FastAPI, status, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import uvicorn



def import_web_template(fname:str):
    return import_resources.files("templates").joinpath(fname).read_text()



class WebApp():
    def __init__(self):
        self.block = True
        self.app = FastAPI(
            title="VITA Appointment Reservation System"
        )
        self._register_routes()
        self.server = None
        self.server_thread = None
    


    ### Register Routes
    def _register_routes(self):

        # Respond to any HTTP request
        @self.app.get("/", response_class = HTMLResponse)
        def root():
            if self.block:
                return import_web_template("wip.html")
            else:
                return import_web_template("wip.html")
        
        # Respond to "test1" request with message
        @self.app.post("/test1/")
        async def test1():
            print("Test1 button clicked!")
            return "Test sat!"
        
        # Respond to "test2" request with HTML
        @self.app.post("/test2/", response_class = HTMLResponse)
        async def test2():
            print("Test2 button clicked!")
            return import_web_template("wip.html")
    


    ### Start and Stop the Web Server

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
    


    ### Allow & Block Access to Application From the Web

    # App Blocking True - Web Access Blocked
    def block_app(self):
        self.block = True
    
    # App Blocking False - Web Access Allowed
    def unblock_app(self):
        self.block = False
    # Alias
    def allow_app(self):
        self.unblock_app()




