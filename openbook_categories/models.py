from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
from openbook_auth.models import User
from django.utils.translation import ugettext_lazy as _

from openbook_communities.models import Community


class Category(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_categories', null=True)
    name = models.CharField(_('name'), max_length=settings.CATEGORY_NAME_MAX_LENGTH, blank=False, null=False,
                            unique=True)
    title = models.CharField(_('title'), max_length=settings.CATEGORY_TITLE_MAX_LENGTH, blank=False, null=False)
    description = models.CharField(_('description'), max_length=settings.CATEGORY_DESCRIPTION_MAX_LENGTH, blank=False,
                                   null=True, )
    created = models.DateTimeField(editable=False)
    communities = models.ManyToManyField(Community, related_name='categories')
    avatar = models.ImageField(_('avatar'), blank=False, null=True)

    @classmethod
    def create_category(cls, creator, name, emoji, title=None, description=None, avatar=None):
        category = cls.objects.create(creator=creator, name=name, emoji=emoji, title=title, description=description,
                                      avatar=avatar)

        return category

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(Category, self).save(*args, **kwargs)
