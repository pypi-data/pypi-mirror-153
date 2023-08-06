from flask import Flask, render_template, request, redirect, url_for
from requests_oauthlib import OAuth2Session
import os
from typing import Protocol
from authapi.authdata import AuthData
import pathlib

os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


class SecretProtocol(Protocol):
    def pull(self) -> dict:
        ...

    def push(self, data: dict) -> None:
        ...


class AuthAPI(Flask):
    def __init__(
        self,
        name: str,
        auth_data: AuthData,
        token_secret: SecretProtocol,
    ):

        template_path = str(pathlib.Path(__file__).parent.absolute() / "templates")
        super().__init__(name, template_folder=template_path)
        self.route("/", methods=["GET"])(self.auth_index)
        self.route("/login", methods=["GET"])(self.login)
        self.route("/authorize", methods=["GET"])(self.authorize)
        self.route("/refresh_token", methods=["GET"])(self.refresh_token)
        self.auth_data = auth_data
        self.auth = OAuth2Session(
            client_id=self.auth_data.client_id,
            redirect_uri=self.auth_data.redirect_uri,
            scope=self.auth_data.scopes,
        )
        self.token_secret = token_secret

    def auth_index(self):
        return render_template(
            "index.html",
            name=self.name,
            state="landing",
            next="login",
        )

    def login(self):
        self.auth.redirect_uri = url_for("authorize", _external=True, _scheme="https")
        authorize_url, self.auth.state = self.auth.authorization_url(
            url=self.auth_data.authorize_url,
            access_type="offline",
            prompt="consent",
        )
        return redirect(authorize_url)

    def authorize(self):
        self.auth.token = self.auth.fetch_token(
            token_url=self.auth_data.access_token_url,
            client_secret=self.auth_data.client_secret,
            authorization_response=request.url,
        )
        self.token_secret.push(self.auth.token)

        return render_template(
            "index.html",
            name=self.name,
            state="authorized",
            next="refresh_token",
        )

    def refresh_token(self):
        self.auth.token = self.token_secret.pull()
        self.auth.token = self.auth.refresh_token(
            token_url=self.auth_data.refresh_token_url,
            client_id=self.auth_data.client_id,
            client_secret=self.auth_data.client_secret,
            refresh_token=self.auth.token["refresh_token"],
        )
        self.token_secret.push(self.auth.token)

        return render_template(
            "index.html",
            name=self.name,
            state="refreshed",
            next="refresh_token",
        )

    def get_token(self):
        self.auth.token = self.token_secret.pull()
        return self.auth.token
