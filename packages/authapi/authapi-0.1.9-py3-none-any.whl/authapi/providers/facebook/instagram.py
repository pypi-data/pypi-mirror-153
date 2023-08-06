from authapi.providers.facebook import facebook


class AuthData(facebook.AuthData):
    scopes: list[str] = [
        "ads_management",
        "instagram_basic",
        "instagram_manage_insights",
    ]
