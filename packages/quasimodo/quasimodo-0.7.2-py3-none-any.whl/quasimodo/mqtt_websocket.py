#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import uuid
import json
import time

from paho.mqtt.client import Client

import quasimodo.base


class QueueWorkerSkeletonTT(quasimodo.base.Q):
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 15675
    DEFAULT_USERNAME = "guest"
    DEFAULT_PASSWORD = "guest"
    DEFAULT_HEARTBEAT_INTERVAL = 60
    DEFAULT_ENDPOINT = "/ws"
    DEFAULT_BINDING_KEYS = ["*", "*.*"]

    def __init__(self, *args, **kwargs):
        quasimodo.base.Q.__init__(self, *args, **kwargs)
        self.log = logging.getLogger(__name__)

        self.endpoint = kwargs.get("endpoint", getattr(self, "DEFAULT_ENDPOINT"))
        self.heartbeat_interval = kwargs.get("heartbeat_interval", 60)
        agent_id = str(uuid.uuid4())

        self.exchange_binding_keys = kwargs.get("binding_keys")

        self.connected = False
        if self.transport is None:
            self.transport = "websockets"
        self.client = Client(client_id=agent_id, transport=self.transport)
        self.client.ws_set_options(self.endpoint)
        self.client.on_connect = self.__on_connect
        self.client.on_message = self.callback
        self.client.on_subscribe = self.__on_subscribe

        if self.tls_context:
            self.log.warning("Not setting credentials")
        else:
            self.client.username_pw_set(self.credentials[0], self.credentials[1])

        self.client.enable_logger()

        if self.tls_context:
            self.client.tls_set_context(self.tls_context)

        if self.autorun:
            self.run()

    def __on_connect(self, client, userdata, flags, rc):
        self.log.debug("on connect ... (rc={!r})".format(rc))
        self.connected = rc == 0

        if self.connected:
            if not self.exchange_binding_keys:
                self.exchange_binding_keys = self.DEFAULT_BINDING_KEYS
                self.log.warning(
                    "Using default binding keys {!r}".format(self.exchange_binding_keys)
                )

            for binding_key in self.exchange_binding_keys:
                client.subscribe(binding_key)

    def callback(self, client, userdata, message):
        try:
            payload = json.loads(message.payload)
        except Exception as exc:
            print(repr(message.payload))
            return

        self.handle_request(payload, client=client, userdata=userdata, message=message)

    def __on_subscribe(self, client, userdata, mid, granted_qos):
        self.log.debug("on subscribe ...")
        # print(client)
        # print(userdata)
        # print(mid)
        # print(granted_qos)

    def run(self):
        self.client.connect(self.host, self.port, keepalive=self.heartbeat_interval)
        self.client.loop_start()

        self._start_consuming()

    def _start_consuming(self):
        net_loc = "{username!s}:{password!s}@{host}:{port}".format(
            username=self.client._username,
            password=self.client._password,
            host=self.host,
            port=self.port,
        )

        exchange_binding_keys = self.exchange_binding_keys
        if exchange_binding_keys is None:
            exchange_binding_keys = self.DEFAULT_BINDING_KEYS

        path_indicator = ""
        if self.transport == "websockets":
            path_indicator = f"{self.client._websocket_path} "
        listening_to = "{path_indicator}({binding_keys})".format(
            path_indicator=path_indicator,
            binding_keys="; ".join(sorted(exchange_binding_keys)),
        )

        self.log.info(
            "The monkeys are listening to {:s} {:s}".format(net_loc, listening_to)
        )

        while True:
            time.sleep(0.5)

    def simple_publish(self, payload, routing_key="", **kwargs):
        sp_client_id = "spc-" + str(uuid.uuid4())
        sp_client = Client(client_id=sp_client_id, transport=self.transport)
        sp_client.ws_set_options(self.endpoint)

        if self.tls_context:
            sp_client.tls_set_context(self.tls_context)
        else:
            sp_client.username_pw_set(self.credentials[0], self.credentials[1])
        sp_client.connect(self.host, self.port, keepalive=self.heartbeat_interval)

        sp_client.loop_start()

        res = sp_client.publish(routing_key, payload=json.dumps(payload))
        res.wait_for_publish()

        sp_client.loop_stop()
        self.log.debug("rc={!r}".format(res.rc))
        return res.rc == 0

    def _handle_request(self, payload, **kwargs):
        raise NotImplementedError
