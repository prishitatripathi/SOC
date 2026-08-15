from fastapi import FastAPI
from .api import routes as routes_mod

app = FastAPI(title="PROBE-SOC API")
app.include_router(routes_mod.router)
from fastapi import FastAPI
from .api import routes

app = FastAPI(title="PROBE-SOC API")
app.include_router(routes.router)
