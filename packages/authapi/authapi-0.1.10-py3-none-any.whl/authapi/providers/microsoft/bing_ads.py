from authapi.providers.microsoft import microsoft


class AuthData(microsoft.AuthData):
    scopes: list[str] = [
        "openid",
        "offline_access",
        "https://ads.microsoft.com/msads.manage",
    ]
