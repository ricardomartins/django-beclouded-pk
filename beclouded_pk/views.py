# coding=utf-8
from django.views.generic.detail import DetailView

from .transparent_hashs import TransparentHashFactory


class BecloudedPKDetailView(DetailView, TransparentHashFactory):
    beclouded_pk_url_kwarg = 'becloudedpk'  # Override to change the url name

    def get_object(self, queryset=None):
        beclouded_pk = self.kwargs.get(self.beclouded_pk_url_kwarg, None)
        try:
            pk = self.decode_from_thash(beclouded_pk)
        except ValueError:
            raise AttributeError  # TODO: give proper message to this exception
        else:
            self.kwargs['pk'] = format(pk, '10')

        return super().get_object(queryset)

