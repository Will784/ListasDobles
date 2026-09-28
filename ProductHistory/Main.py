import importlib.util
import pkgutil

if not hasattr(pkgutil, "find_loader"):
    pkgutil.find_loader = importlib.util.find_spec

from nicegui import ui

from Services.HistoryService import HistoryService
from Views.HistoryView import HistoryView

service = HistoryService()
service.load_sample_data()


@ui.page("/")
def index_page():
    HistoryView(service).build()


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Historial de Productos", port=8080, reload=False, favicon="🛒", show=True)
