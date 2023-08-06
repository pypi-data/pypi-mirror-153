#!/usr/bin/env python
# -*- coding: utf-8 -*-
from quasimodo.amqp import QueueWorkerSkeleton
from quasimodo.mqtt_websocket import QueueWorkerSkeletonTT


class Monkey(QueueWorkerSkeleton):
    def _handle_request(self, payload, **kwargs):
        success = True
        delivery_method = kwargs.get("method")
        content_type = 'unknown'

        try:
            content_type = kwargs.get("properties").content_type
        except Exception:
            pass

        if delivery_method:
            try:
                self.log.info(
                    "{exchange}/{routing_key} [{content_type}]".format(
                        exchange=delivery_method.exchange,
                        routing_key=delivery_method.routing_key,
                        content_type=content_type
                    ))
            except Exception:
                pass

        self.log_data_dump(payload)

        return {
            "success": success
        }


class Ape(QueueWorkerSkeletonTT):
    def _handle_request(self, payload, **kwargs):
        success = True

        if kwargs.get("message"):
            message_obj = kwargs.get("message")
            try:
                self.log.info("{routing_key}".format(
                    routing_key=message_obj.topic))
            except Exception:
                pass

        self.log_data_dump(payload)

        return {
            "success": success
        }
