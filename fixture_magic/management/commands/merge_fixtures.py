try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.core.management.base import BaseCommand

def write_json(output):
    try:
        # check our json import supports sorting keys
        json.dumps([1], sort_keys=True)
    except TypeError:
        print(json.dumps(output, indent=2))
    else:
        print(json.dumps(output, sort_keys=True, indent=2))

class Command(BaseCommand):
    help = ('Merge a series of fixtures and remove duplicates.')
    args = '[file ...]'

    def handle(self, *filenames, **options):
        """
        Load a bunch of json files.  Store the pk/model in a seen dictionary.
        Add all the unseen objects into output.
        """
        output = []
        seen = {}

        for fn in filenames:
            with open(fn) as f:
                data = json.loads(f.read())
                for instance in data:
                    key = '%s|%s' % (instance['model'], instance['pk'])
                    if key not in seen:
                        seen[key] = 1
                        output.append(instance)

        write_json(output)
