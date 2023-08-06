
from django.core.exceptions import ValidationError
from wagtail.admin.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

class EmailActionHandler:

    def __init__(self, **kwargs):
        self.context = kwargs

    def handle(self, value):
        form = self.context['form']
        form_name = form.name
        subject = _(f'Odpověď na formulář "{form_name}"')
        sender_field_name = value['sender']
        validated_data = self.context['validated_data']
        sender = validated_data.get(sender_field_name, None)
        if sender is None and self.context['request'].user.is_authenticated:
            sender = self.context['request'].user.email
        context= {
            'user': self.context['request'].user,
            'data': validated_data,
            'context': {}
        }
        msg_html = render_to_string('send_email_action.html', context)
        send_mail(subject=subject,
                  message=str(validated_data),
                  from_email=sender,
                  recipient_list=[value['address']],
                  html_message=msg_html)
