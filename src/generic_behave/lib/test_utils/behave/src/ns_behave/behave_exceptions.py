"""Contains all the exceptions for behave framework"""


class BaseError(Exception):
    """Base class for other exceptions"""

    def __init__(self, msg: str) -> None:
        Exception.__init__(self, msg)


class InvalidStackError(BaseError):
    """Raised when the stack name in correct in behave.ini"""

    def __init__(self, environment: str) -> None:
        """Initialize an InvalidStackError

        Args:
            environment: The environment set by the user in behave.ini

        """
        self.environment = environment
        msg = (
            f"\nYou must specify a full stack name in the behave.ini file for {self.environment}"
            + (
                r"""

                                                        ____
             ___                                      .-~    '.
            `-._~-.                                  / /  ~@\   )
                 \  \                               | /  \~\.  `\
                 ]  |                              /  |  |< ~\(..)
                /   !                        _.--~T   \  \<   .,,
               /   /                 ____.--~ .    _  /~\ \< /
              /   /             .-~~'        /|   /o\ /-~\ \_|
             /   /             /     )      |o|  / /|o/_   '--'
            /   /           .-'(     l__   _j \_/ / /\|~    .
            /    l          /    \       ~~~|    `/ / / \.__/l_
            |     \     _.-'      ~-\__     l      /_/~-.___.--~
            |      ~---~           /   ~~'---\_    __[o,
            l  .                _.    ___     _>-/~
            \  \     .      .-~   .-~   ~>--'  /
             \  ~---'            /         _.-'
              '-.,_____.,_  _.--~\     _.-~
                          ~~     (   _}
                                 `. ~(
                                   )  \
                             /,`--'~\--'~\
            """
            )
        )
        super().__init__(msg)


class LocalDevError(BaseError):
    """Raised when local dev is not running on the computer"""

    def __init__(self) -> None:
        """Initialize an LocalDevError"""
        msg = (
            "\nHey Narrative Scientist... In order to run tests against "
            "local-dev you kind of have to have local-dev running and healthy!! Go ahead and check on that!!"
            + r"""
                                                     ___._
                                                   .'  <0>'-.._
                                                  /  /.--.____")
                                                 |   \   __.-'~
                                                 |  :  -'/
                                                /:.  :.-'
__________                                     | : '. |
'--.____  '--------.______       _.----.-----./      :/
        '--.__            `'----/       '-.      __ :/
              '-.___           :           \   .'  )/
                    '---._           _.-'   ] /  _/
                         '-._      _/     _/ / _/
                             \_ .-'____.-'__< |  \___
                               <_______.\    \_\_---.7
                              |   /'=r_.-'     _\\ =/
                          .--'   /            ._/'>
                        .'   _.-'
                       / .--'
                      /,/
                      |/`)
                      'c=,
        """
        )
        super().__init__(msg)


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


class TestSetupError(BaseError):
    """Raised when the framework can not properly setup the test environment"""

    def __init__(self, environment: str) -> None:
        """Initialize an TestConnectionError

        Args:
            environment: The environment set by the user in behave.ini

        """
        self.environment = environment
        msg = (
            f"\nCould not setup the {self.environment} test environment properly in the behave before_test hook."
            + r"""
                           <\              _
                            \\          _/{
                     _       \\       _-   -_
                   /{        / `\   _-     - -_
                 _~  =      ( @  \ -        -  -_
               _- -   ~-_   \( =\ \           -  -_
             _~  -       ~_ | 1 :\ \      _-~-_ -  -_
           _-   -          ~  |V: \ \  _-~     ~-_-  -_
        _-~   -            /  | :  \ \            ~-_- -_
     _-~    -   _.._      {   | : _-``               ~- _-_
  _-~   -__..--~    ~-_  {   : \:}
=~__.--~~              ~-_\  :  /
                           \ : /__
                          //`Y'--\\      =
                         <+       \\
                          \\      WWW
                          MMM
               """
        )
        super().__init__(msg)
