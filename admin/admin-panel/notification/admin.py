from django.contrib import admin

from django import forms
from django.http import HttpRequest, HttpResponseRedirect
from django.http.response import HttpResponse
from .models import Notification

from .tasks import notification_created


class NotificationCreateForm(forms.ModelForm):
    class Meta:
        """Create a form to send notifications."""

        model = Notification
        fields = ['first_name', 'last_name', 'email', 'message']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    def add_view(self, request: HttpRequest, form_url: str = '', extra_context: None = ...) -> HttpResponse:
        if request.method == 'POST':
            form = NotificationCreateForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                notification = Notification.objects.create(
                    first_name=cd['first_name'],
                    last_name=cd['last_name'],
                    email=cd['email'],
                    message=cd['message'],
                    send=True
                )
                notification_created.delay(notification.id)
                return HttpResponseRedirect('../{notification}/'.format(notification=notification.pk))
        else:
            form = NotificationCreateForm()

        context = self.get_changeform_initial_data(request)
        context['form'] = form

        return super().add_view(request, form_url, extra_context=context)
