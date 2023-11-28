from . import frontend

from fastapi import FastAPI

from app.admin.router import router as admin_router
from app.auth.router import router as auth_router
from app.core.database import engine
from app.entry.router import router as entry_router
from app.insights.router import router as insights_router
from app.models import models
from app.user.router import router as user_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="kakeibo-app", summary="A household-ledger app.")


@app.get("/")
def root():
    return {"message": "The API is LIVE!!"}


app.include_router(user_router)
app.include_router(entry_router)
app.include_router(insights_router)

app.include_router(admin_router)

app.include_router(auth_router)

frontend.init(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
