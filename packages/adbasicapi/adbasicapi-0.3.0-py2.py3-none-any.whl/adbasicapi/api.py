# -*- coding: utf-8 -*-

"""Main module."""


import os
import requests
import json
import logging
import socket

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")
URL = "https://api.alwaysdata.com/v1/{what}/"
# get API credentials environment variables
apikey = os.getenv("AD_APIKEY")
account = os.getenv("AD_ACCOUNT")
CREDENTIALS = (f"{apikey} account={account}", "")


def check_if_single(seq):
    """check if passed sequence contains one and only one item.
    If not, raise an appropriate exception

    >>> check_if_single(("a",))
    'a'
    """
    if len(seq) > 1:
        raise ValueError("multiple items in passed sequence")
    elif len(seq) == 0:
        raise ValueError("no item defined in sequence")
    return seq[0]


def getIP(url=None, type="A"):
    """return IP
    If `url` is not provided, retrieve host's public IP
    >>> getIP()
    '...'
    """
    if url:
        # ip = socket.gethostbyname(url)
        ip = get_site_record(url, type=type)["value"]
    else:
        # get own public IP
        response = requests.get("https://ipecho.net/plain")
        ip = response.content.decode()
    return ip


def forge_url(what):
    """forge appropriate URL for AD domains

    >>> forge_url("toto")
    'https://api.alwaysdata.com/v1/toto/'
    """
    url = URL.format(what=what)
    return url


def requests_get(what_to_search):
    """forge an url from URL global var and sends a request to this url.
    If returned code is OK, return decoded server response as a python object.

    >>> requests_get("account")
    [{'id': ...}]
    """
    url = forge_url(what=what_to_search)
    # Send HTTP request
    response = requests.get(
        url,
        auth=CREDENTIALS,
    )
    if response.ok is False:
        msg = f"{url}:: code{response.status_code}"
        logging.error(msg)
        raise ValueError(msg)
    return json.loads(response.content.decode())


def split_url(url):
    """return a tuple `name`, `domain`
    >>> split_url("www.dsfgsdf-sdfsdf.fgh")
    ('www', 'dsfgsdf-sdfsdf.fgh')
    >>> split_url("www.a.b.c.dsfgsdf-sdfsdf.fgh")
    ('www.a.b.c', 'dsfgsdf-sdfsdf.fgh')
    """
    tokens = url.split(".")
    name = ".".join(tokens[:-2])
    domain = ".".join(tokens[-2:])
    return name, domain


def get_site_record(url, check_single=True, type="A"):
    # domain and name
    name, domain = split_url(url)
    # =========================================================
    # first step: recover domain definition
    # =========================================================
    domains = requests_get("domain")  # recover all the domains defined
    # --------------------------------------------------------
    # keep only domains refereing to passed argument `domain`
    domains = [d for d in domains if d["name"] == domain]
    # ensure that we found one and only one domain
    domain = check_if_single(domains)
    # =========================================================
    # second step: find records linked to found domain definition
    # =========================================================
    records = requests_get(what_to_search="record")
    records = [
        record
        for record in records
        if record["domain"]["href"] == domain["href"]
        and record["name"] == name
        and record["type"] == type  # discard IPV6
        and record["is_active"] is True
    ]
    if len(records) > 1:
        logging.warning("still more than one record")
        records = [record for record in records if record["is_user_defined"] is True]
    if check_single:
        return check_if_single(records)
    return records


def modify_record_targetIP(url=None, targetIP=None, dry_run=False):
    if not url:
        url = os.getenv("AD_SITE_URL")
    logging.info(f"checking {url=}")
    name, domain = split_url(url)
    if not targetIP:
        targetIP = getIP()  # get my own public IP
    # ----------------------------------------------------------
    # check if this is necessary
    current_ip = getIP(url=url)
    logging.info(f"checking {targetIP=} vs. {current_ip=}")
    if targetIP == current_ip:
        logging.info("nothing to do...")
        return True
    # -----------------------------------------------------------
    # get domain info
    domain_name = domain  # keep it for later use
    domain = get_site_record(url)
    href = domain["href"]
    # '/v1/record/6432223/' -> 'record/6432223'
    href = href.strip("/").replace("v1/", "")
    url = forge_url(href)
    # ------------------------------------------------------------
    # forge
    domain_data = {"value": targetIP, "name": name}
    logging.info(
        f"{domain_name}: attempt to change IP from {domain['value']} to {targetIP}"
    )
    if dry_run:
        logging.warning("dry_run requested. no action performed")
        return
    response = requests.patch(url, auth=CREDENTIALS, data=json.dumps(domain_data))
    if response.ok:
        logging.info("all right!")
    return response.ok


def modify_record_cname(url=None, cname_target=None, dry_run=False):
    if not url:
        url = os.getenv("AD_SITE_CNAME")
    logging.info(f"checking {url=}")
    name, domain = split_url(url)
    if not cname_target:
        cname_target = os.getenv("AD_SITE_URL")
    # ensure `target_cnames` is an iterable of urls

    # ----------------------------------------------------------
    # check if this is necessary
    current_cname_target = getIP(url=url, type="CNAME")
    logging.info(
        f"checking locally defined {cname_target=} vs. {current_cname_target=}"
    )
    if cname_target == current_cname_target:
        logging.info("nothing to do...")
        return True
    # -----------------------------------------------------------
    # get record info
    record = get_site_record(url, type="CNAME")
    href = record["href"].strip("/").replace("v1/", "")
    url = forge_url(href)
    record_data = {"value": cname_target}
    logging.info(
        f"{name}.{domain}: attempt to change CNAME target from `{record['value']}` to `{cname_target}`"
    )
    if dry_run:
        logging.warning("dry_run requested. no action performed")
        return
    response = requests.patch(url, auth=CREDENTIALS, data=json.dumps(record_data))
    if response.ok:
        logging.info("all right!")
    return response.ok


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
