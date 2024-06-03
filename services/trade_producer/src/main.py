from quixstreams import Application
from typing import List, Dict

from src.kraken_api import KrakenWebsocketTradeAPI


def produce_trades(
    kaka_broker_address: str,
    kaka_topic_name: str,
) -> None:
    """
    Reads trades from the Kraken websocket API and saves them into a Kafka topic.

    Args:
        kaka_broker_address (str): The address of the Kafka broker.
        kaka_topic_name (str): The name of the Kafka topic.

    Returns:
        None
    """
    app = Application(broker_address=kaka_broker_address)

    # the topic where we will save the trades
    topic = app.topic(name=kaka_topic_name, value_serializer='json')

    # Create an instance of the Kraken API
    kraken_api = KrakenWebsocketTradeAPI(product_id='BTC/USD')

    print('Creating the producer...')

    # Create a Producer instance
    with app.get_producer() as producer:

        while True:

            # Get the trades from the Kraken API
            trades : List[Dict] = kraken_api.get_trades()
            print('Got trades from Kraken')
            
            for trade in trades:

                # Serialize an event using the defined Topic 
                message = topic.serialize(key=trade["product_id"],
                                          value=trade)

                # Produce a message into the Kafka topic
                producer.produce(
                    topic=topic.name,
                    value=message.value,
                    key=message.key
                )

                print('Message sent!')

            from time import sleep
            sleep(1)

if __name__ == '__main__':

    produce_trades(
        kaka_broker_address="redpanda-0:9092",
        kaka_topic_name="trade"
    )