from app.auth.jwt import SECRET_KEY

from fastapi import FastAPI

from nicegui import app, ui


def init(fastapi_app: FastAPI) -> None:
    @ui.page('/show')
    def show():
        ui.label('The Kakeibo app')

        # NOTE dark mode will be persistent for each user across tabs and server restarts
        ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
        ui.checkbox('dark mode').bind_value(app.storage.user, 'dark_mode')

    ui.run_with(
        fastapi_app,
        storage_secret=SECRET_KEY)