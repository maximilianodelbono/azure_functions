import datetime
import logging

import azure.functions as func

from dbpostgres import get_alerts,takecareofAlert


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    
    alerts=get_alerts()
    for alert in alerts:
        print("======================================")
        print("Sending signal about alert to next function")
        print(alert[3])
        print("======================================")
        print(takecareofAlert(alert[3]))
    
    logging.info('Alerts have been taken care of at (UTC) %s', utc_timestamp)
