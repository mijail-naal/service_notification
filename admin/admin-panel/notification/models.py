from django.db import models


class Notification(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField()
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    send = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'Message sent to {self.first_name} {self.last_name}'


class Template(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=50)
    content = models.TextField(help_text='HTML or text.')

    class Meta:
        verbose_name = 'Template'
        verbose_name_plural = 'Templates'

    def __str__(self):
        return f'Template - {self.title}'
