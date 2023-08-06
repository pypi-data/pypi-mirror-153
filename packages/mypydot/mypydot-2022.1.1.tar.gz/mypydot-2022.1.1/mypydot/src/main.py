from mypydot.src.logging_manager import LoggingConf
from mypydot.src.app import Opt, App
from typing import Callable
import argparse


def main(test_param=None) -> Callable:
    """Options can be :


        - create : It's going to initialize a new dotfiles folder and sync
        the available symlinks

        - sync : Will try to sync new dotfiles

        """
    parser = None
    if not test_param:
        parser = argparse.ArgumentParser(
            description='Organize your dotfiles using MYPYDOTFILES'
        )
        parser.add_argument(
            '--option', type=str,
            help='Basic action, could be [create, sync]',
            choices=[Opt.CREATE, Opt.SYNC]
        )

    cmd = test_param or parser.parse_args().option
    LoggingConf()
    app = App()
    fun = app.parse_opt(cmd)
    return fun


def entry_point():
    fun = main()
    fun()


if __name__ == '__main__':
    f = main()
    f()
