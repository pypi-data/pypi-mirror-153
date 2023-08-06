from authapi import data


class AuthData(data.AuthData):
    authorize_url: str = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
    access_token_url: str = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    scopes: list[str] = [
        "openid",
        "offline_access",
        "email",
        "profile",
    ]
