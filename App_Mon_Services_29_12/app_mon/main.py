from fastapi import FastAPI
import models
from database import engine
from routers import app_mon, monitor, PGService

app = FastAPI(title=" Application Monitoring", debug=True)
models.Base.metadata.create_all(engine)
app.include_router(app_mon.router)
app.include_router(monitor.router)
app.include_router(PGService.router)


