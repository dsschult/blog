from .entry import Entries

blog_entries = Entries()


class Obj:
    def __init__(self, template, *args, **kwargs):
        self.template = template
        self.args = args
        self.kwargs = kwargs

def main():
    e = blog_entries.get_last_n()
    return Obj('main.html', entries=e)

def about():
    return Obj('about.html')

def entries():
    e = blog_entries.get_last_n(100000000000)
    return Obj('main.html', entries=e)

def entry(name):
    e = blog_entries.get(name)
    return Obj('entries.html', **e)


# define all the routes  (route, handler, wildcard_args)
routes = [
    ('index.html', main),
    ('about.html', about),
    ('entries.html', entries),
    ('entries/*.html', entry, blog_entries.get_names()),
]