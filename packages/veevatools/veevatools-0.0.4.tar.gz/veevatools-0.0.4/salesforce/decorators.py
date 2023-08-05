def serialze_zeep(func):
    import zeep.helpers
    import pandas as pd
    def wrapper(*args, **kwargs):
        result = pd.DataFrame.from_dict(zeep.helpers.serialize_object(func(*args, **kwargs)),orient="index").transpose()
        return result
    return wrapper