import logging
import config

def version(obj):
    logging.info(obj["version"])

def mr(objs):
    mr_sources = []
    for obj in objs:
        mr_sources.append(obj["title"])
        logging.info(obj["title"])

    return mr_sources
