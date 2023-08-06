#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse
import logging
import json
import socket

from quasimodo.stubs import Ape, Monkey

OPT_NO_VALUE = "<use implementation's default>"


class DumpMixin(object):
    def _handle_request(self, payload, **kwargs):
        success = True

        self.log_data_dump(payload)

        return {"success": success}


class ApeDumper(Ape, DumpMixin):
    pass


class MonkeyDumper(Monkey, DumpMixin):
    pass


def dump_hunchback_parameters(kwargs, connection_option_keys, use_log=None):
    if use_log is None:
        use_log = logging.getLogger(__name__)
    use_log.info("Parameters")
    use_log.info("=" * 80)
    all_option_keys = set(kwargs.keys())
    all_option_keys |= set([x[0] for x in connection_option_keys])
    base_class = None

    if kwargs.get("flavour") == "amqp":
        base_class = Monkey
    elif kwargs.get("flavour") == "mqtt":
        base_class = Ape

    for key in sorted(all_option_keys):
        implementation_attribute = "DEFAULT_{:s}".format(key).upper()

        try:
            fallback_val = getattr(base_class, implementation_attribute)
        except AttributeError:
            fallback_val = None

        val = kwargs.get(key, fallback_val)
        use_log.info("{key:14}: {val!r}".format(key=key, val=val))


def hunchback_client():
    parser = argparse.ArgumentParser()
    flavours = ("amqp", "mqtt")
    connection_option_keys = (
        ("host", "a"),
        ("port", "i"),
        ("username", "u"),
        ("password", "p"),
    )

    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        dest="dry_run",
        default=False,
        help="Dry run mode",
    )

    publishing_group = parser.add_argument_group("Publishing")
    publishing_group.add_argument(
        "payloads",
        metavar="DATA",
        nargs="*",
        help="Payloads - either JSON encoded parameter or path of a JSON "
        "encoded file",
    )
    publishing_group.add_argument(
        "-r",
        "--routing-key",
        dest="routing_key",
        default="quasimodo.notifications",
        help="Topic",
    )

    flavour_group = parser.add_argument_group("Protocol")
    group = flavour_group.add_mutually_exclusive_group()
    for flavour in flavours:
        group.add_argument(
            "--{:s}".format(flavour),
            const=flavour,
            action="store_const",
            dest="flavour",
            default=flavours[0],
            help="Use {!r} as protocol ".format(flavour),
        )

    connection_group = parser.add_argument_group("Generic Connection Options")
    for opt_l, opt_s in connection_option_keys:
        env_key = "QUASIMODO_{:s}".format(opt_l).upper()
        connection_group.add_argument(
            "-{:s}".format(opt_s),
            "--{:s}".format(opt_l),
            dest=opt_l,
            default=os.environ.get(env_key, OPT_NO_VALUE),
            help="{!r} parameter. Default: %(default)s, "
            "Environment variable: {!r}".format(opt_l, env_key),
        )
    connection_group.add_argument(
        "--listen",
        dest="binding_keys",
        default=[],
        action="append",
        help="Subscriptions",
    )
    connection_group.add_argument(
        "--no-tls", dest="tls", default=True, action="store_false", help="Disable TLS"
    )

    amqp_group = parser.add_argument_group("AMQP Connection Options")
    amqp_group_queue = amqp_group.add_mutually_exclusive_group()
    env_key_queue = "QUASIMODO_QUEUE"
    env_key_exchange = "QUASIMODO_EXCHANGE"
    amqp_group_queue.add_argument(
        "--queue",
        dest="queue",
        default=os.environ.get(env_key_queue, False),
        help="Queue, Environment variable: {!r}".format(env_key_queue),
    )
    amqp_group_queue.add_argument(
        "--exchange",
        dest="exchange",
        default=os.environ.get(env_key_exchange, "amq.topic"),
        help="Exchange, Environment variable: {!r}".format(env_key_exchange),
    )

    tls_group = parser.add_argument_group("TLS Options")
    tls_group.add_argument(
        "--tls-ca",
        dest="cafile",
        default=None,
        help="Certificate Authority File Location",
    )
    tls_group.add_argument(
        "--tls-key",
        dest="keyfile",
        default=None,
        help="Private Key File Location",
    )
    tls_group.add_argument(
        "--tls-cert",
        dest="certfile",
        default=None,
        help="Public Key File Location",
    )
    tls_group.add_argument(
        "--transport-tcp",
        dest="transport",
        default=None,
        help="",
        const="tcp",
        action="store_const",
    )
    tls_group.add_argument(
        "--alpn-amazon",
        dest="alpn_amz",
        default=None,
        help="",
        action="store_true",
    )

    cli_args = parser.parse_args()
    kwargs = dict()

    for key, val in vars(cli_args).items():
        if val == OPT_NO_VALUE:
            continue
        elif key == "binding_keys" and not val:
            continue

        kwargs[key] = val

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y%m%d %H:%M:%S",
    )
    logging.getLogger("pika").setLevel(logging.WARNING)

    log = logging.getLogger(__name__)
    log.debug(kwargs)

    if cli_args.flavour == "amqp":
        impl = MonkeyDumper(**kwargs)
    elif cli_args.flavour == "mqtt":
        impl = ApeDumper(**kwargs)
    else:
        raise ValueError(
            "Implementation for {!r} is not available!".format(cli_args.flavour)
        )

    if cli_args.dry_run:
        log.info("DRY RUN.")
        log.info("")
        dump_hunchback_parameters(kwargs, connection_option_keys)
        sys.exit(0)

    payloads = []
    if cli_args.payloads:
        for p_in in cli_args.payloads:
            try:
                if os.path.isfile(p_in):
                    with open(p_in, "r") as src:
                        payload = json.load(src)
                else:
                    payload = json.loads(p_in)
                payloads.append(payload)
            except Exception as exc:
                log.info("Ignoring payload {!r}, GOT {!s}".format(p_in, exc))

        if not payloads:
            log.error("No payloads? No gain.")
            sys.exit(2)

    try:
        if payloads:
            log.info(payloads)
            for payload in payloads:
                impl.simple_publish(payload, cli_args.routing_key)
        else:
            impl.run()
    except socket.error as sexc:
        log.error("Could not connect: {!s}".format(sexc))
        dump_hunchback_parameters(kwargs, connection_option_keys)
        log.info("")
        log.info("Implementation Object:")
        log.info("=" * 80)
        log.info(impl)
        sys.exit(3)
    except KeyboardInterrupt:
        impl.log.info("You pressed Ctrl-C. This will be reported.")
        sys.exit(1)

    sys.exit(0)
