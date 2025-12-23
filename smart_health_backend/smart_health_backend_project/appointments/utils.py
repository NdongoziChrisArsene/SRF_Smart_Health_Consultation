import logging
import asyncio

logger = logging.getLogger(__name__)


async def async_notify(message):
    await asyncio.sleep(0.1)
    logger.info(message)


def notify_appointment_booked(patient, doctor, appointment):
    try:
        msg = (
            f"[BOOKED] Patient={patient.user.username}, "
            f"Doctor={doctor.user.username}, "
            f"Date={appointment.date}, Time={appointment.time}"
        )
        asyncio.run(async_notify(msg))
        return True
    except Exception as e:
        logger.error(f"Notify booked failed: {e}")
        return False


def notify_appointment_cancelled(patient, appointment):
    try:
        msg = (
            f"[CANCELLED] Patient={patient.user.username}, "
            f"Date={appointment.date}, Time={appointment.time}"
        )
        asyncio.run(async_notify(msg))
        return True
    except Exception as e:
        logger.error(f"Notify cancelled failed: {e}")
        return False































# import logging
# import asyncio

# logger = logging.getLogger(__name__)

# async def async_notify(message):
#     # Simulate async notification, e.g., email/SMS
#     await asyncio.sleep(0.1)
#     logger.info(message)
#     return True

# def notify_appointment_booked(patient, doctor, appointment):
#     try:
#         msg = f"[Notification] Appointment booked: Patient={patient.user.username}, " \
#               f"Doctor={doctor.user.username}, Date={appointment.date}, Time={appointment.time}"
#         asyncio.run(async_notify(msg))
#         return True
#     except Exception as e:
#         logger.error(f"Failed to notify appointment booked: {e}")
#         return False

# def notify_appointment_cancelled(patient, appointment):
#     try:
#         msg = f"[Notification] Appointment cancelled: Patient={patient.user.username}, " \
#               f"Date={appointment.date}, Time={appointment.time}"
#         asyncio.run(async_notify(msg))
#         return True
#     except Exception as e:
#         logger.error(f"Failed to notify appointment cancelled: {e}")
#         return False








































# import logging

# logger = logging.getLogger(__name__)


# def notify_appointment_booked(patient, doctor, appointment):
#     """
#     Sends notification when appointment is booked.
#     """
#     try:
#         # Example: log only. Replace with email/SMS if needed.
#         logger.info(
#             f"[Notification] Appointment booked: Patient={patient.user.username}, "
#             f"Doctor={doctor.user.username}, Date={appointment.date}, Time={appointment.time}"
#         )
#         return True
#     except Exception as e:
#         logger.error(f"Failed to notify appointment booked: {e}")
#         return False


# def notify_appointment_cancelled(patient, appointment):
#     """
#     Sends notification when appointment is cancelled.
#     """
#     try:
#         logger.info(
#             f"[Notification] Appointment cancelled: Patient={patient.user.username}, "
#             f"Date={appointment.date}, Time={appointment.time}"
#         )
#         return True
#     except Exception as e:
#         logger.error(f"Failed to notify appointment cancelled: {e}")
#         return False
























