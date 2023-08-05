import time
from django.db import models
from tinymce import models as tiny_models
from django.contrib.auth.models import User
from django.utils.text import slugify

from BaseCode import settings
User = settings.AUTH_USER_MODEL

class CMS(models.Model):
    id=models.AutoField(primary_key=True,)
    title = models.CharField(max_length=255,null=False,help_text="Title Must Be Unique Because Slug is created from the title")
    slug = models.SlugField(max_length=255,null=False,unique=True)
    content=tiny_models.HTMLField(null=False)
    created_at = models.IntegerField(default=int(time.time()))
    updated_at = models.IntegerField(default=int(time.time()))
    created_by = models.ForeignKey(User,blank=True,on_delete=models.CASCADE, related_name='created_by_user')
    updated_by = models.ForeignKey(User, blank=True,on_delete=models.CASCADE, related_name='updated_by_user')

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs): 
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = "CMS"




