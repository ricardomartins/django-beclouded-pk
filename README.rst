============
Beclouded Pk
============

Beclouded Pk is a simple Django app that provides a simple way to obfuscate(or becloud) primary keys in URLs (or anything if you want).

It simply hashes the provide primary key, and appends to it the same primary key.

It's not secure, and it's not meant to be secure, you should not rely on it to prevent people to access locations they should not have access to.
It's main use is to prevent people from traversing your site when using incremental primary keys, but it does not hide the incremental nature of the primary key, or even the key itself.


Quick start
===========

1. Models that should have the capability to becloud their primary key should inherit ``beclouded_pk.BecloudedPKModel``::

      from beclouded_pk import BecloudedPKModel

      class AModel(BecloudedPKModel):
          ...

2. DetailViews that should have the capability to read beclouded primary keys should inherit ``beclouded_pk.BecloudedPKDetailView``::

      from beclouded_pk import BecloudedPKDetailView
      from . import models

      class ADetailView(BecloudedPKDetailView):
          model = models.AModel

3. URLs to the BecloudedPKDetailView should have a ``becloudedpk`` argument::

      url(r'^(?P<becloudedpk>.+)/$', ADetailView.as_view(), name='a_model_detail),

4. URLs should be constructed using the ``beclouded_pk`` field from the model that inherits``BecloudedPKModel``::

      {% url 'a_model_detail' a_model.beclouded_pk %}
