import importlib

mod = importlib.import_module("globalsush")
mod.num.append("123")
print(mod.num)

def main2_func():
    import main2
    print(main2.get_num())

main2_func()