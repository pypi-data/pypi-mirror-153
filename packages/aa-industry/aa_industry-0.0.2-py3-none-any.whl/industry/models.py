from django.db import models
from django.contrib.auth import get_user_model
from esi.models import Token

from django.utils.translation import ugettext as _


User = get_user_model()


class Industry(models.Model):
    pass


class UserToken(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    token = models.ForeignKey(Token, blank=False, on_delete=models.CASCADE)
    character_id = models.IntegerField(db_index=True, help_text="The ID of the EVE character who authenticated by SSO.")

    class Meta:
        ordering = ['user']
        verbose_name = _('Industry User x Token')
        verbose_name_plural = _('Industry User x Tokens')

    def __str__(self):
        return self.user.profile.main_character.character_name


class Facility(models.Model):
    facility_id = models.BigIntegerField(_('Facility'), null=False, blank=False)
    name = models.CharField(_('Name'), null=False, blank=False, max_length=2048)
    owner_id = models.BigIntegerField(_('Owner Id'), null=False, blank=False)
    solar_system_id = models.BigIntegerField(_('Solar System Id'), null=False, blank=False)
    type_id = models.BigIntegerField(_('Type'), null=False, blank=False)

    class Meta:
        ordering = ['name']
        verbose_name = _('Facility')
        verbose_name_plural = _('Facilities')
