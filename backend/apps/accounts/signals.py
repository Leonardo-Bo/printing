from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.core.mail import mail_admins, send_mail
from django.contrib.auth.signals import user_logged_in
from django.conf import settings

from apps.accounts.models import User
from apps.crossuser.models import UserId


url_login = settings.DOMAIN + '/login'
url_admin = settings.DOMAIN + '/admin'
url_home = settings.TEAM


@receiver(post_save, sender=User)#, dispatch_uid='register')
def register(sender, instance, **kwargs):
    if kwargs.get('created', False) and not instance.is_active:
        mail_admins('User registration request', 
        f"A subscription request has been made by the user:\n\n{ instance.username }\n{ instance.email }\n\nTo manage the subscription go to { url_admin }",
        fail_silently=False, )


@receiver(pre_save, sender=User)#, dispatch_uid='active')
def active(sender, instance, **kwargs):
    if instance.is_active and User.objects.filter(pk=instance.pk, is_active=False).exists():
        subject = 'Account Activation'
        mesagge = f"{ instance.username } Your account has been activated successfully!\n\nTo log in go to the page:\n\n{ url_login }\n\nTeam { url_home }"
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, mesagge, from_email, [instance.email], fail_silently=False)


@receiver(pre_delete, sender=User, dispatch_uid='delete')
def delete_account(sender, instance, **kwargs):
        subject = 'Account deleted'
        mesagge = f"{ instance.username }, your account has been deleted successfully.\n\nThank you for using our service!\n\nTeam { url_home }"
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, mesagge, from_email, [instance.email], fail_silently=False)


def update_userid(sender, user, **kwargs):
    UserId.objects.get_or_create(id_user=user.id)

user_logged_in.connect(update_userid)