#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import uuid
import json
import pprint
import copy

import pika

import quasimodo
import quasimodo.base

MIMETYPE_JSON = 'application/json'

#: fallback queue
DEFAULT_QUEUE = "quasimodo"


class Quasimodo(quasimodo.base.Q):
    #: default rabbitMQ parameters
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 5671
    DEFAULT_USERNAME = 'guest'
    DEFAULT_PASSWORD = 'guest'
    DEFAULT_HEARTBEAT_INTERVAL = 1800
    DEFAULT_BINDING_KEYS = ['*']

    def __init__(self, *args, **kwargs):
        quasimodo.base.Q.__init__(self, *args, **kwargs)
        self.log = logging.getLogger(__name__)
        self.ssl_options = None
        if self.tls_context:
            self.ssl_options = pika.SSLOptions(self.tls_context, self.host)

    def set_credentials(self, username, password):
        self._credentials = pika.PlainCredentials(
            username=username, password=password)

    def add_to_queue(self, payload, queue=DEFAULT_QUEUE,
                     content_type=MIMETYPE_JSON, arguments=None,
                     correlation_id=None, reply_to=None, durable=False):
        """
        Request adding of *payload* to the queue named *queue*.
        """
        transaction_id = uuid.uuid4().hex

        payload['transaction_id'] = transaction_id
        payload['queue'] = queue

        if content_type == MIMETYPE_JSON:
            payload = json.dumps(payload)

        self.log.debug("Payload (q={!r}):".format(queue))
        self.log.debug(pprint.pformat(payload))

        connection_parameters = pika.ConnectionParameters(
            host=self.host, port=self.port, credentials=self.credentials,
            ssl_options=self.ssl_options,
        )
        connection = pika.BlockingConnection(connection_parameters)
        channel = connection.channel()

        properties = pika.BasicProperties(
            # make message persistent
            delivery_mode=2,
            content_type=content_type,
            correlation_id=correlation_id,
            reply_to=reply_to
        )

        if arguments:
            channel.queue_declare(queue=queue, durable=True,
                                  arguments=arguments)
        elif durable:
            channel.queue_declare(queue=queue, durable=True)
        else:
            channel.queue_declare(queue=queue, passive=True)

        channel.basic_publish(
            exchange='', routing_key=queue, body=payload,
            properties=properties)

        connection.close()

        return transaction_id

    def add_to_exchange(self, payload, routing_key='', exchange='amq.topic',
                        content_type=MIMETYPE_JSON, exchange_type='direct',
                        arguments=None):
        """
        Request adding of *payload* to the exchange named *exchange*.
        """
        transaction_id = uuid.uuid4().hex

        payload['transaction_id'] = transaction_id
        payload['exchange'] = exchange
        if content_type == MIMETYPE_JSON:
            payload = json.dumps(payload)

        self.log.debug("Payload (x={!r}):".format(exchange))
        self.log.debug(pprint.pformat(payload))

        connection_parameters = pika.ConnectionParameters(
            host=self.host, port=self.port, credentials=self.credentials,
            ssl_options=self.ssl_options,
        )
        connection = pika.BlockingConnection(connection_parameters)
        channel = connection.channel()

        properties = pika.BasicProperties(
            # make message persistent
            delivery_mode=2,
            content_type=content_type,
        )

        if arguments:
            channel.exchange_declare(exchange=exchange, durable=True,
                                     arguments=arguments,
                                     exchange_type=exchange_type)
        else:
            channel.exchange_declare(exchange=exchange, passive=True,
                                     exchange_type=exchange_type)

        channel.basic_publish(
            exchange=exchange, routing_key=routing_key, body=payload,
            properties=properties)

        connection.close()

        return transaction_id

    @property
    def qcc(self):
        return self

    def simple_publish(self, payload, routing_key='', **kwargs):
        return self.add_to_exchange(payload, routing_key=routing_key, **kwargs)


class QueueWorkerSkeleton(Quasimodo):
    """
    Skeleton implementation of a queue worker application.
    """

    def __init__(self, *args, **kwargs):
        Quasimodo.__init__(self, *args, **kwargs)
        self.log = logging.getLogger(kwargs.get("log_name", __name__))
        self.queue_name = kwargs.get("queue", False)
        self.exchange_name = kwargs.get("exchange", False)
        self.exchange_type = kwargs.get("exchange_type", 'topic')
        self.exchange_binding_keys = kwargs.get("binding_keys")
        self.requeue_default = kwargs.get("requeue_default", False)
        self.max_consumed_messages = kwargs.get("max_consumed_messages", -1)
        self.deadletter_support = kwargs.get("deadletter_support", False)
        self.queue_declare_arguments = kwargs.get("queue_declare_arguments")
        self.consumed_count = 0
        self.channel = None
        self.connection = None

        if self.autorun:
            self.run()

    def set_environment_variables(self, fallback_values=None, dump=False):
        """
        .. deprecated:: 0.0.0

        Args:
            fallback_values:
            dump:

        Returns:

        """
        if fallback_values is None:
            fallback_values = {
                'LANG': "C.UTF-8",
                'PYTHONIOENCODING': 'UTF-8',
            }

        for key in fallback_values:
            if key not in os.environ.keys():
                self.log.debug(
                    "Setting LANG={value}".format(value=fallback_values[key]))
                os.environ[key] = fallback_values[key]

        if dump:
            self.log.info("Environment:")
            for key in sorted(os.environ.keys()):
                self.log.info('{key:40s}: {value!r}'.format(
                    key=key, value=os.environ[key]))

    def run(self):
        """
        Set up queue and start consuming.
        """
        connection_parameters = pika.ConnectionParameters(
            host=self.host, port=self.port, credentials=self.credentials,
            heartbeat=self.heartbeat_interval,
            connection_attempts=10,
            ssl_options=self.ssl_options,
        )
        self.connection = pika.BlockingConnection(connection_parameters)
        self.channel = self.connection.channel()

        if self.exchange_name is not False:
            if not self.exchange_binding_keys:
                self.exchange_binding_keys = self.DEFAULT_BINDING_KEYS
                self.log.warning("Using default binding keys {!r}".format(
                    self.exchange_binding_keys))

            self.channel.exchange_declare(
                exchange=self.exchange_name, exchange_type=self.exchange_type,
                arguments=self.queue_declare_arguments, durable=True)
            result = self.channel.queue_declare('', exclusive=True)
            self.queue_name = result.method.queue

            for binding_key in self.exchange_binding_keys:
                self.channel.queue_bind(
                    exchange=self.exchange_name, queue=self.queue_name,
                    routing_key=binding_key)

            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(
                on_message_callback=self.callback, queue=self.queue_name)
        else:
            if self.deadletter_support:
                self._setup_deadletter_exchange()
            else:
                self.channel.queue_declare(
                    queue=self.queue_name, durable=True,
                    arguments=self.queue_declare_arguments)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            on_message_callback=self.callback, queue=self.queue_name)

        self._start_consuming()

    def _setup_deadletter_exchange(self):
        """
        Add dead letter exchange handling if enabled.
        """
        if not self.deadletter_support:
            self.log.debug("No dead letter support")
            return

        exchange_name = '{:s}-dlx'.format(self.queue_name)
        deadletter_name = '{:s}-deadletter'.format(self.queue_name)

        self.log.info("Setting up exchange {:s}".format(exchange_name))
        self.channel.exchange_declare(exchange=exchange_name, 
                                      exchange_type='direct',
                                      durable=True)

        self.log.debug("Setting up deadletter queue {:s}".format(
            deadletter_name))
        self.channel.queue_declare(queue=deadletter_name, durable=True)

        arguments = {
            # 'x-message-ttl': 1000,
            "x-dead-letter-exchange": exchange_name,
            # if not specified, queue's routing-key is used
            "x-dead-letter-routing-key": self.queue_name,
        }
        self.channel.queue_declare(queue=self.queue_name, durable=True,
                                   arguments=arguments)

    def _start_consuming(self):
        """
        Start consuming function.
        May be implemented by deriving classes.
        """
        net_loc = "{username!s}:{password!s}@{host}:{port}".format(
            username=self._credentials.username,
            password=self._credentials.password,
            host=self.host, port=self.port
        )
        listening_to = '{queue}'.format(queue=self.queue_name)
        if self.exchange_name is not False:
            listening_to += ' ({:s})'.format(
                '; '.join(sorted(self.exchange_binding_keys)))
        self.log.info("The monkeys are listening to {:s} {:s}".format(
            net_loc, listening_to))

        self.channel.start_consuming()

    def callback(self, channel, method, properties, body):
        """
        Message queue callback.
        """
        may_run = True
        success = None
        requeue = self.requeue_default
        self.consumed_count += 1
        response_payload = dict()
        payload = dict()
        handle_request_result = dict()

        if properties.content_type == MIMETYPE_JSON:
            body = json.loads(body)

        if properties.content_type is None:
            try:
                body = json.loads(body)
                properties.content_type = MIMETYPE_JSON
            except Exception:
                pass

        if self.verbose:
            self.log.info("Received    S{:s}".format(pprint.pformat(body)))
            self.log.info(" properties {:s}".format(pprint.pformat(properties)))
            self.log.info(" channel    {:s}".format(pprint.pformat(channel)))
            self.log.info(" method     {:s}".format(pprint.pformat(method)))

        if not may_run:
            self.log.warning("Denied by may_run value")
            requeue = False
        else:
            payload = copy.copy(body)
            try:
                del payload['transaction_id']
            except Exception:
                pass

            try:
                self.log.debug("now handling request")
                handle_request_result = self.handle_request(
                    payload=payload,
                    channel=channel, method=method, properties=properties)
            except Exception as exception:
                self.log_traceback("execution (QueueWorkerSkeleton.callback)",
                                   exception)

        try:
            success = handle_request_result.get("success")
            response_payload = handle_request_result
        except AttributeError:
            success = handle_request_result
            response_payload['success'] = handle_request_result
        except NameError as nexc:
            self.log_traceback("UH-OH! execution (QueueWorkerSkeleton)", nexc)
            success = False
            requeue = False

        response_payload['__request_payload'] = payload

        self._confirm_callback(channel, method, properties,
                               response_payload)

        if success:
            self.log.debug("Success.")
            channel.basic_ack(delivery_tag=method.delivery_tag)
        else:
            self.log.warning(
                "{!s}: Failure, Abort. requeue={!r}".format(self.identifier,
                                                            requeue))
            self.log.info("payload:")
            self.log.info("-" * 40)
            self.log_data_dump(body)
            self.log.info("~" * 40)

            if not self.deadletter_support:
                channel.basic_nack(delivery_tag=method.delivery_tag,
                                   requeue=requeue)
            else:
                delivery_tag = method.delivery_tag
                requeue = False
                self.log.info(
                    "basic_reject: delivery_tag={delivery_tag} requeue={requeue}".format(
                        delivery_tag=delivery_tag, requeue=requeue))
                channel.basic_reject(delivery_tag=delivery_tag,
                                     requeue=requeue)

        if self.max_consumed_messages != -1:
            if self.consumed_count >= self.max_consumed_messages:
                try:
                    current_identifier = ' ({:s})'.format(self.identifier)
                except Exception:
                    current_identifier = ''
                self.log.info("Stop consuming{:s}".format(current_identifier))
                channel.stop_consuming()

    def _confirm_callback(self, channel, method, properties, payload):
        """
        Callback for emitting confirmations.
        """
        self.log.debug("CONFIRM CALLBACK:")
        try:
            if not properties.reply_to:
                self.log.debug("reply_to is None")
                return None

            mfg = "[{reply_to}] corr'n_id={correlation_id}: {payload}".format(
                reply_to=properties.reply_to,
                correlation_id=properties.correlation_id,
                payload=pprint.pformat(payload))
            self.log.info(mfg)

            pika_properties = pika.BasicProperties(
                correlation_id=properties.correlation_id,
                content_type=MIMETYPE_JSON)

            try:
                payload_json = json.dumps(payload)
            except TypeError as texception:
                payload_dummy = {
                    '_exception': True,
                    '_payload': pprint.pformat(payload)
                }
                self.log_traceback("JSON conversion failed", texception)
                payload_json = json.dumps(payload_dummy)

            channel.basic_publish(exchange='',
                                  routing_key=properties.reply_to,
                                  properties=pika_properties,
                                  body=payload_json)
            return True
        except Exception as exception:
            self.log_traceback("confirm callback", exception)

        self.log.warn("FAIL!")
        return False
