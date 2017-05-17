#!/usr/bin/env python
# coding=utf-8

"""
benchmark popular serialization libraries
"""

from __future__ import print_function, unicode_literals

import logging
import sys
import uuid
import random
import datetime
import json

from wells.debug import trace_time
import msgpack
import umsgpack
import msgpack_pypy

import obj_pb2


logging.basicConfig(format='%(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def gen_obj():
    """generate a random python dict with a few keys.

    """
    randstr = "%s" % (uuid.uuid4(),)
    time = datetime.datetime.now().isoformat()
    return {
        "id": randstr,
        "key1": randstr[:random.randint(10, 30)],
        "key2": randstr[:random.randint(10, 30)],
        "key3": randstr[:random.randint(10, 30)],
        "key4": randstr[:random.randint(10, 30)],
        "key5": randstr[:random.randint(10, 30)],
        "key6": random.randint(10, 30),
        "key7": randstr[:random.randint(10, 30)],
        "key8": time,
        "key9": time,
    }


def gen_objs(n):
    """generate n python dicts.

    """
    return [gen_obj() for _ in range(n)]


@trace_time()
def bench_json_encode(objs):
    result = []
    for obj in objs:
        result.append(json.dumps(obj))
    return result


@trace_time()
def bench_json_decode(strs):
    for s in strs:
        json.loads(s)


def prepare_data_for_pb(objs):
    result = []
    for obj in objs:
        msg = obj_pb2.Object()
        for k, v in obj.items():
            setattr(msg, k, v)
        result.append(msg)
    return result


@trace_time()
def bench_pb_encode(objs):
    result = []
    for obj in objs:
        result.append(obj.SerializeToString())
    return result


@trace_time()
def bench_pb_decode(strs):
    for s in strs:
        msg = obj_pb2.Object()
        msg.ParseFromString(s)


@trace_time()
def bench_msgpack_encode(objs):
    result = []
    for obj in objs:
        result.append(umsgpack.packb(obj))
    return result


@trace_time()
def bench_msgpack_decode(strs):
    for s in strs:
        umsgpack.unpackb(s)


@trace_time()
def bench_umsgpack_encode(objs):
    result = []
    for obj in objs:
        result.append(umsgpack.packb(obj))
    return result


@trace_time()
def bench_umsgpack_decode(strs):
    for s in strs:
        umsgpack.unpackb(s)


@trace_time()
def bench_msgpack_pypy_encode(objs):
    result = []
    for obj in objs:
        result.append(msgpack_pypy.dumps(obj))
    return result


@trace_time()
def bench_msgpack_pypy_decode(strs):
    for s in strs:
        msgpack_pypy.loads(s)


def main():
    N = 50000
    objs = gen_objs(N)

    logger.info("running in python %s", sys.version)

    logger.info("running json benchmark")
    r = bench_json_encode(objs)
    bench_json_decode(r)

    logger.info("running pb benchmark")
    r = bench_pb_encode(prepare_data_for_pb(objs))
    bench_pb_decode(r)

    logger.info("running msgpack (msgpack-python) benchmark")
    r = bench_msgpack_encode(objs)
    bench_msgpack_decode(r)

    logger.info("running msgpack (u-msgpack-python) benchmark")
    r = bench_umsgpack_encode(objs)
    bench_umsgpack_decode(r)

    logger.info("running msgpack (msgpack-pypy) benchmark")
    r = bench_msgpack_pypy_encode(objs)
    bench_msgpack_pypy_decode(r)


if __name__ == '__main__':
    main()
