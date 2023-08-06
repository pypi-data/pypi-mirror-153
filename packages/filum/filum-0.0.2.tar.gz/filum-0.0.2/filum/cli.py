import argparse
import configparser
import pathlib
import platform
import subprocess
import sys
from cmd import Cmd

from filum.controller import Controller
from filum.models import FilumModel
from filum.validation import InvalidInputError, is_valid_id, is_valid_url
from filum.view import RichView


def parser():
    parser = argparse.ArgumentParser(
                                description='Archive discussion threads',
                                prog='filum'
                                    )

    subparsers = parser.add_subparsers(dest='subparser')

    parser_add = subparsers.add_parser('add', help='add a URL')
    parser_add.add_argument('url', nargs='+', type=str, help='add a URL')
    parser_add.set_defaults(parser_add=True)

    parser_all = subparsers.add_parser('all', help='show all saved top-level items')
    parser_all.set_defaults(parser_all=False)

    parser_thread = subparsers.add_parser('thread', help='display a saved thread')
    parser_thread.add_argument('id', nargs='+', type=int)

    parser_delete = subparsers.add_parser('delete', help='delete a saved thread')
    parser_delete.add_argument('id', nargs='+', type=int)

    parser_config = subparsers.add_parser('config', help='open config file')
    parser_config.set_defaults(parser_config=False)

    parser.add_argument('-i', action='store_true', help='interactive mode')
    args = parser.parse_args()

    return args


def main():

    class FilumShell(Cmd):
        intro = 'filum interactive mode'
        prompt = 'filum > '

        def onecmd(self, line):
            try:
                return super().onecmd(line)
            except Exception as err:
                print(err)
                return False

        def emptyline(self):
            # Do nothing if an empty line is entered at the prompt
            pass

        def do_add(self, arg):
            '''Add a URL to the filum database: $ add <url>'''
            if arg == '':
                print('Please supply a URL.')
                return False
            add(arg)

        def do_all(self, arg):
            '''Show all top-level items currently saved in the filum database: $ all'''
            show_all()

        def do_thread(self, arg):
            '''Display a thread given its top-level selector: $ thread 1.\n
            Top-level selectors are contained in the left-most column in the table shown by the "all" command.'''
            try:
                show_thread(int(arg))
            except ValueError:
                print('Please enter a valid integer.')

        def do_delete(self, arg):
            '''Delete a thread given its top-level selector: $ thread 1.\n
            Top-level selectors are contained in the left-most column in the table shown by the "all" command.'''
            try:
                delete(int(arg))
            except ValueError:
                print('Please enter a valid integer.')

        def do_config(self, arg):
            '''Open the config file in an editor. Change settings by modifying the parameter values: $ config'''
            try:
                open_config()
            except Exception as err:
                print(err)

        def do_quit(self, arg):
            '''Quit the interactive session using 'quit' or CTRL-D'''
            sys.exit(0)

        def do_EOF(self, arg):
            '''Quit the interactive session using 'quit' or CTRL-D'''
            sys.exit(0)

    valid_id_message = 'Please enter a valid thread ID (positive integer). Run `filum all` to see a list of thread IDs.'

    config = configparser.ConfigParser()
    config_filepath = pathlib.Path(__file__).parent.resolve() / 'config.ini'
    config.read(config_filepath)

    c = Controller(FilumModel(), RichView())

    def add(url) -> None:
        try:
            is_valid_url(url)
            thread = c.download_thread(url)
            c.add_thread(thread)
        except InvalidInputError as err:
            print(err)

    def show_thread(id: int) -> None:
        try:
            is_valid_id(id)
            c.display_thread(
                id,
                pager=config.getboolean('output', 'pager'),
                pager_colours=config.getboolean('output', 'pager_colours')
                )
        except InvalidInputError as err:
            print(err)
        except IndexError:
            print(valid_id_message)

    def show_all() -> None:
        c.show_all_ancestors()

    def delete(id: int) -> None:
        try:
            if confirm_delete():
                is_valid_id(id)
                ancestors_length = c.get_ancestors_length()
                print(ancestors_length)
                success = True if id <= ancestors_length else False
                if success:
                    c.delete(id)
                    print(f'Thread no. {id} deleted.')
                else:
                    print(f'Thread no. {id} does not exist.\n{valid_id_message}')
            else:
                print('Delete action cancelled.')
        except InvalidInputError as err:
            print(err)
        except IndexError:
            print(valid_id_message)

    def confirm_delete() -> bool:
        yes_no = ''

        while yes_no not in ('y', 'n'):
            yes_no = input('Are you sure you want to delete this thread? [y/n] ')
            if yes_no == 'y':
                return True
            elif yes_no == 'n':
                return False
            else:
                print('Enter "y" for yes or "n" for no.')
                continue

    def open_config():
        # filepath = pathlib.Path(__file__).parent.resolve() / 'config.ini'
        if platform.system() == 'Darwin':       # macOS
            subprocess.run(('open', config_filepath))
        elif platform.system() == 'Windows':    # Windows
            subprocess.run('notepad', config_filepath)
        else:                                   # Linux variants
            subprocess.run(('nano', config_filepath))

    description = (
        'filum - archive discussion threads from the command line.\n\n'
        'Usage:\n'
        'filum all\nfilum add <url>\nfilum thread <id>\nfilum delete <id>\n\n'
        'filum is a tool to save discussion threads from Reddit, Hacker News, and Stack Exchange on your PC. '
        'Like a bookmarking tool, but the text itself is saved locally. Worry no more about deleted threads.\n\n'
        'Run "filum -h" for a full list of options.'
    )

    args = parser()

    if args.i:
        FilumShell().cmdloop()

    if args.subparser == 'config':
        print('Opening config file...')
        open_config()

    if args.subparser == 'add':
        add(args.url[0])

    elif args.subparser == 'all':
        show_all()

    elif args.subparser == 'thread':
        show_thread(args.id[0])

    elif args.subparser == 'delete':
        delete(args.id[0])

    else:
        print(description)


if __name__ == '__main__':
    main()
