import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string, TemplateDoesNotExist
from django.conf import settings

logger = logging.getLogger("email")

def send_email(subject, to_email, template_name, context=None):
    """
    Safe & production-ready email sender:
    - Validates email
    - Handles missing template
    - Logs success & failures
    - Uses correct FROM_EMAIL setting
    """

    if not to_email:
        logger.error("send_email() called without a recipient.")
        return False

    context = context or {}

    # Render HTML template
    try:
        html_content = render_to_string(template_name, context)
    except TemplateDoesNotExist:
        logger.error(f"Email template not found: {template_name}")
        return False

    text_content = "Your email client does not support HTML content."

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", settings.EMAIL_HOST_USER)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=[to_email],
    )
    email.attach_alternative(html_content, "text/html")

    try:
        email.send()
        logger.info(f"Email sent successfully to: {to_email}")
        return True
    except Exception as e:
        logger.error(f"Email sending failed to {to_email}: {e}", exc_info=True)
        return False




































# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.conf import settings

# def send_email(subject, to_email, template_name, context):
#     """
#     Sends HTML email using Django's email backend.
#     """
#     html_content = render_to_string(template_name, context)
#     text_content = "This email requires an HTML-compatible email client."

#     email = EmailMultiAlternatives(
#         subject=subject,
#         body=text_content,
#         from_email=settings.EMAIL_HOST_USER,
#         to=[to_email]
#     )

#     email.attach_alternative(html_content, "text/html")
#     email.send()
