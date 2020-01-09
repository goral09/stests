import os

from dramatiq.brokers.rabbitmq import RabbitmqBroker

from stests.core.mq.brokers.rabbitmq import connection
from stests.core.utils.execution import ExecutionContext



def get_broker(ctx: ExecutionContext) -> RabbitmqBroker:
    """Returns instance of rabbit mq broker.

    :param network_id: Network identifier, e.g. LOC-DEV-01
    :returns: An instance of a Rabbit MQ broker.

    """
    # Set RabbitMQ virtual host.
    vhost = ctx.network_id.upper()

    # Set RabbitMQ connection url.
    url = connection.get_url(vhost)

    return RabbitmqBroker(url=url)
