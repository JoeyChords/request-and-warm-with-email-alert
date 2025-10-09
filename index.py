import datetime, logging, time, requests
from dotenv import load_dotenv
import os
import resend

load_dotenv()

resend.api_key = os.environ["RESEND_API_KEY"]
COLD_URL = os.environ["COLD_URL"]
EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = os.environ["EMAIL_TO"]
logging.basicConfig(filename="warmer.log", level=logging.INFO)
timeStarted = datetime.datetime.now()
logging.info(
    timeStarted.strftime("%m/%d/%Y, %H:%M:%S")
    + "   requestAndWarm started on "
    + COLD_URL
)
alertMessageMailed = False

print("Keeping " + COLD_URL + " warm")

while True:
    timeOfRequest = datetime.datetime.now()
    try:
        r = requests.get(COLD_URL)
        if r.status_code == 200:
            logging.info(
                timeOfRequest.strftime("%m/%d/%Y, %H:%M:%S")
                + "   "
                + COLD_URL
                + " returned status code "
                + str(r.status_code)
            )
            # Send an email alert when the website is online.

            if alertMessageMailed:
                params = {
                    "from": EMAIL_FROM,
                    "to": [EMAIL_TO],
                    "subject": COLD_URL + " is Online",
                    "html": "<strong>"
                    + COLD_URL
                    + " is online.</strong><br><br><strong>Status code = "
                    + str(r.status_code)
                    + "</strong>"
                    }
                try:
                    response = resend.Emails.send(params)
                    logging.info(
                        "  Alert message sent with Resend. Site back online."
                    )
                    logging.info("  Resend.com email: " + str(response))
                    alertMessageMailed = False
                except Exception as e:
                    logging.info(e.message)
        else:
            raise Exception()
    except:
        logging.exception(
            timeOfRequest.strftime("%m/%d/%Y, %H:%M:%S")
            + "   Status code "
            + str(r.status_code)
        )
        # Send an email alert when something is wrong with the website.
        if not alertMessageMailed:
            params = {
                    "from": EMAIL_FROM,
                    "to": [EMAIL_TO],
                    "subject": "Problem with " + COLD_URL,
                    "html": "<strong>Something is wrong with "
                    + COLD_URL
                    + "</strong><br><br><strong>Status code = "
                    + str(r.status_code)
                    + "</strong>",
                }
            try:               
                response = resend.Emails.send(params)
                logging.info("  Alert message sent with Resend. Site Error.")
                logging.info("  Resend.com email: " + str(response))
                alertMessageMailed = True
            except Exception as e:
                logging.info(e.message)
    time.sleep(840)