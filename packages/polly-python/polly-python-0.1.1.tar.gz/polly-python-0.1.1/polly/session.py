from requests import Session
import os
import base64
import json


class PollySession(Session):
    """
    This class contain function to create session for
    polly.

    ``Args:``
        |  ``token (str):`` token copy from polly.

    ``Returns:``
        |  None

    To use this function


    .. code::


            from polly.session import PollySession
            session = PollySession(token)

    """

    def __init__(self, TOKEN, env="polly"):
        Session.__init__(self)
        try:
            # for python version >= python3.8
            from importlib.metadata import version

            version = version("polly-python")
        except ImportError:
            # for python version < python3.8
            import pkg_resources

            version = pkg_resources.get_distribution("polly-python").version
        client = os.getenv("POLLY_SERVICE")
        if client is not None:
            version = version + "/" + client
        else:
            version = version + "/local"

        # check to differentiate between api auth key and refresh token
        # this check is based on the premise that

        # REFRESH TOKEN =>  It is not base64 encoded string.
        # There are 5 parts of REFRESH_TOKEN(all seperated by `.`)
        # Part 1 -> base64 encoded json string-> contains cty(technology of token),
        # algorithm used to encode and encryption type
        # Part 2,Part 3, Part 4, Part 5 -> Not base64 encoded json.

        # API AUTH KEY => base64 encoded string, no `.` in between.

        # check applied
        # split the token by `.` and take the 1st part
        # if the 1st part is a base64 encoded json string
        # that means its a refresh token
        # because API AUTH KEY is if we decode it is not
        # base64 encoded json neither it has `.` in it.
        # decoding API AUTH KEY => gives decoded string

        try:
            json.loads(base64.b64decode(TOKEN.split(".")[0].encode("ascii") + b"=="))
            self.headers = {
                "Content-Type": "application/vnd.api+json",
                "Cookie": f"refreshToken={TOKEN}",
                "User-Agent": "polly-python/" + version,
            }
        except Exception:
            self.headers = {
                "Content-Type": "application/vnd.api+json",
                "x-api-key": f"{TOKEN}",
                "User-Agent": "polly-python/" + version,
            }
        self.env = env
