# from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db.models.signals import post_migrate, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import User

from enum import Enum #ToDo Каждый раз писать value бред


class AdStatus:
    DRAFT = 'draft'
    ACTIVE = 'active'
    CLOSED = 'closed'


class ResponseAdStatus:
    CONFIRMED = 'confirmed'
    REJECTED = 'rejected'
    CONSIDERATION = 'consideration'


class Post(models.Model):

    title = models.CharField(max_length=255, blank=True, null=True)
    description = CKEditor5Field('Text', config_name='extends')
    slug = models.SlugField(default='', blank='')

    def save(self):
        self.slug = slugify(self.title)
        super(Post, self).save()

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ad(models.Model):
    STATUS_CHOICES = (
        (AdStatus.DRAFT, 'Draft'),
        (AdStatus.ACTIVE, 'Active'),
        (AdStatus.CLOSED, 'Closed'),
    )

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ads')
    body = CKEditor5Field('Text', config_name='extends')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AdStatus.DRAFT)

    def check_status(self):
        return self.status == AdStatus.ACTIVE

    def get_status_display(self):
        return dict(self.STATUS_CHOICES)[self.status]

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title


class ResponseAd(models.Model):
    STATUS_CHOICES = (
        (ResponseAdStatus.CONFIRMED, 'Confirmed'),
        (ResponseAdStatus.REJECTED, 'Rejected'),
        (ResponseAdStatus.CONSIDERATION, 'Consideration'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='responses')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ResponseAdStatus.CONSIDERATION)

    def get_status_display(self):
        return dict(self.STATUS_CHOICES)[self.status]

    def check_status(self):
        return self.status == ResponseAdStatus.CONSIDERATION

    def confirmed(self):
        if self.check_status:
            self.status = ResponseAdStatus.CONFIRMED
            self.save()
    def rejected(self):
        if self.check_status:
            self.status = ResponseAdStatus.REJECTED
            self.save()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.author.username}\'s response to {self.ad.title}'


@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name == 'board':
        Category.objects.get_or_create(name='Танки')
        Category.objects.get_or_create(name='Хилы')
        Category.objects.get_or_create(name='ДД')
        Category.objects.get_or_create(name='Торговцы')
        Category.objects.get_or_create(name='Гилдмастеры')
        Category.objects.get_or_create(name='Квестгиверы')
        Category.objects.get_or_create(name='Кузнецы')
        Category.objects.get_or_create(name='Кожевники ')
        Category.objects.get_or_create(name='Зельевары ')
        Category.objects.get_or_create(name='Мастера заклинаний')


@receiver(pre_save, sender=Ad)
def add_slug_to_post(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        slug = slugify(f"{instance.id}-{instance.title}")
        instance.slug = slug







