import time

from kafka import KafkaConsumer as KC, KafkaProducer as KP

from ._data_types import *
from ... import EventSink, Event, TriggerableEventBatchSource, TriggererEventSource
from ..._private._utilities import *


class KafkaTriggererConsumer(TriggererEventSource):
    def __init__(self,
                 topic: KafkaTopic,
                 group_id: str,
                 deserializer: Callable[[str], Any],
                 offset_reset_strategy: str = 'latest',
                 **kwargs):
        super().__init__(**kwargs)
        self.topic = topic
        self.group_id = group_id
        self.deserializer = deserializer
        self.offset_reset_strategy = offset_reset_strategy
        self.consuming: bool = False

        self.inner_consumer: KC = KC(
            self.topic.topic_id,
            bootstrap_servers=[str(self.topic.server)],
            auto_offset_reset=self.offset_reset_strategy,
            enable_auto_commit=True,
            group_id=self.group_id,
            value_deserializer=lambda x: self.deserializer(x.decode('utf-8'))
        )

    def start_generating(self) -> None:
        self.consuming = True
        threading.Thread(target=self._repetitively_generate).start()

    def _repetitively_generate(self):
        for message in self.inner_consumer:
            try:
                event = message.value
                if not isinstance(event, Event):
                    print(f'Invalid kafka message with type {str(type(event))}')  # TODO log
                else:
                    self.process_generated_event(event)
            except:
                pass  # TODO log
            finally:
                if not self.consuming:
                    break

    def stop_generating(self) -> None:
        self.consuming = False


class KafkaConsumer(TriggerableEventBatchSource):
    def __init__(self,
                 topic: KafkaTopic,
                 group_id: str,
                 deserializer: Callable[[str], Any],
                 offset_reset_strategy: str = 'latest',
                 max_records: int = None,
                 timeout_ms: int = 0,
                 empty_check_timeout_ms: int = 5000,
                 **kwargs):
        super().__init__(**kwargs)
        self.topic = topic
        self.group_id = group_id
        self.deserializer = deserializer
        self.offset_reset_strategy = offset_reset_strategy
        self.max_records = max_records
        self.timeout_ms = timeout_ms
        self.empty_check_timeout_s = empty_check_timeout_ms / 1000
        self.last_empty_epoch: float = 0
        self.inner_consumer: KC = KC(
            self.topic.topic_id,
            bootstrap_servers=[str(self.topic.server)],
            auto_offset_reset=self.offset_reset_strategy,
            enable_auto_commit=True,
            group_id=self.group_id,
            value_deserializer=lambda x: self.deserializer(x.decode('utf-8'))
        )

    def get_event_batch(self) -> List[Event]:
        if time.time() < self.last_empty_epoch + self.empty_check_timeout_s:
            return []
        records: Dict = \
            self.inner_consumer.poll(timeout_ms=self.timeout_ms, max_records=self.max_records) \
                if self.max_records is not None \
                else self.inner_consumer.poll(timeout_ms=self.timeout_ms)
        record_list: List[Event] = []
        for tp, consumer_records in records.items():
            for consumer_record in consumer_records:
                event = consumer_record.value
                if not isinstance(event, Event):
                    print(f'Invalid kafka message with type {str(type(event))}')  # TODO log
                else:
                    record_list.append(event)
        if len(record_list) == 0:
            self.last_empty_epoch = time.time()
        return record_list


class KafkaProducer(EventSink):
    def __init__(self,
                 topic: KafkaTopic,
                 serializer: Callable[[Any], str],
                 producer_config: ProducerConfig,
                 **kwargs):
        super().__init__(**kwargs)
        self.topic = topic
        self.serializer = serializer

        producer_config = producer_config if producer_config is not None else ProducerConfig()
        self.inner_producer: KP = KP(bootstrap_servers=[str(self.topic.server)],
                                     value_serializer=lambda x: self.serializer(x).encode('utf-8'),
                                     **producer_config.producer_kwargs)

    def drown_event(self, event: Event) -> None:
        self.inner_producer.send(self.topic.topic_id, value=event)
