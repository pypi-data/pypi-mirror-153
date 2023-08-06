import os

from synapse.module_api import ModuleApi


class RequestDigitTokenMailer:
    def __init__(self, api: ModuleApi):
        self._api = api

        (self._template_html, self._template_text,) = self._api.read_templates(
            ["request_token_template.html", "request_token_template.txt"],
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"),
        )

    async def send_registration_email(
        self, email: str, token: str, client_secret: str, sid: str
    ) -> bool:
        try:
            template_vars = {
                "app_name": self._api.email_app_name,
                "server_name": self._api.server_name,
                "token": token,
                "client_secret": client_secret,
                "sid": sid,
            }

            subject = "Your Campgrounds Validation Token"

            html_text = self._template_html.render(**template_vars)
            plain_text = self._template_text.render(**template_vars)

            await self._api.send_mail(
                recipient=email,
                subject=subject,
                html=html_text,
                text=plain_text,
            )

            return True
        except Exception:
            return False
