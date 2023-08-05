import os
import json

from uuid import uuid4


def gen_uuid():
    """
    Objetivo: Criar uuids.
    """
    uuid_str = str(uuid4())
    return uuid_str


def convert_days_to_sec(days):
    """
    Objetivo: Converter um numero em dias para formato em segundos.
    """
    seconds = int(days) * 86400
    return seconds


def velero(cmd):
    """
    Objetive: Run velero and get output json
    """
    run = os.popen(f"velero {cmd} -o json")
    return json.loads(run.read())

def velero_str(cmd):
    """
    Objetive: Run velero and get output text
    """
    run = os.popen(f"velero {cmd}")
    return run.read()
