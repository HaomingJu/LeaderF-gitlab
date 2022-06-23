import os

db_path = os.path.dirname(os.path.abspath(__file__)) + '/.db'

def version(response):
    if response.status_code == 200:
        return True
    else:
        return False

def mr(response):
    if response.status_code == 200:
        mr_sources = []
        for obj in response.json():
            mr_sources.append("{} {}".format(obj["id"], obj["title"]))
            mr_file = "{}/{}".format(db_path, obj["id"])
            with open(mr_file, 'w') as mr_handle:
                mr_handle.write("** {} ** \n\n".format(obj["title"]))
                mr_handle.write("@{} ({} >>> {})\n\n".format(obj["author"]["name"], obj["source_branch"], obj["target_branch"]))
                mr_handle.write(obj["description"])

        return mr_sources
    else:
        return ["-1 response status_code != 200"]


