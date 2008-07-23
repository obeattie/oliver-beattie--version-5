"""Request-related utils."""
from django.http import Http404

def check_key(dictionary, key_name, fail_exception=Http404):
    """Checks the presence of the key in the passed dictionary, raising an exception
       if it is not (exception defaults to Http404)."""
    assert isinstance(dictionary, dict)
    if not key_name in dictionary:
        raise fail_exception(u'Key \'%s\' not found in dictionary' % key_name)
