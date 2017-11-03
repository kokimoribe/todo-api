"""
JWT token validation

Heavily based on:
https://github.com/auth0-samples/auth0-python-api-samples/blob/master/00-Starter-Seed/server.py
"""

import functools

from flask import request
from jose import jwt

from todo.exceptions import UnauthorizedError

ALGORITHMS = ["RS256"]
AUDIENCE = 'https://todo-api-rd7qf9.herokuapp.com'
ISSUER = 'https://todo-api-rd7qf9.auth0.com/'

# cSpell: disable
RSA_KEY = {
    "alg": "RS256",
    "kty": "RSA",
    "use": "sig",
    "x5c": [
        "MIIDDTCCAfWgAwIBAgIJdmhdQkfTCK5jMA0GCSqGSIb3DQEBCwUAMCQxIjAgBgNVBAMTGXRvZG8tYXBpLXJkN3FmOS5hdXRoMC5jb20wHhcNMTcxMDE3MDIxMTM4WhcNMzEwNjI2MDIxMTM4WjAkMSIwIAYDVQQDExl0b2RvLWFwaS1yZDdxZjkuYXV0aDAuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzUKYXWNcKUhe+S6gOh07C/Gp3OEVCrIHyjSOFKH+0C72D+eZJNWxNdvVwt0z08zLw1geZlHdjKcqKUr+eb/UCUgsEIQrXoHzxHZtZ5LudlUu9w7AVpvfsIhW3DJWXG6w9DHW7+u4pJ9uHdS7/yxrLDzA+xvFj/Y1gIMQf9SZoVwB090qrCyTYrCacjEZ0Yr1cH4/lxCvi5W+6Gg7sei5PK97c8fEfa4HS+6zImysSgyPeXuaCdXY2Dx9QSiQvNTrL58KM1GPTTfdC3bSgRmC3xvKUD2WIufK0Mywoz2nrA7KV3oIHaJ5MP/TdFdJonI3uc9UoxCWN568byp/CCFlBQIDAQABo0IwQDAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBQ+dk33WHZhCCQ8B7mk7ciK9i137DAOBgNVHQ8BAf8EBAMCAoQwDQYJKoZIhvcNAQELBQADggEBADcXd3IW3Y6uMD+GNsnKcMQC5kfTs5eMl8U1FQl8873BX0trhXQ6aUrW7+qvFAkGTszqKJ6G/YxpSHFknPCJtxr5XHr+NsZ4qFReNTbmvuT0yMKNx0Abwh810fBhTeJCckn1Mk9Gpj8Ru6FLqrR9KrNN8XShHHS3D1uXG4Dxo7gy9l0ctQt4f9xmO1EI6UHba6WJUoNee6WUxZ+m5dc8tyTRziWhz6T4xi/zBrjGrpantmaTMEm8TnPmy/8DoEd//8B2mwH56P1jEpnBUlON0gi8Xsw7xzRPtcznaYF2sVI2uxm+XimJ7hwjqAXvntaYIyuRXUnrZ5oli8wElJV0/7Y="  # pylint: disable=line-too-long
    ],
    "n": "zUKYXWNcKUhe-S6gOh07C_Gp3OEVCrIHyjSOFKH-0C72D-eZJNWxNdvVwt0z08zLw1geZlHdjKcqKUr-eb_UCUgsEIQrXoHzxHZtZ5LudlUu9w7AVpvfsIhW3DJWXG6w9DHW7-u4pJ9uHdS7_yxrLDzA-xvFj_Y1gIMQf9SZoVwB090qrCyTYrCacjEZ0Yr1cH4_lxCvi5W-6Gg7sei5PK97c8fEfa4HS-6zImysSgyPeXuaCdXY2Dx9QSiQvNTrL58KM1GPTTfdC3bSgRmC3xvKUD2WIufK0Mywoz2nrA7KV3oIHaJ5MP_TdFdJonI3uc9UoxCWN568byp_CCFlBQ",  # pylint: disable=line-too-long
    "e": "AQAB",
    "kid": "RkQ0Q0UxNUJBRkExMjg2Q0VGREU1NDIyMDI3NTIwNkRFQkZFMUZCMQ",
    "x5t": "RkQ0Q0UxNUJBRkExMjg2Q0VGREU1NDIyMDI3NTIwNkRFQkZFMUZCMQ"
}
# cSpell: enable


def get_token_auth_header():
    """Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise UnauthorizedError("Authorization header is expected")

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise UnauthorizedError("Authorization header must start with Bearer")
    elif len(parts) == 1:
        raise UnauthorizedError("Token not found")
    elif len(parts) > 2:
        raise UnauthorizedError("Authorization header must be Bearer token")

    token = parts[1]
    return token


def requires_auth(func):
    """Determines if the access token is valid
    """

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        """decorated"""
        token = get_token_auth_header()
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError:
            raise UnauthorizedError(
                "Invalid header. Use an RS256 signed JWT Access Token")

        if unverified_header["alg"] == "HS256":
            raise UnauthorizedError(
                "Invalid header. Use an RS256 signed JWT Access Token")

        if unverified_header["kid"] != RSA_KEY["kid"]:
            raise UnauthorizedError("Unable to find appropriate key")

        try:
            payload = jwt.decode(
                token,
                RSA_KEY,
                algorithms=ALGORITHMS,
                audience=AUDIENCE,
                issuer=ISSUER)

        except jwt.ExpiredSignatureError:
            raise UnauthorizedError("Token has expired")

        except jwt.JWTClaimsError:
            raise UnauthorizedError(
                "Incorrect claims. Please check the audience and issuer.")

        user_id = payload["sub"]
        return func(*args, **kwargs, user_id=user_id)

    return wrapped
