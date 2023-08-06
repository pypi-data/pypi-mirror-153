from authapi import data


class AuthData(data.AuthData):
    authorize_url: str = "https://accounts.google.com/o/oauth2/v2/auth"
    access_token_url: str = "https://www.googleapis.com/oauth2/v4/token"
    scopes: list[str] = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ]
