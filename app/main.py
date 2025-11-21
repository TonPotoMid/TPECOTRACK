from fastapi import FastAPI
from app.routers import auth, users, zones, sources, indicators


def create_app() -> FastAPI:
    app = FastAPI(title="EcoTrack API - Minimal Auth Scaffold")
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(users.router, prefix="/users", tags=["users"])
    app.include_router(zones.router, prefix="/zones", tags=["zones"])
    app.include_router(sources.router, prefix="/sources", tags=["sources"])
    app.include_router(indicators.router, prefix="/indicators", tags=["indicators"])
    @app.get("/", tags=["root"])
    def read_root():
        return {"status": "ok", "message": "EcoTrack API"}
    return app


app = create_app()
