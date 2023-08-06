from authapi.providers.facebook import facebook


class AuthData(facebook.AuthData):
    scopes: list[str] = [
        "ads_management",
        "ads_read",
        "read_insights",
        "business_management",
    ]
