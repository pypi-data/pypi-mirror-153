from typing import ValuesView, Mapping
from rich.table import Table
from rich.console import Console, group
from rich.padding import Padding
from rich import box
from filum.helpers import timestamp_to_iso
from rich.markdown import Markdown
from rich.theme import Theme


console = Console(
    theme=Theme({'markdown.block_quote': 'yellow'}),
    style='on black')


class RichView:
    def __init__(self):
        self.console = console

    def stringify(self, row: ValuesView) -> tuple:
        '''Turns each item in the SQL query result into a string
        that can be passed to Table().add_row
        '''
        return tuple(str(i) for i in row)

    def display_table(self, row_list: list) -> None:
        '''Construct a new table each time to prevent concatenating
        new tables together each time the "all" command is called in the
        interactive shell.
        '''
        table = Table(box=box.SIMPLE, expand=True)
        table.add_column('', style='green')
        table.add_column('Title')
        table.add_column('Posted')
        table.add_column('Saved')
        table.add_column('Score')
        table.add_column('Source')
        table.add_column('Tags')
        # Convert each sqlite3.Row object to a dict
        rows = [dict(row) for row in row_list]
        for row in rows:
            row['posted_timestamp'] = timestamp_to_iso(row['posted_timestamp'])
            row['saved_timestamp'] = timestamp_to_iso(row['saved_timestamp'])
            table.add_row(*self.stringify(row.values()))
        self.console.print(table)

    def display_top_level(self, item: Mapping) -> str:
        timestamp = timestamp_to_iso(item['posted_timestamp'])
        to_print = (
            f'\n[bold bright_yellow]{item["author"]}[/bold bright_yellow] '
            f'{item["score"]} [blue]{timestamp}[/blue] {item["permalink"]}\n\n'
            f'✎ {item["title"]}\n'
            )
        if item['body']:
            to_print += f'{item["body"]}\n'

        return to_print

    def display_indented(self, results: list):
        @group()
        def make_panels(results: list):
            for result in results:
                text = Markdown(result['text'])
                timestamp = ''
                indent = result["depth"] + 2
                if result['timestamp']:
                    timestamp = timestamp_to_iso(result['timestamp'])
                if result['score'] is not None:
                    score = result['score']
                else:
                    score = ''
                header = (
                    f'\n¬ [bold bright_cyan]{result["author"]}[/bold bright_cyan] '
                    f'[green]{score}[/green] [blue]{timestamp}[/blue]\n'
                    )

                yield Padding(header, (0, 0, 0, indent))
                yield Padding(text, (0, 0, 0, indent + 1))

        return make_panels(results)

    def display_thread(self, top_level, indented, pager=True):

        if not pager:
            self.console.print(top_level)
            self.console.print(indented)
        elif pager:
            with self.console.pager(styles=True):
                # Only works if terminal pager supports colour
                self.console.print(top_level)
                self.console.print(indented)
