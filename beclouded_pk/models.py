from django.db import models

from .transparent_hashs import TransparentHashFactory


class BecloudedPKModel(models.Model, TransparentHashFactory):
    class Meta:
        abstract = True

    def _get_beclouded_pk(self) -> str:
        return self.encode_to_thash(self.pk)

    beclouded_pk = property(fget=_get_beclouded_pk)