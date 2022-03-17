# # Meta
from src.utils.integrity import structure
# # Fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.middleware import cors as cors
# # GraphQL
# # Server Logic
# # # V2
from src.v2.routers import data as data_v2
from src.v2.routers import reports as reports_v2

# Backend Logic
# Instantiate the FastAPI Server
app = FastAPI()


@app.on_event("startup")
# Perform Directory/File Integrity checks on first run
async def startup_event():
    structure.local_dir_check()

# Import external routing logic
# Add prefix to these in order to specify
# openAPI version
api_v2 = "/api/v2"

# App Data
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors.origins,
    allow_credentials=True,
    allow_methods=cors.methods,
    allow_headers=cors.headers,
)

# API V2
app.include_router(data_v2.router, prefix=api_v2)
app.include_router(reports_v2.router, prefix=api_v2)


@app.on_event("shutdown")
# # Delete folder from database on closure
# # to ensure PHI
def shutdown_event():
    structure.remove_sensitive_data()
