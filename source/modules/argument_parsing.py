import sys
from argparse import ArgumentParser, Namespace

from modules._platform import is_frozen, show_windows_help

# These custom handlings are necessary for frozen Windows builds to show
# argparse help messages properly


def error(parser: ArgumentParser, msg: str):
    if is_frozen() and sys.platform == "win32":
        from PyQt5.QtWidgets import QApplication
        from windows.dialog_window import DialogWindow

        app = QApplication([])
        dlg = DialogWindow(
            title="Error",
            text="An error occurred during parsing arguments:<br>" + parser.format_usage() + "<br>" + msg,
            accept_text="Quit",
            cancel_text=None,
            app=app,
        )
        dlg.show()
        sys.exit(app.exec())
    else:
        parser.error(msg)


def show_help(
    parser: ArgumentParser,
    update_parser: ArgumentParser,
    launch_parser: ArgumentParser,
    args: Namespace,
):
    if is_frozen() and sys.platform == "win32":
        if args.command == "update":
            show_windows_help(update_parser)
        elif args.command == "launch":
            show_windows_help(launch_parser)
        else:
            show_windows_help(parser)
    else:
        if args.command == "update":
            update_parser.print_help()
        elif args.command == "launch":
            launch_parser.print_help()
        else:
            parser.print_help()
