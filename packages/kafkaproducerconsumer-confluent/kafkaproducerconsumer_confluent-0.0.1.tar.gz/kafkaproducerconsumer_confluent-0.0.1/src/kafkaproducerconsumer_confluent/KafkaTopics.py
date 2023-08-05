from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer
from confluent_kafka import Producer, Consumer, KafkaError
import ccloud_lib
import json 

class KafkaProducerConsumer():
    # Messages will be serialized as JSON 
    def json_serializer(self, messages):
        return json.dumps(messages).encode('utf-8')

    def acked(self, err, msg):       
        global delivered_records
        if err is not None:
            print("Failed to deliver message: {}".format(err))
        else:
            delivered_records += 1
            print("Produced record to topic {} partition [{}] @ offset {}"
                  .format(msg.topic(), msg.partition(), msg.offset()))

    def kafka_json_producer(self, topic_name,  message_type, key = None, messages_list = None,**conf):
        producer_conf = ccloud_lib.pop_schema_registry_params_from_config(conf)
        producer = Producer(producer_conf)
        ccloud_lib.create_topic(conf, topic_name)
        for messages in messages_list:
            producer.produce(topic = topic_name, key = key, value = self.json_serializer(messages), on_delivery=self.acked)
            producer.poll(0)
        producer.flush()


    def kafka_json_consumer(self, topic_name, auto_offset_reset, consumer_group,  **conf):
        consumer_conf = ccloud_lib.pop_schema_registry_params_from_config(conf)
        consumer_conf['group.id'] = consumer_group
        consumer_conf['auto.offset.reset'] = auto_offset_reset
        consumer = Consumer(consumer_conf)

        consumer.subscribe([topic_name])
        try:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                elif msg.error():
                    print('error: {}'.format(msg.error()))
                else:
                    record_key = msg.key()
                    record_value = json.loads(msg.value())
                    yield(record_value)

        except KeyboardInterrupt:
            pass
        finally:
            # Leave group and commit final offsets
            consumer.close()

    def kafka_avro_consumer(self, topic_name, auto_offset_reset,consumer_group, **conf):  

        schema_registry_conf = {
            'url': conf['schema.registry.url'],
            'basic.auth.user.info': conf['basic.auth.user.info']}
        schema_registry_client = SchemaRegistryClient(schema_registry_conf)

        name_avro_deserializer = AvroDeserializer(schema_registry_client = schema_registry_client,
                                                schema_str = ccloud_lib.name_schema,
                                                from_dict = ccloud_lib.Name.dict_to_name)
        count_avro_deserializer = AvroDeserializer(schema_registry_client = schema_registry_client,
                                                schema_str = ccloud_lib.count_schema,
                                                from_dict = ccloud_lib.Count.dict_to_count)

        consumer_conf = ccloud_lib.pop_schema_registry_params_from_config(conf)
        consumer_conf['key.deserializer'] = name_avro_deserializer
        consumer_conf['value.deserializer'] = count_avro_deserializer
        consumer_conf['group.id'] = consumer_group
        consumer_conf['auto.offset.reset'] = auto_offset_reset
        consumer = DeserializingConsumer(consumer_conf)

        consumer.subscribe([topic_name])

    # Process messages
        total_count = 0
        while True:
            try:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                elif msg.error():
                    print('error: {}'.format(msg.error()))
                else:
                    name_object = msg.key()
                    count_object = msg.value()
                    count = count_object.count
                    total_count += count
                    print("Consumed record with key {} and value {}, \
                        and updated total count to {}"
                        .format(name_object.name, count, total_count))
            except KeyboardInterrupt:
                break
            except SerializerError as e:
                # Report malformed record, discard results, continue polling
                print("Message deserialization failed {}".format(e))
                pass
        consumer.close()


    
