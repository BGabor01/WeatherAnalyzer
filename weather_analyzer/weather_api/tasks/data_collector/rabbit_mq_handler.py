import os
import logging
import uuid
import socket
from typing import Optional, Dict, Tuple, Any

import pika
import json


logger = logging.getLogger(__name__)


class RabbitMqHandler:
    def __init__(self, queue_name: str) -> None:
        self.credentials = (
            pika.PlainCredentials(
                os.environ.get("RABBITMQ_USER"),
                os.environ.get("RABBITMQ_PASSWORD"),
            ),
        )

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters("rabbitmq", credentials=self.credentials[0])
        )

        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def publish(
        self,
        task_name: str,
        exchange: str,
        routing_key: str,
        args: Optional[Tuple[Any, ...]] = (),
        kwargs: Optional[Dict[Any, Any]] = {},
        retries: Optional[int] = 2,
    ) -> None:
        task_id, root_id, parent_id, group_id = self.create_ids()

        message = {
            "args": args,
            "kwargs": kwargs,
            "embed": {"callbacks": [], "errbacks": [], "chain": [], "chord": None},
        }

        headers = {
            "lang": "py",
            "task": task_name,
            "id": str(task_id),
            "root_id": str(root_id),
            "parent_id": str(parent_id),
            "group": str(group_id),
            "argsrepr": repr(args),
            "kwargsrepr": repr(kwargs),
            "origin": "@".join([str(os.getpid()), socket.gethostname()]),
            "retries": retries,
        }

        properties = {
            "correlation_id": str(task_id),
            "content_type": "application/json",
            "content_encoding": "utf-8",
        }

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2, headers=headers, **properties
            ),
        )

        logger.info(
            f"Message published to {self.queue_name} queue with task: {task_name}!"
        )

    def close(self) -> None:
        if self.connection.is_open:
            logger.info("Closing connection!")
            self.connection.close()

    @staticmethod
    def create_ids() -> Tuple[uuid.UUID, uuid.UUID, uuid.UUID, uuid.UUID]:
        return tuple(uuid.uuid4() for _ in range(4))
