import sys
import traceback

from rich.console import Console

from filum.download import Download
from filum.database import Database, ItemAlreadyExistsError
from filum.view import RichView

console = Console()


class Controller(object):
    def __init__(self):
        self.database = Database()
        self.view = RichView()

    def download_thread(self, url):
        return Download(url).run()

    def add_thread(self, thread):
        try:
            self.database.insert_row(thread['parent_data'], 'ancestors')
            for comment in thread['comment_data']:
                self.database.insert_row(thread['comment_data'][comment], 'descendants')
        except ItemAlreadyExistsError:
            # TODO: Allow updating of existing thread
            print('This item already exists in your database.')
            raise ItemAlreadyExistsError
            sys.exit(0)
        except Exception:
            traceback.print_exc()

    def update_thread(self, thread: dict):
        ancestor_id = self.database.update_ancestor(thread['parent_data'])
        self.database.delete_descendants(ancestor_id)
        for comment in thread['comment_data']:
            self.database.insert_row(thread['comment_data'][comment], 'descendants')

    def get_permalink(self, id: int) -> str:
        return self.database.select_permalink(id)

    def check_thread_exists(self, id):
        self.database.select_one_ancestor(id)

    def show_all_ancestors(self):
        results = self.database.select_all_ancestors()
        table = self.view.create_table(results)
        self.view.filum_print(table)

    def display_thread(self, id, pager, pager_colours, cond='', **kwargs):
        ancestor_query = self.database.select_one_ancestor(id, cond=cond, **kwargs)
        top_level = self.view.create_thread_header(ancestor_query)

        descendants_query = self.database.select_all_descendants(id, cond=cond, **kwargs)
        indented = self.view.create_thread_body(descendants_query)

        self.view.display_thread(top_level, indented, pager=pager, pager_colours=pager_colours)

    def delete(self, ancestor):
        self.database.delete_descendants(ancestor)
        self.database.delete_ancestor(ancestor)

    def get_ancestors_length(self):
        return self.database.get_ancestors_length()

    def modify_tags(self, id: int, add=True, **kwargs):
        '''Add or delete tags of a top-level item in the "ancestor" table
        :param int id: the ID of the item (in consecutive ascending order)
        :param bool add: default is to add tags, otherwise delete tags
        :key list tags: user-supplied tags to be added

        '''
        current_tags = self.database.get_tags(id)
        if current_tags is not None:
            current_tags = current_tags.split(', ')
        else:
            current_tags = []
        entered_tags = [tag.lower() for tag in kwargs['tags']]
        if add:
            # Ignore user-supplied tags that already exist
            new_tags = ', '.join(set(current_tags).union(entered_tags))
        else:
            new_tags = ', '.join([tag for tag in current_tags if tag not in entered_tags])
            if new_tags == '':
                new_tags = None
        self.database.update_tags(id, new_tags)

    def search(self, column, searchstr):
        results = self.database.search(column, searchstr)
        table = self.view.create_table(results)
        self.view.filum_print(table)
