from uuid import uuid4

import platform
import sys
from contextlib import AbstractContextManager
from requests import Session, Response
from typing import List, Optional

from dnastack.common.events import EventSource
from dnastack.common.logger import get_logger
from dnastack.constants import __version__
from dnastack.http.authenticators.abstract import Authenticator


class AuthenticationError(RuntimeError):
    """ Authentication Error """


class HttpError(RuntimeError):
    def __init__(self, response: Response):
        super(HttpError, self).__init__(response)

    @property
    def response(self) -> Response:
        return self.args[0]

    def __str__(self):
        response: Response = self.response
        return f'HTTP {response.status_code}: {response.text}'


class HttpSession(AbstractContextManager):
    def __init__(self,
                 uuid: Optional[str] = None,
                 authenticators: List[Authenticator] = None,
                 suppress_error: bool = True,
                 enable_auth: bool = True):
        super().__init__()

        self.__id = uuid or str(uuid4())
        self.__logger = get_logger(f'{type(self).__name__}/{self.__id}')
        self.__authenticators = authenticators
        self.__session: Optional[Session] = None
        self.__suppress_error = suppress_error
        self.__enable_auth = enable_auth

        # This will inherit event types from
        self.__events = EventSource(['authentication-before',
                                     'authentication-ok',
                                     'authentication-failure',
                                     'authentication-ignored',
                                     'initialization-before',
                                     'refresh-before',
                                     'refresh-ok',
                                     'refresh-failure',
                                     'session-restored',
                                     'session-not-restored',
                                     'session-revoked'],
                                    origin=self)

        if self.__authenticators:
            for authenticator in self.__authenticators:
                self.__events.set_passthrough(authenticator.events)

        if not self.__enable_auth:
            self.__logger.info('Authentication has been disable for this session.')

    @property
    def events(self) -> EventSource:
        return self.__events

    @property
    def _session(self):
        if not self.__session:
            self.__session = Session()
            self.__session.headers.update({
                'User-Agent': self.generate_http_user_agent()
            })

        return self.__session

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self.close()

    def submit(self,
               method: str,
               url: str,
               retry_with_reauthentication: bool = True,
               retry_with_next_authenticator: bool = False,
               authenticator_index: int = 0,
               **kwargs) -> Response:
        session = self._session

        self.__logger.debug(f'{method.upper()} {url}')

        authenticator: Optional[Authenticator] = None
        if self.__enable_auth:
            if self.__authenticators:
                self.__logger.debug(f'AUTH: authenticator => {authenticator_index + 1}/{len(self.__authenticators)}')
                self.__logger.debug(f'AUTH: retry_with_reauthentication => {retry_with_reauthentication}')
                self.__logger.debug(f'AUTH: retry_with_next_authenticator => {retry_with_next_authenticator}')

                if authenticator_index < len(self.__authenticators):
                    authenticator = self.__authenticators[authenticator_index]
                else:
                    raise AuthenticationError('Exhausted all authentication methods but still unable to get successful '
                                              'authentication')

                self.__logger.debug(f'AUTH: session_id => {authenticator.session_id}')

                authenticator.before_request(session)
            else:
                self.__logger.debug(f'AUTH: no authenticators configured')
        else:
            self.__logger.debug(f'AUTH: the authentication has been disabled')
            self.events.dispatch('authentication-ignored', dict(method=method, url=url))

        http_method = method.lower()
        response = getattr(self._session, http_method)(url, **kwargs)

        if response.ok:
            return response
        else:
            if self.__suppress_error:
                return response

            status_code = response.status_code

            if self.__enable_auth:
                if status_code == 403 and authenticator:
                    authenticator.revoke()
                    if retry_with_reauthentication:
                        # Initiate the reauthorization process.
                        return self.submit(method,
                                           url,
                                           retry_with_reauthentication=False,
                                           retry_with_next_authenticator=True,
                                           authenticator_index=authenticator_index,
                                           **kwargs)
                    elif retry_with_next_authenticator:
                        return self.submit(method,
                                           url,
                                           retry_with_reauthentication=True,
                                           retry_with_next_authenticator=False,
                                           authenticator_index=authenticator_index + 1,
                                           **kwargs)
                    else:
                        # No more retries.
                        raise HttpError(response)
                else:
                    # Non-access-denied error will be handled here.
                    raise HttpError(response)
            else:
                # No-auth requests will just throw an exception.
                raise HttpError(response)

    def get(self, url, **kwargs) -> Response:
        return self.submit('get', url, **kwargs)

    def post(self, url, **kwargs) -> Response:
        return self.submit('post', url, **kwargs)

    def close(self):
        if self.__session:
            self.__id = None
            self.__session.close()
            self.__session = None

    def __del__(self):
        self.close()

    @staticmethod
    def generate_http_user_agent(comments: Optional[List[str]] = None) -> str:
        # NOTE: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent
        interested_module_names = [
            'IPython',  # indicates that it is probably used in a notebook
            'unittest',  # indicates that it is used by a test code
        ]

        final_comments = [
            f'Platform/{platform.platform()}',  # OS information + CPU architecture
            'Python/{}.{}.{}'.format(*sys.version_info),  # Python version
            *(comments or list()),
            *[
                f'Module/{interested_module_name}'
                for interested_module_name in interested_module_names
                if interested_module_name in sys.modules
            ]
        ]

        return f'dnastack-client/{__version__} {" ".join(final_comments)}'.strip()
