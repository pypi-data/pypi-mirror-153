from pydantic import BaseModel, root_validator
from typing import Optional, Any


class AuthData(BaseModel):
    client_id: str
    client_secret: str
    authorize_url: str
    access_token_url: str
    refresh_token_url: Optional[str] = None
    scopes: list[str]
    redirect_uri: Optional[str] = None
    state: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    extra: Optional[dict[str, Any]] = None

    @root_validator
    def default_to_access_token(cls, values):
        if not values.get("refresh_token_url"):
            values["refresh_token_url"] = values["access_token_url"]
        return values
