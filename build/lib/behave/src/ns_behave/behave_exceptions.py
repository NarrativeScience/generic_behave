"""Contains all the exceptions for behave framework"""


class BaseError(Exception):
    """Base class for other exceptions"""

    def __init__(self, msg: str) -> None:
        Exception.__init__(self, msg)


class TestConnectionError(BaseError):
    """Raised when the framework can not reach the test environment"""

    def __init__(self, environment: str) -> None:
        """Initialize an TestConnectionError

        Args:
            environment: The environment set by the user in behave.ini

        """
        self.environment = environment
        msg = (
            f"\nCould not connect to the test environment."
            f"Check to make sure local-dev is running or you have a good connection to {self.environment}"
            + r"""
                          _._
                        _/:|:
                       /||||||.
                       ||||||||.
                      /|||||||||:
                     /|||||||||||
                    .|||||||||||||
                    | ||||||||||||:
                  _/| |||||||||||||:_=---.._
                  | | |||||:'''':||  '~-._  '-.
                _/| | ||'         '-._   _:    ;
                | | | '               '~~     _;
                | '                _.=._    _-~
             _.~                  {     '-_'
     _.--=.-~       _.._          {_       }
 _.-~   @-,        {    '-._     _. '~==+  |
('          }       \_      \_.=~       |  |
`======='  /_         ~-_    )         <_oo_>
  `-----~~/ /'===...===' +   /
         <_oo_>         /  //
                       /  //
                      <_oo_>
               """
        )
        super().__init__(msg)
