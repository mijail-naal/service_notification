import pika

from deliver.tasks import send_notification
from core.config import rabbit_settings as rs


class RabbitConsumer:
    def __init__(self) -> None:
        self.credentials = pika.PlainCredentials(rs.user, rs.password)
        self.parameters = pika.ConnectionParameters(
            credentials=self.credentials,
            host=rs.host,
            port=rs.port
        )
        self.connection = pika.SelectConnection(
            parameters=self.parameters,
            on_open_callback=self.on_connected,
            on_close_callback=self.on_close
        )
        self.chanel = None

    def on_connected(self, connection):
        """Called when connected to RabbitMQ."""
        connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, new_channel):
        """Called when the channel has opened."""
        self.channel = new_channel
        self.channel.queue_declare(
            queue=rs.queue,
            durable=True,
            exclusive=False,
            auto_delete=False,
            callback=self.on_queue_declared
        )

    def on_queue_declared(self, frame):
        """Called when the Queue has been declared."""
        self.channel.basic_consume(rs.queue, self.handle_delivery)

    def handle_delivery(self, channel, method, header, body):
        """Called when we receive a message from RabbitMQ."""
        print(body)
        send_notification.delay(body)

    def on_close(self, connection, exception):
        # Invoked when the connection is closed
        connection.ioloop.stop()


if __name__ == '__main__':
    from deliver.tasks import send_notification

    consumer = RabbitConsumer()

    try:
        consumer.connection.ioloop.start()

    except KeyboardInterrupt:
        consumer.connection.close()
        consumer.connection.ioloop.start()
