from http.cookiejar import MozillaCookieJar
from http.cookies import SimpleCookie


class Cookies(dict[str, str]):
    def load_raw_cookie(self, rawdata: str) -> None:
        cookie: SimpleCookie[str] = SimpleCookie(rawdata)
        self.update({key: morsel.value for key, morsel in cookie.items()})

    def load_cookie_txt(self, filename: str) -> None:
        mcj = MozillaCookieJar()
        mcj.load(filename)
        self.update({each.name: each.value or "" for each in mcj})
