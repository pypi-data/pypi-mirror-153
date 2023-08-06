from synapse.module_api import ModuleApi
from synapse.module_api.errors import SynapseError
from synapse.util.stringutils import random_string

from request_digit_token._config import RequestDigitTokenConfig
from request_digit_token._mailer import RequestDigitTokenMailer
from request_digit_token._utils import random_digit_string


class RequestDigitTokenBase:
    def __init__(self, config: RequestDigitTokenConfig, api: ModuleApi):
        self._api = api
        self._hs = api._hs
        self._store = api._store

        self._token_length = config.token_length
        self._token_lifetime = config.token_lifetime

        self._mailer = RequestDigitTokenMailer(self._api)

    async def send_digit_token(
        self, email: str, client_secret: str, send_attempt: int
    ) -> str:
        session = await self._store.get_threepid_validation_session(
            "email", client_secret, address=email, validated=False
        )

        # Check if a session already exists and is not yet validated.
        if session and session.get("validated_at") is None:
            session_id = session["session_id"]
            last_send_attempt = session["last_send_attempt"]

            # Check if send_attempt is higher than previous attempts.
            if send_attempt <= last_send_attempt:
                # If not, just return a success without sending an email.
                return session_id
        else:
            # An non-validated session does not exist yet.
            # Generate new session id.
            session_id = random_string(16)

        # Generate new validation token.
        token = random_digit_string(self._token_length)

        # Send the mail containing the token.
        sent = await self._mailer.send_registration_email(
            email, token, client_secret, session_id
        )

        if not sent:
            raise SynapseError(500, "An error was encountered when sending the email")

        token_expires = self._hs.get_clock().time_msec() + self._token_lifetime

        await self._store.start_or_continue_validation_session(
            "email",
            email,
            session_id,
            client_secret,
            send_attempt,
            "",  # unused next_link
            token,
            token_expires,
        )

        return session_id

    async def validate_digit_token(
        self, token: str, client_secret: str, session_id: str
    ):
        try:
            await self._store.validate_threepid_session(
                session_id, client_secret, token, self._hs.get_clock().time_msec()
            )
        except Exception:
            raise SynapseError(400, "Invalid registration token.")
