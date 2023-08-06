import attr


@attr.s(auto_attribs=True, frozen=True)
class RequestDigitTokenConfig:
    token_length: int
    token_lifetime: int
