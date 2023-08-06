from ... import Server


class KafkaTopic:
    def __init__(self,
                 server: Server,
                 topic_id: str
                 ):
        self.server = server
        self.topic_id = topic_id


class ProducerConfig:
    def __init__(self, **kwargs):
        """
        :kwargs args for https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html
        """
        self.producer_kwargs = kwargs
