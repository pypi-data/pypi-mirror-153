from synapse.http.servlet import (
    assert_params_in_dict,
    parse_json_object_from_request,
    parse_string,
)
from synapse.metrics import threepid_send_requests
from synapse.module_api import DirectServeJsonResource, ModuleApi
from synapse.module_api.errors import SynapseError
from synapse.util.stringutils import assert_valid_client_secret
from synapse.util.threepids import check_3pid_allowed, validate_email
from twisted.web.resource import Resource

from request_digit_token._base import RequestDigitTokenBase
from request_digit_token._config import RequestDigitTokenConfig


class RequestDigitTokenServlet(Resource):
    def __init__(self, config: RequestDigitTokenConfig, api: ModuleApi):
        super().__init__()

        self.putChild(b"requestToken", RequestDigitTokenSendServlet(config, api))
        self.putChild(b"validateToken", RequestDigitTokenValidateServlet(config, api))


class RequestDigitTokenSendServlet(RequestDigitTokenBase, DirectServeJsonResource):
    def __init__(self, config: RequestDigitTokenConfig, api: ModuleApi):
        RequestDigitTokenBase.__init__(self, config, api)
        DirectServeJsonResource.__init__(self)

        self._api = api
        self._hs = api._hs
        self._store = api._store

    async def _async_render_POST(self, request):
        body = parse_json_object_from_request(request)

        assert_params_in_dict(body, ["client_secret", "email", "send_attempt"])

        client_secret = body["client_secret"]
        assert_valid_client_secret(client_secret)

        try:
            email = validate_email(body["email"])
        except ValueError as e:
            raise SynapseError(400, str(e))

        send_attempt = body["send_attempt"]

        if not await check_3pid_allowed(self._hs, "email", email, registration=True):
            raise SynapseError(
                403,
                "Your email domain is not authorized to register on this server",
            )

        await self._hs.get_identity_handler().ratelimit_request_token_requests(
            request, "email", email
        )

        existing_user_id = await self._store.get_user_id_by_threepid("email", email)

        if existing_user_id is not None:
            raise SynapseError(400, "Email is already in use")

        session_id = await self.send_digit_token(email, client_secret, send_attempt)

        threepid_send_requests.labels(type="email", reason="register").observe(
            send_attempt
        )

        return 200, {"sid": session_id}


class RequestDigitTokenValidateServlet(RequestDigitTokenBase, DirectServeJsonResource):
    def __init__(self, config: RequestDigitTokenConfig, api: ModuleApi):
        RequestDigitTokenBase.__init__(self, config, api)
        DirectServeJsonResource.__init__(self)

    async def _async_render_GET(self, request):
        client_secret = parse_string(request, "client_secret", required=True)
        assert_valid_client_secret(client_secret)

        sid = parse_string(request, "sid", required=True)
        token = parse_string(request, "token", required=True)

        await self.validate_digit_token(token, client_secret, sid)

        return 200, {}
