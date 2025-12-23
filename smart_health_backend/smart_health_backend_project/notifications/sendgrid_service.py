import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger("email")

# Read SendGrid API key explicitly (from .env)
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")


def send_health_consultation_email(to_email, dynamic_data, template_id):
    """
    Sends an email using SendGrid Dynamic Template.

    Args:
        to_email (str): Recipient email
        dynamic_data (dict): Data for dynamic_template_data
        template_id (str): SendGrid dynamic template ID to use
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    if not to_email:
        logger.error("No recipient provided for SendGrid email.")
        return False

    if not template_id:
        logger.error("No template ID provided for SendGrid email.")
        return False

    if not SENDGRID_API_KEY:
        logger.error("SENDGRID_API_KEY is not set.")
        return False

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email
    )

    message.template_id = template_id
    message.dynamic_template_data = dynamic_data

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        logger.info(f"SendGrid email sent to {to_email} | Template ID: {template_id}")
        return True
    except Exception as e:
        logger.error(f"SendGrid email failed to {to_email} | Template ID: {template_id}: {e}", exc_info=True)
        return False











































# import os
# import logging
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

# logger = logging.getLogger("email")

# # Read environment variables
# SENDGRID_API_KEY = os.getenv("EMAIL_HOST_PASSWORD")
# FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")


# def send_health_consultation_email(to_email, dynamic_data, template_id):
#     """
#     Sends an email using SendGrid Dynamic Template.

#     Args:
#         to_email (str): Recipient email
#         dynamic_data (dict): Data for dynamic_template_data
#         template_id (str): SendGrid dynamic template ID to use
#     Returns:
#         bool: True if email sent successfully, False otherwise
#     """
#     if not to_email:
#         logger.error("No recipient provided for SendGrid email.")
#         return False

#     if not template_id:
#         logger.error("No template ID provided for SendGrid email.")
#         return False

#     message = Mail(
#         from_email=FROM_EMAIL,
#         to_emails=to_email
#     )

#     message.template_id = template_id
#     message.dynamic_template_data = dynamic_data

#     try:
#         sg = SendGridAPIClient(SENDGRID_API_KEY)
#         sg.send(message)
#         logger.info(f"SendGrid email sent to {to_email} | Template ID: {template_id}")
#         return True
#     except Exception as e:
#         logger.error(f"SendGrid email failed to {to_email} | Template ID: {template_id}: {e}", exc_info=True)
#         return False

















































# import os
# import logging
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

# logger = logging.getLogger("email")

# SENDGRID_API_KEY = os.getenv("EMAIL_HOST_PASSWORD")
# FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
# TEMPLATE_ID_CONSULTATION = "d-6b56dc983e194751a2d6d4ec8f97a599"  # your dynamic template ID

# def send_health_consultation_email(to_email, dynamic_data):
#     """
#     Sends an email using SendGrid Dynamic Template.

#     Args:
#         to_email (str): Recipient email
#         dynamic_data (dict): Data for dynamic_template_data
#     Returns:
#         bool: True if email sent, False otherwise
#     """
#     if not to_email:
#         logger.error("No recipient provided for SendGrid email.")
#         return False

#     message = Mail(
#         from_email=FROM_EMAIL,
#         to_emails=to_email
#     )
#     message.template_id = TEMPLATE_ID_CONSULTATION
#     message.dynamic_template_data = dynamic_data

#     try:
#         sg = SendGridAPIClient(SENDGRID_API_KEY)
#         sg.send(message)
#         logger.info(f"SendGrid email sent to {to_email}")
#         return True
#     except Exception as e:
#         logger.error(f"SendGrid email failed to {to_email}: {e}", exc_info=True)
#         return False
