# iLens Kafka Publisher

```shell
pip install ilens-kafka-publisher
```

Sample Code:

```python

# pip install ilens-kafka-publisher
from ilens_kafka_publisher import KafkaPublisher

import app_configuration
from logger_file import logger


class DataPush:
    def __init__(self):
        self.obj = KafkaPublisher(
            kafka_host=app_configuration.kafka_host,
            kafka_port=app_configuration.kafka_port,
            kafka_topic=app_configuration.kafka_topic,
            redis_host=app_configuration.redis_host,
            redis_port=app_configuration.redis_port,
            redis_db=app_configuration.redis_db,
            enable_sites_partition=app_configuration.enable_sites_partition,
            split_key=app_configuration.split_key,
            round_robin_enable=app_configuration.round_robin_enable
        )

    def publish_message(self, message):
        try:
            self.obj.perform_task(message)
        except Exception as e:
            logger.debug(f"Failed to publish message - {e}")
            logger.debug(f"Trying reconnect")


if __name__ == '__main__':
    msg = {
        "data": {

            "site_107$dept_112$line_201$equipment_2885$tag_3351": 54
        },
        "site_id": "site_107",
        "gw_id": "",
        "pd_id": "",
        "timestamp": 1635227258000,
        "msg_id": 0,
        "retain_flag": False
    }
    obj = DataPush()
    obj.publish_message(msg)
```

### Authors: 
- [Charan Kumar Cheemanapalli](mailto:charankumar@knowledgelens.com)

Submit your feedbacks [here](https://gitlab-pm.knowledgelens.com/KnowledgeLens/Products/iLens-2.0/core/utilities/ilens-kafka-publisher/issues)
