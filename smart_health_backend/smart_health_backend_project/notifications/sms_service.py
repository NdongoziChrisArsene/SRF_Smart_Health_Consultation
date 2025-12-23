import logging
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import re

logger = logging.getLogger("sms")

def send_sms(phone_number: str, message: str) -> bool:
    """
    Safe, production-ready SMS sending function using Twilio.
    Returns True if sent successfully, False otherwise.

    Enforces international phone format for Rwanda (+250).
    Logs warnings if the phone number is invalid.
    """
    # Normalize phone number: remove spaces, dashes, parentheses
    phone_number = re.sub(r"[ \-\(\)]", "", phone_number)

    # Check for Rwanda international format
    if not phone_number.startswith("+250"):
        logger.warning(f"Invalid phone number format (must start with +250): {phone_number}")
        return False

    # Check that the rest of the number has 9 digits
    if not re.fullmatch(r"\+250\d{9}", phone_number):
        logger.warning(f"Invalid phone number length or characters: {phone_number}")
        return False

    try:
        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

        message_instance = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )

        logger.info(f"SMS sent to {phone_number}, SID: {message_instance.sid}")
        return True

    except TwilioRestException as e:
        logger.error(
            f"Twilio API error when sending SMS to {phone_number}: {str(e)}",
            exc_info=True
        )
        return False

    except Exception as e:
        logger.error(
            f"Unexpected error when sending SMS to {phone_number}: {str(e)}",
            exc_info=True
        )
        return False



















































# import logging
# from django.conf import settings
# from twilio.rest import Client
# from twilio.base.exceptions import TwilioRestException

# logger = logging.getLogger("sms")


# def send_sms(phone_number: str, message: str) -> bool:
#     """
#     Safe, production-ready SMS sending function using Twilio.
#     Returns True if sent successfully, False otherwise.
#     """
#     # Normalize phone number: remove spaces, dashes
#     phone_number = phone_number.replace(" ", "").replace("-", "")
    
#     # Basic validation (avoid API call if number is invalid)
#     if not phone_number or not phone_number.startswith("+"):
#         logger.warning(f"Invalid phone number format: {phone_number}")
#         return False

#     try:
#         client = Client(
#             settings.TWILIO_ACCOUNT_SID,
#             settings.TWILIO_AUTH_TOKEN
#         )

#         message_instance = client.messages.create(
#             body=message,
#             from_=settings.TWILIO_PHONE_NUMBER,
#             to=phone_number
#         )

#         logger.info(f"SMS sent to {phone_number}, SID: {message_instance.sid}")
#         return True

#     except TwilioRestException as e:
#         logger.error(
#             f"Twilio API error when sending SMS to {phone_number}: {str(e)}",
#             exc_info=True
#         )
#         return False

#     except Exception as e:
#         logger.error(
#             f"Unexpected error when sending SMS to {phone_number}: {str(e)}",
#             exc_info=True
#         )
#         return False





























# from django.conf import settings
# from twilio.rest import Client

# def send_sms(phone_number, message):
#     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

#     client.messages.create(
#         body=message,
#         from_=settings.TWILIO_PHONE_NUMBER,
#         to=phone_number
#     )
