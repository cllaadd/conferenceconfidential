from datetime import datetime
import json
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendees_bc.settings")
django.setup()


from attendees.models import AccountVO


def update_account(ch, method, properties, body):
    content = json.loads(body)
    first_name = content["first_name"]
    last_name = content["last_name"]
    email = content["email"]
    is_active = content["is_active"]
    updated_string = content["updated"]
    updated = datetime.fromisoformat(updated_string)
    if is_active:
        account = AccountVO.objects.update_or_create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=is_active,
            updated=updated,
        )
        account.save()
    #   Use the update_or_create method of the AccountVO.objects QuerySet
    #       to update or create the AccountVO object
    else:
        account = AccountVO.objects.get(email=email).delete()
        account.delete()


# Based on the reference code at
#   https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/python/receive_logs.py
while True:
    try:
        parameters = pika.ConnectionParameters(host="rabbitmq")
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.exchange_declare(
            exchange="account_info", exchange_type="fanout"
        )
        result = channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(queue=queue_name, exchange="account_info")
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=update_account,
            auto_ack=True,
        )
        print(" [*] Waiting for Responses. To exit press CTRL+C")
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except AMQPConnectionError:
        print("Could not connect to rabbitmq")
        time.sleep(1)


#   try
#       create the pika connection parameters
#       create a blocking connection with the parameters
#       open a channel
#       declare a fanout exchange named "account_info"
#       declare a randomly-named queue
#       get the queue name of the randomly-named queue
#       bind the queue to the "account_info" exchange
#       do a basic_consume for the queue name that calls
#           function above
#       tell the channel to start consuming
#   except AMQPConnectionError
#       print that it could not connect to RabbitMQ
#       have it sleep for a couple of seconds
