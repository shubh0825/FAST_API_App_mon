from fastapi import FastAPI
import models
from database import engine
from routers import routers

app = FastAPI(title=" Application Monitoring", debug=True)
models.Base.metadata.create_all(engine)

app.include_router(routers.router)



