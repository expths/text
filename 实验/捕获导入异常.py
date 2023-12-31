
try:
    import a
except ModuleNotFoundError as err:
    print(err)
    print(type(err))