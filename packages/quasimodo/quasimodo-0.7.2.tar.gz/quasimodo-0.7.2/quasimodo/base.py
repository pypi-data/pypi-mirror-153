#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import logging
import traceback
import json
import pprint
import ssl

import quasimodo


class Q(object):
    def __init__(self, *args, **kwargs):
        self.tls_context = None
        self._credentials = (False, False)
        self.log = logging.getLogger(__name__)
        self.host = kwargs.get("host", getattr(self, "DEFAULT_HOST"))
        self.port = int(kwargs.get("port", getattr(self, "DEFAULT_PORT")))
        self.transport = kwargs.get("transport")
        username = kwargs.get("username", getattr(self, "DEFAULT_USERNAME"))
        password = kwargs.get("password", getattr(self, "DEFAULT_PASSWORD"))
        self.heartbeat_interval = kwargs.get(
            "heartbeat_interval", getattr(self, "DEFAULT_HEARTBEAT_INTERVAL", 60)
        )
        self.set_credentials(username, password)
        self.verbose = kwargs.get("verbose", 0)
        self.dry_run = kwargs.get("dry_run", False)
        self.autorun = kwargs.get("autorun", False)
        self.identifier = kwargs.get(
            "identifier",
            "Q-{:s}/{!s}".format(self.__class__.__name__, quasimodo.__version__),
        )
        if kwargs.get("tls_context"):
            self.tls_context = kwargs.get("tls_context")
        elif kwargs.get("tls"):
            self.tls_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            cafile, keyfile, certfile = (
                kwargs.get("cafile"),
                kwargs.get("keyfile"),
                kwargs.get("certfile"),
            )
            if None in (cafile, keyfile, certfile):
                self.log.info(f"No certificates based TLS ..")
            else:
                if kwargs.get("alpn_amz"):
                    self.tls_context.set_alpn_protocols(["x-amzn-mqtt-ca"])
                self.tls_context.load_verify_locations(cafile=cafile)
                self.tls_context.load_cert_chain(certfile=certfile, keyfile=keyfile)

    def __str__(self):
        portions = [
            "<{klass}-{version} ".format(
                klass=self.__class__.__name__, version=quasimodo.__version__
            )
        ]

        try:
            portions.append(self._credentials.username + "@")
        except Exception:
            try:
                portions.append(self._credentials[0] + "@")
            except Exception:
                pass

        portions.append("{host}:{port}".format(host=self.host, port=self.port))
        portions.append(">")
        return "".join(portions)

    @property
    def credentials(self):
        return self._credentials

    def set_credentials(self, username, password):
        self._credentials = (username, password)

    def log_traceback(self, message, exception, uselog=None):
        """
        Use *uselog* Logger to log a Traceback of exception *exception*.
        """
        if uselog is None:
            uselog = self.log
        e_type, e_value, e_traceback = sys.exc_info()

        uselog.warning(message)
        uselog.error(exception)
        tb_lines = traceback.format_exception(e_type, e_value, e_traceback)

        for line in tb_lines:
            for part in line.strip().split("\n"):
                if part != "":
                    uselog.warning(part)

    def log_data_dump(self, data):
        try:
            encoded = json.dumps(data, indent=2, sort_keys=True)
            for line in encoded.split("\n"):
                self.log.info(line)
        except Exception as exc:
            self.log.warning(exc)
            self.log.info(pprint.pformat(data))

    def handle_request(self, payload, **kwargs):
        """
        Handle a message/request obtained from queue.
        """
        self.log.debug("payload={:s}".format(pprint.pformat(payload)))
        retval = self._handle_request(payload, **kwargs)

        return retval

    def _handle_request(self, payload, **kwargs):
        """
        Message/request handling function.
        To be implemented by deriving classes.
        """
        raise NotImplementedError

    def _start_consuming(self):
        raise NotImplementedError

    def callback(self, *args, **kwargs):
        raise NotImplementedError

    def run(self, *args, **kwargs):
        raise NotImplementedError

    def simple_publish(self, payload, routing_key="", **kwargs):
        raise NotImplementedError
