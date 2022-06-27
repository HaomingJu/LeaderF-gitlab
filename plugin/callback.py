import os
import ast

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
        with open('{}/{}'.format(db_path, 'summary'), 'w') as summary_handle:
            summary_handle.write(str(mr_sources))
        with open('{}/{}'.format(db_path, 'etag'), 'w') as etag_handle:
            etag_handle.write(response.headers['ETag'])

        return mr_sources
    elif response.status_code == 304:
        summary = ""
        with open('{}/{}'.format(db_path, 'summary'), 'r') as summary_handle:
            summary = summary_handle.read()
        return ast.literal_eval(summary)

    else:
        return ["-1 response status_code != 200, is {}".format(response.status_code)]


