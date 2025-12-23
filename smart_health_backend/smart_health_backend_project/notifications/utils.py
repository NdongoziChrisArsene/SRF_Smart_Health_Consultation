import logging
from .sms_service import send_sms
from .sendgrid_service import send_health_consultation_email

logger = logging.getLogger("notifications")

# --------------------------------------------
# SAFE SENDGRID DYNAMIC TEMPLATE EMAIL
# --------------------------------------------
def safe_sendgrid_email(to_email, template_id, dynamic_data):
    """
    Sends email using SendGrid Dynamic Template safely.
    """
    try:
        sent = send_health_consultation_email(
            to_email=to_email,
            dynamic_data=dynamic_data,
            template_id=template_id
        )
        if sent:
            logger.info(f"SendGrid email sent to {to_email} | Template ID: {template_id}")
        return sent
    except Exception as e:
        logger.error(f"SendGrid email failed to {to_email} | Template ID: {template_id}: {e}", exc_info=True)
        return False

# --------------------------------------------
# SAFE SMS SENDER
# --------------------------------------------
def safe_send_sms(phone_number, message):
    """
    Sends SMS using the validated phone number format from sms_service.py
    """
    try:
        sent = send_sms(phone_number=phone_number, message=message)
        if sent:
            logger.info(f"SMS sent to {phone_number}")
        return sent
    except Exception as e:
        logger.error(f"SMS sending failed to {phone_number}: {e}", exc_info=True)
        return False

# --------------------------------------------
# TEMPLATE IDs
# --------------------------------------------
TEMPLATE_ID_BOOKED = "d-6b56dc983e194751a2d6d4ec8f97a599"
TEMPLATE_ID_CANCELLED = "d-1234567890abcdef1234567890abcdef"  # replace with actual
TEMPLATE_ID_RESCHEDULED = "d-abcdef1234567890abcdef1234567890"  # replace with actual

# --------------------------------------------
# APPOINTMENT BOOKED NOTIFICATION
# --------------------------------------------
def notify_appointment_booked(patient, doctor, appointment):
    dynamic_data = {
        "patient_name": patient.user.get_full_name(),
        "doctor_name": doctor.user.get_full_name(),
        "date": str(appointment.date),
        "time": str(appointment.time)
    }

    sg_email_status = safe_sendgrid_email(
        to_email=patient.user.email,
        template_id=TEMPLATE_ID_BOOKED,
        dynamic_data=dynamic_data
    )

    sms_status = safe_send_sms(
        phone_number=patient.phone,
        message=f"Your appointment with Dr. {doctor.user.last_name} "
                f"is booked for {appointment.date} at {appointment.time}."
    )

    return {"sg_email_sent": sg_email_status, "sms_sent": sms_status}

# --------------------------------------------
# APPOINTMENT CANCELLED NOTIFICATION
# --------------------------------------------
def notify_appointment_cancelled(patient, appointment):
    dynamic_data = {
        "patient_name": patient.user.get_full_name(),
        "date": str(appointment.date),
        "time": str(appointment.time),
    }

    sg_email_status = safe_sendgrid_email(
        to_email=patient.user.email,
        template_id=TEMPLATE_ID_CANCELLED,
        dynamic_data=dynamic_data
    )

    sms_status = safe_send_sms(
        phone_number=patient.phone,
        message=f"Your appointment scheduled on {appointment.date} "
                f"at {appointment.time} has been cancelled."
    )

    return {"sg_email_sent": sg_email_status, "sms_sent": sms_status}

# --------------------------------------------
# APPOINTMENT RESCHEDULED NOTIFICATION
# --------------------------------------------
def notify_appointment_rescheduled(patient, doctor, old_appointment, new_appointment):
    dynamic_data = {
        "patient_name": patient.user.get_full_name(),
        "doctor_name": doctor.user.get_full_name(),
        "new_date": str(new_appointment.date),
        "new_time": str(new_appointment.time),
    }

    sg_email_status = safe_sendgrid_email(
        to_email=patient.user.email,
        template_id=TEMPLATE_ID_RESCHEDULED,
        dynamic_data=dynamic_data
    )

    sms_status = safe_send_sms(
        phone_number=patient.phone,
        message=f"Your appointment has been rescheduled to "
                f"{new_appointment.date} at {new_appointment.time}."
    )

    return {"sg_email_sent": sg_email_status, "sms_sent": sms_status}







































# import logging
# from .sms_service import send_sms
# from .sendgrid_service import send_health_consultation_email

# logger = logging.getLogger("notifications")

# # --------------------------------------------
# # SAFE SENDGRID DYNAMIC TEMPLATE EMAIL
# # --------------------------------------------
# def safe_sendgrid_email(to_email, template_id, dynamic_data):
#     """
#     Sends email using SendGrid Dynamic Template safely.
#     """
#     try:
#         sent = send_health_consultation_email(
#             to_email=to_email,
#             dynamic_data=dynamic_data,
#             template_id=template_id  # pass template ID dynamically
#         )
#         if sent:
#             logger.info(f"SendGrid email sent to {to_email} | Template ID: {template_id}")
#         return sent
#     except Exception as e:
#         logger.error(f"SendGrid email failed to {to_email} | Template ID: {template_id}: {e}", exc_info=True)
#         return False


# # --------------------------------------------
# # SAFE SMS SENDER
# # --------------------------------------------
# def safe_send_sms(phone_number, message):
#     try:
#         send_sms(phone_number=phone_number, message=message)
#         logger.info(f"SMS sent to {phone_number}")
#         return True
#     except Exception as e:
#         logger.error(f"SMS sending failed to {phone_number}: {e}")
#         return False


# # --------------------------------------------
# # APPOINTMENT BOOKED NOTIFICATION
# # --------------------------------------------
# TEMPLATE_ID_BOOKED = "d-6b56dc983e194751a2d6d4ec8f97a599"  # your booked template ID

# def notify_appointment_booked(patient, doctor, appointment):
#     dynamic_data = {
#         "patient_name": patient.user.get_full_name(),
#         "doctor_name": doctor.user.get_full_name(),
#         "date": str(appointment.date),
#         "time": str(appointment.time)
#     }

#     # Send SendGrid dynamic template email
#     sg_email_status = safe_sendgrid_email(
#         to_email=patient.user.email,
#         TEMPLATE_ID_BOOKED = "d-6b56dc983e194751a2d6d4ec8f97a599",
#         dynamic_data=dynamic_data
#     )

#     # Send SMS
#     sms_status = safe_send_sms(
#         phone_number=patient.phone,
#         message=f"Your appointment with Dr. {doctor.user.last_name} "
#                 f"is booked for {appointment.date} at {appointment.time}."
#     )

#     return {
#         "sg_email_sent": sg_email_status,
#         "sms_sent": sms_status
#     }


# # --------------------------------------------
# # APPOINTMENT CANCELLED NOTIFICATION
# # --------------------------------------------
# TEMPLATE_ID_CANCELLED = "d-your_cancelled_template_id"  # replace with your SendGrid template ID

# def notify_appointment_cancelled(patient, appointment):
#     dynamic_data = {
#         "patient_name": patient.user.get_full_name(),
#         "date": str(appointment.date),
#         "time": str(appointment.time),
#     }

#     # Send SendGrid dynamic template email
#     sg_email_status = safe_sendgrid_email(
#         to_email=patient.user.email,
#         TEMPLATE_ID_CANCELLED = "d-1234567890abcdef1234567890abcdef",
#         dynamic_data=dynamic_data
#     )

#     # Send SMS
#     sms_status = safe_send_sms(
#         phone_number=patient.phone,
#         message=f"Your appointment scheduled on {appointment.date} "
#                 f"at {appointment.time} has been cancelled."
#     )

#     return {
#         "sg_email_sent": sg_email_status,
#         "sms_sent": sms_status
#     }


# # --------------------------------------------
# # APPOINTMENT RESCHEDULED NOTIFICATION
# # --------------------------------------------
# TEMPLATE_ID_RESCHEDULED = "d-your_rescheduled_template_id"  # replace with your SendGrid template ID

# def notify_appointment_rescheduled(patient, doctor, old_appointment, new_appointment):
#     dynamic_data = {
#         "patient_name": patient.user.get_full_name(),
#         "doctor_name": doctor.user.get_full_name(),
#         "new_date": str(new_appointment.date),
#         "new_time": str(new_appointment.time),
#     }

#     # Send SendGrid dynamic template email
#     sg_email_status = safe_sendgrid_email(
#         to_email=patient.user.email,
#         TEMPLATE_ID_RESCHEDULED = "d-abcdef1234567890abcdef1234567890",
#         dynamic_data=dynamic_data
#     )

#     # Send SMS
#     sms_status = safe_send_sms(
#         phone_number=patient.phone,
#         message=f"Your appointment has been rescheduled to "
#                 f"{new_appointment.date} at {new_appointment.time}."
#     )

#     return {
#         "sg_email_sent": sg_email_status,
#         "sms_sent": sms_status
#     }



















































# import logging
# from .email_service import send_email
# from .sms_service import send_sms
# from .sendgrid_service import send_health_consultation_email as sg_send_email

# logger = logging.getLogger("notifications")


# # --------------------------------------------
# # SAFE HTML TEMPLATE EMAIL SENDER
# # --------------------------------------------
# def safe_send_email(subject, to_email, template_name, context):
#     """
#     Sends email using local HTML templates safely.
#     """
#     try:
#         send_email(
#             subject=subject,
#             to_email=to_email,
#             template_name=template_name,
#             context=context
#         )
#         logger.info(f"Email sent to {to_email} | Template: {template_name}")
#         return True

#     except Exception as e:
#         logger.error(f"Email sending failed to {to_email}: {e}")
#         return False


# # --------------------------------------------
# # SAFE SENDGRID DYNAMIC TEMPLATE EMAIL
# # --------------------------------------------
# def safe_send_consultation_email(to_email, dynamic_data):
#     """
#     Sends email using SendGrid Dynamic Template safely.
#     dynamic_data: dict with keys matching your dynamic template variables
#     """
#     try:
#         sent = sg_send_email(to_email=to_email, dynamic_data=dynamic_data)
#         if sent:
#             logger.info(f"SendGrid consultation email sent to {to_email}")
#         return sent
#     except Exception as e:
#         logger.error(f"SendGrid consultation email failed to {to_email}: {e}")
#         return False


# # --------------------------------------------
# # SAFE SMS SENDER
# # --------------------------------------------
# def safe_send_sms(phone_number, message):
#     """
#     Sends SMS safely via Twilio
#     """
#     try:
#         send_sms(phone_number=phone_number, message=message)
#         logger.info(f"SMS sent to {phone_number}")
#         return True

#     except Exception as e:
#         logger.error(f"SMS sending failed to {phone_number}: {e}")
#         return False


# # --------------------------------------------
# # APPOINTMENT BOOKED NOTIFICATION
# # --------------------------------------------
# def notify_appointment_booked(patient, doctor, appointment):
#     """
#     Sends appointment booked notifications:
#     - SendGrid dynamic template email
#     - Optional HTML template email (legacy)
#     - SMS
#     """

#     # -------------------------------
#     # Prepare dynamic template data
#     # -------------------------------
#     dynamic_data = {
#         "patient_name": patient.user.get_full_name(),
#         "doctor_name": doctor.user.get_full_name(),
#         "date": str(appointment.date),
#         "time": str(appointment.time)
#     }

#     # -------------------------------
#     # Send SendGrid dynamic template email
#     # -------------------------------
#     sg_email_status = safe_send_consultation_email(
#         to_email=patient.user.email,
#         dynamic_data=dynamic_data
#     )

#     # -------------------------------
#     # Optional: Legacy HTML template email (if still needed)
#     # -------------------------------
#     html_context = dynamic_data.copy()
#     email_status = safe_send_email(
#         subject="Appointment Confirmation",
#         to_email=patient.user.email,
#         template_name="appointment_confirmation.html",
#         context=html_context
#     )

#     # -------------------------------
#     # Send SMS notification
#     # -------------------------------
#     sms_status = safe_send_sms(
#         phone_number=patient.phone,
#         message=f"Your appointment with Dr. {doctor.user.last_name} "
#                 f"is booked for {appointment.date} at {appointment.time}."
#     )

#     # -------------------------------
#     # Return all statuses
#     # -------------------------------
#     return {
#         "sg_email_sent": sg_email_status,
#         "email_sent": email_status,
#         "sms_sent": sms_status
#     }


# # --------------------------------------------
# # APPOINTMENT CANCELLED NOTIFICATION
# # --------------------------------------------
# def notify_appointment_cancelled(patient, appointment):
#     context = {
#         "patient_name": patient.user.get_full_name(),
#         "date": appointment.date,
#         "time": appointment.time,
#     }

#     email_status = safe_send_email(
#         subject="Appointment Cancelled",
#         to_email=patient.user.email,
#         template_name="appointment_cancelled.html",
#         context=context
#     )

#     sms_status = safe_send_sms(
#         phone_number=patient.phone,
#         message=f"Your appointment scheduled on {appointment.date} "
#                 f"at {appointment.time} has been cancelled."
#     )

#     return {
#         "email_sent": email_status,
#         "sms_sent": sms_status
#     }


# # --------------------------------------------
# # APPOINTMENT RESCHEDULED NOTIFICATION
# # --------------------------------------------
# def notify_appointment_rescheduled(patient, doctor, old_appointment, new_appointment):
#     context = {
#         "patient_name": patient.user.get_full_name(),
#         "doctor_name": doctor.user.get_full_name(),
#         "new_date": new_appointment.date,
#         "new_time": new_appointment.time,
#     }

#     email_status = safe_send_email(
#         subject="Appointment Rescheduled",
#         to_email=patient.user.email,
#         template_name="appointment_rescheduled.html",
#         context=context
#     )

#     sms_status = safe_send_sms(
#         phone_number=patient.phone,
#         message=f"Your appointment has been rescheduled to "
#                 f"{new_appointment.date} at {new_appointment.time}."
#     )

#     return {
#         "email_sent": email_status,
#         "sms_sent": sms_status
#     }




















































# import logging
# from .email_service import send_email
# from .sms_service import send_sms
# from .sendgrid_service import send_health_consultation_email as sg_send_email

# logger = logging.getLogger("notifications")


# # --------------------------------------------
# # SAFE EMAIL SENDER
# # --------------------------------------------
# def safe_send_email(subject, to_email, template_name, context):
#     try:
#         send_email(
#             subject=subject,
#             to_email=to_email,
#             template_name=template_name,
#             context=context
#         )
#         logger.info(f"Email sent to {to_email} | Template: {template_name}")
#         return True

#     except Exception as e:
#         logger.error(f"Email sending failed to {to_email}: {e}")
#         return False


# # --------------------------------------------
# # SAFE SMS SENDER
# # --------------------------------------------
# def safe_send_sms(phone_number, message):
#     try:
#         send_sms(phone_number=phone_number, message=message)
#         logger.info(f"SMS sent to {phone_number}")
#         return True

#     except Exception as e:
#         logger.error(f"SMS sending failed to {phone_number}: {e}")
#         return False


# # --------------------------------------------
# # APPOINTMENT BOOKED NOTIFICATION
# # --------------------------------------------
# def notify_appointment_booked(patient, doctor, appointment):
#     context = {
#         "patient_name": patient.user.get_full_name(),
#         "doctor_name": doctor.user.get_full_name(),
#         "date": appointment.date,
#         "time": appointment.time,
#     }

#     email_status = safe_send_email(
#         subject="Appointment Confirmation",
#         to_email=patient.user.email,
#         template_name="appointment_confirmation.html",
#         context=context
#     )

#     sms_status = safe_send_sms(
#         phone_number=patient.phone,
#         message=f"Your appointment with Dr. {doctor.user.last_name} "
#                 f"is booked for {appointment.date} at {appointment.time}."
#     )

#     return {
#         "email_sent": email_status,
#         "sms_sent": sms_status
#     }


# # --------------------------------------------
# # APPOINTMENT CANCELLED NOTIFICATION
# # --------------------------------------------
# def notify_appointment_cancelled(patient, appointment):
#     context = {
#         "patient_name": patient.user.get_full_name(),
#         "date": appointment.date,
#         "time": appointment.time,
#     }

#     email_status = safe_send_email(
#         subject="Appointment Cancelled",
#         to_email=patient.user.email,
#         template_name="appointment_cancelled.html",
#         context=context
#     )

#     sms_status = safe_send_sms(
#         phone_number=patient.phone,
#         message=f"Your appointment scheduled on {appointment.date} "
#                 f"at {appointment.time} has been cancelled."
#     )

#     return {
#         "email_sent": email_status,
#         "sms_sent": sms_status
#     }


# # --------------------------------------------
# # APPOINTMENT RESCHEDULED NOTIFICATION
# # --------------------------------------------
# def notify_appointment_rescheduled(patient, doctor, old_appointment, new_appointment):
#     context = {
#         "patient_name": patient.user.get_full_name(),
#         "doctor_name": doctor.user.get_full_name(),
#         "new_date": new_appointment.date,
#         "new_time": new_appointment.time,
#     }

#     email_status = safe_send_email(
#         subject="Appointment Rescheduled",
#         to_email=patient.user.email,
#         template_name="appointment_rescheduled.html",
#         context=context
#     )

#     sms_status = safe_send_sms(
#         phone_number=patient.phone,
#         message=f"Your appointment has been rescheduled to "
#                 f"{new_appointment.date} at {new_appointment.time}."
#     )

#     return {
#         "email_sent": email_status,
#         "sms_sent": sms_status
#     }







































# import logging
# from .email_service import send_email
# from .sms_service import send_sms

# logger = logging.getLogger("notifications")


# # --------------------------------------------
# # SAFE EMAIL SENDER
# # --------------------------------------------
# def safe_send_email(subject, to_email, template_name, context):
#     try:
#         send_email(
#             subject=subject,
#             to_email=to_email,
#             template_name=template_name,
#             context=context
#         )
#         logger.info(f"Email sent to {to_email} | Template: {template_name}")
#         return True

#     except Exception as e:
#         logger.error(f"Email sending failed to {to_email}: {e}")
#         return False


# # --------------------------------------------
# # SAFE SMS SENDER
# # --------------------------------------------
# def safe_send_sms(phone_number, message):
#     try:
#         send_sms(phone_number=phone_number, message=message)
#         logger.info(f"SMS sent to {phone_number}")
#         return True

#     except Exception as e:
#         logger.error(f"SMS sending failed to {phone_number}: {e}")
#         return False


# # --------------------------------------------
# # APPOINTMENT BOOKED NOTIFICATION
# # --------------------------------------------
# def notify_appointment_booked(patient, doctor, appointment):
#     context = {
#         "patient_name": patient.user.get_full_name(),
#         "doctor_name": doctor.user.get_full_name(),
#         "date": appointment.date,
#         "time": appointment.time,
#     }

#     email_status = safe_send_email(
#         subject="Appointment Confirmation",
#         to_email=patient.user.email,
#         template_name="appointment_confirmation.html",
#         context=context
#     )

#     sms_status = safe_send_sms(
#         phone_number=patient.phone,
#         message=f"Your appointment with Dr. {doctor.user.last_name} "
#                 f"is booked for {appointment.date} at {appointment.time}."
#     )

#     return {
#         "email_sent": email_status,
#         "sms_sent": sms_status
#     }


# # --------------------------------------------
# # APPOINTMENT CANCELLED NOTIFICATION
# # --------------------------------------------
# def notify_appointment_cancelled(patient, appointment):
#     context = {
#         "patient_name": patient.user.get_full_name(),
#         "date": appointment.date,
#         "time": appointment.time,
#     }

#     email_status = safe_send_email(
#         subject="Appointment Cancelled",
#         to_email=patient.user.email,
#         template_name="appointment_cancelled.html",
#         context=context
#     )

#     sms_status = safe_send_sms(
#         phone_number=patient.phone,
#         message=f"Your appointment scheduled on {appointment.date} "
#                 f"at {appointment.time} has been cancelled."
#     )

#     return {
#         "email_sent": email_status,
#         "sms_sent": sms_status
#     }


# def notify_appointment_rescheduled(patient, doctor, old_appointment, new_appointment):
#     context = {
#         "patient_name": patient.user.get_full_name(),
#         "doctor_name": doctor.user.get_full_name(),
#         "new_date": new_appointment.date,
#         "new_time": new_appointment.time,
#     }

#     send_email(
#         subject="Appointment Rescheduled",
#         to_email=patient.user.email,
#         template_name="appointment_rescheduled.html",
#         context=context
#     )

#     send_sms(
#         phone_number=patient.phone,
#         message=f"Your appointment has been rescheduled to {new_appointment.date} at {new_appointment.time}."
#     )






































# from .email_service import send_email
# from .sms_service import send_sms

# def notify_appointment_booked(patient, doctor, appointment):
#     context = {
#         "patient_name": patient.user.get_full_name(),
#         "doctor_name": doctor.user.get_full_name(),
#         "date": appointment.date,
#         "time": appointment.time,
#     }

#     # Email
#     send_email(
#         subject="Appointment Confirmation",
#         to_email=patient.user.email,
#         template_name="appointment_confirmation.html",
#         context=context
#     )

#     # SMS
#     send_sms(
#         phone_number=patient.phone,
#         message=f"Your appointment with Dr. {doctor.user.last_name} is booked for {appointment.date} at {appointment.time}."
#     )


# def notify_appointment_cancelled(patient, appointment):
#     context = {
#         "patient_name": patient.user.get_full_name(),
#         "date": appointment.date,
#         "time": appointment.time,
#     }

#     send_email(
#         subject="Appointment Cancelled",
#         to_email=patient.user.email,
#         template_name="appointment_cancelled.html",
#         context=context
#     )

#     send_sms(
#         phone_number=patient.phone,
#         message=f"Your appointment scheduled on {appointment.date} at {appointment.time} has been cancelled."
#     )
