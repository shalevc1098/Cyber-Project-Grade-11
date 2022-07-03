import importlib

mod = importlib.import_module("globalsush")

def get_num():
    mod.num.append("456")
    return mod.num