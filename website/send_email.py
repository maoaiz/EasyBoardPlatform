#encoding:utf-8
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.conf import settings
from django.utils.translation import ugettext as _
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.header import Header


def sendEmail(email_type, ctx, to=None):
    """to should be a list.
        SEND EMAIL TYPES:
            #ACTIVATE_ACCOUNT: Activate account
            #SEND_CREDENTIALS: send credentials of new school"""
    if not to:
        to = [settings.ADMIN_EMAIL]
    if email_type == "#ACTIVATE_ACCOUNT":
        subject = ctx['username'] + " " + _("Bienvenido!")
        plaintext = get_template('email_welcome.txt')
        url_key = settings.PRINCIPAL_DOMAIN  # change this to the original url
        variables = {
            "project_name": settings.PROJECT_NAME,
            "activate_url": url_key,
            "full_name": ctx['username']
        }
        html_content = render_to_string('email/email_activate_account.html', variables)
    elif email_type == "#SEND_CREDENTIALS":
        subject = _(u"Datos para iniciar sesión en tu nuevo colegio") + " " + unicode(settings.PROJECT_NAME, 'utf-8')
        variables = {
            "project_name": settings.PROJECT_NAME,
            "full_name": ctx['username'],
            "school_url": ctx['school_url'],
            "username": ctx['username'],
            "password": ctx['password'],
            "manual_url": settings.PRINCIPAL_DOMAIN + "#manual",
        }
        plaintext = get_template('email/email_welcome.txt')
        html_content = render_to_string('email/email_send_credentials.html', variables)
    else:
        plaintext = get_template('email/email_welcome.txt')
        html_content = render_to_string('email/email_welcome.txt')
        subject, to = 'Mensaje de prueba', ['no-reply@daiech.com']
    from_email = settings.EMAIL_HOST_USER
    d = Context(ctx)
    text_content = plaintext.render(d)
    html_content = html_content

    try:
        smtp = settings.EMAIL_HOST_PASSWORD and settings.EMAIL_HOST_USER
    except NameError:
        smtp = None
    if smtp:
        return sendGmailEmail(to, subject, html_content)
    else:
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
            print "EMAIL enviado!"
            return "EMAIL enviado!"
        except Exception, e:
            print e
            print "Error al enviar correo electronico tipo: ", email_type, " con plantilla HTML."
            return "Correo NO enviado"


def sendGmailEmail(to, subject, text, attach=False):
    gmail_user = settings.EMAIL_HOST_USER
    gmail_pwd = settings.EMAIL_HOST_PASSWORD
    msg = MIMEMultipart()

    msg['From'] = gmail_user
    msg['To'] = ",".join(to)
    # msg['Subject'] = subject
    msg['Subject'] = "%s" % Header(subject, 'utf-8')

    # msg.attach(MIMEText(text, "html"))
    msg.attach(MIMEText(text, "html", 'utf-8'))

    if attach:
        from email import Encoders
        from email.MIMEBase import MIMEBase
        import os
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attach, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition',
               'attachment; filename="%s"' % os.path.basename(attach))
        msg.attach(part)

    mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()
    return "Email sent"