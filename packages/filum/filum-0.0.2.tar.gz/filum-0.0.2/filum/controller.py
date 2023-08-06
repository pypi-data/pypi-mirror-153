import sys
import traceback

from rich.console import Console

from filum.download import Download
from filum.models import ItemAlreadyExistsError

console = Console()


class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def download_thread(self, url):
        return Download(url).run()

    def add_thread(self, thread):
        try:
            self.model.insert_row(thread['parent_data'], 'ancestors')
            for comment in thread['comment_data']:
                self.model.insert_row(thread['comment_data'][comment], 'descendants')
        except ItemAlreadyExistsError:
            # TODO: Allow updating of existing thread
            print('This item already exists in your database.')
            sys.exit(0)
        except Exception:
            traceback.print_exc()

    def show_all_ancestors(self):
        results = self.model.select_all_ancestors()
        self.view.display_table(results)

    '''
    def show_one_ancestor(self, id):
        columns = ('row_id', 'num', 'permalink', 'author', 'posted_timestamp', 'score', 'body', 'title')
        results = self.model.select_one_ancestor(columns, id)
        return self.view.display_top_level(results)

    def show_all_descendants(self, ancestor):
        results = self.model.select_all_descendants(ancestor)
        return self.view.display_indented(results)
    '''

    def display_thread(self, id, pager, pager_colours):
        columns = ('row_id', 'num', 'permalink', 'author', 'posted_timestamp',
                   'score', 'body', 'title')
        ancestor_query = self.model.select_one_ancestor(columns, id)
        top_level = self.view.display_top_level(ancestor_query)
        descendants_query = self.model.select_all_descendants(id)
        indented = self.view.display_indented(descendants_query)
        self.view.display_thread(top_level, indented, pager=pager, pager_colours=pager_colours)

    def delete(self, ancestor):
        self.model.delete(ancestor)

    def get_ancestors_length(self):
        return self.model.get_ancestors_length()
