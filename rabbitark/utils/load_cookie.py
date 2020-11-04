from http.cookies import SimpleCookie


def load_cookie(rawdata):
    cookie = SimpleCookie()
    cookie.load(rawdata)
    return {key: morsel.value for key, morsel in cookie.items()}
