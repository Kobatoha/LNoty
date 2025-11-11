import importlib
import pkgutil
from aiogram import Router

def load_routers() -> list[Router]:
    routers = []
    package = __name__  # 'routers'
    for _, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"{package}.{module_name}")
        router = getattr(module, "router", None)
        if isinstance(router, Router):
            routers.append(router)
    print(routers)
    return routers
