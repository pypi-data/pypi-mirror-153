from django.apps import apps
from django.db.models import Q, Model
from django.shortcuts import _get_queryset

from djackal.exceptions import NotFound
from djackal.settings import djackal_settings


def get_object_or_None(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def get_object_or(klass, this=None, *args, **kwargs):
    return get_object_or_None(klass, *args, **kwargs) or this


def get_object_or_404(model, **fields):
    obj = get_object_or_None(model, **fields)
    if obj is None:
        raise NotFound(model=model)
    return obj


def model_update(instance, commit=True, **fields):
    for key, value in fields.items():
        setattr(instance, key, value)

    if commit:
        instance.save()
    return instance


def get_model(label, *args, **kwargs):
    if djackal_settings.SINGLE_APP:
        if djackal_settings.SINGLE_APP_NAME and len(label.split('.')) == 1:
            return apps.get_model('{}.{}'.format(djackal_settings.SINGLE_APP_NAME, label))
    return apps.get_model(label, *args, **kwargs)


def gen_q(value, *filter_keywords):
    q_object = Q()
    for q in filter_keywords:
        q_object |= Q(**{q: value})
    return q_object


def auto_f_key(**kwargs):
    result = dict()

    for key, value in kwargs.items():
        if type(value) is int:
            result['{}_id'.format(key)] = value
        elif isinstance(value, Model):
            result[key] = value
        else:
            raise ValueError('unknown type: {}'.format(type(value)))
    return result
