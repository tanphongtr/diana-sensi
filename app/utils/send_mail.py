from django.core.mail import send_mail


class SendMail():

    title = None
    content = None

    def __init__(self, subject, message, from_email, recipient_list, html_message=None):

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )