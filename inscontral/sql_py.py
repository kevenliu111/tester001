import inscontral.models
from django.core import serializers

def udstate(state):
    stacon = inscontral.models.State.objects.create()
    stacon.state = state
    re = stacon.save()
    return re


def gdstate():
    # re = ''
    mdgd = inscontral.models.State.objects.latest('add_date')
    stacon = {}
    stacon['state'] = mdgd.state
    stacon['id'] = mdgd.id
    re = stacon
    print(stacon)
    return re
