from datetime import datetime

from django.contrib.auth.models import User

from .meta import get_user_or_superuser
from .models import Log, LogItem
from .utils import get_local_date


def log(ref, model, action, user=None, old='', new='', transaction=None):
    _log = Log(user=get_user_or_superuser(user))
    _log.date = get_local_date()
    _log.ref = ref
    _log.model = model
    _log.action = action
    _log.transaction = transaction
    _log.save()

    if old and new:
        diff = {}
        for key in new.keys():
            if old[key] != new[key]:
                diff[key] = (old[key], new[key])
        for key in diff.keys():
            _log_item = LogItem()
            _log_item.log = _log
            _log_item.key = key
            _log_item.old = diff[key][0]
            _log_item.new = diff[key][1]
            _log_item.save()


def logs(ref, model):
    return Log.objects.all().filter(ref=ref).filter(model=model).order_by('-date')


