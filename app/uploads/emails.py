from django.conf import settings

from comicsite.utils.email import send_templated_email


def send_file_uploaded_notification_email(**kwargs):
    uploader = kwargs['uploader']
    comicsite = kwargs['comicsite']
    site = kwargs['site']
    title = "New upload for %s: '%s' " % (
        comicsite.short_name, kwargs["filename"])
    admins = comicsite.get_admins()

    if not admins:
        admin_email_adresses = [x[1] for x in settings.ADMINS]
        kwargs['additional_message'] = '<i> Message from COMIC: I could not\
        find any administrator for ' + comicsite.short_name + '. Somebody needs to\
        know about this new upload, so I am Sending this email to everyone set\
        as general COMIC admin (ADMINS in the /comic/settings/ conf file). To\
        stop getting these messages, set an admin for\
        ' + comicsite.short_name + '.</i> <br/><br/>'
    else:
        kwargs['additional_message'] = ''
        admin_email_adresses = [x.email for x in admins]

    kwargs['project'] = comicsite
    send_templated_email(
        title,
        "uploads/emails/file_uploaded_email.html",
        kwargs,
        admin_email_adresses,
    )
