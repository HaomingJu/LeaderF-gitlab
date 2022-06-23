import logging

def version(response):
    if response.status_code == 200:
        logging.info(response.json()["version"])
        return True
    else:
        return False

def mr(response):
    if response.status_code == 200:
        mr_sources = []
        for obj in response.json():
            mr_sources.append("{} {}".format(obj["id"], obj["title"]))
            logging.info(obj["title"])
        return mr_sources
    else:
        return ["-1 response status_code != 200"]


