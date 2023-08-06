from authapi.authdata.google import google


class AuthData(google.AuthData):
    scopes: list[str] = [
        "openid",
        "https://www.googleapis.com/auth/adwords",
    ]
