import os


def create_files(repository_name, url):
    queue = repository_name + "/queue.txt"
    crawled = repository_name + "/crawled.txt"

    if not os.path.isfile(queue):
        write_to_file(queue, url)

    if not os.path.isfile(crawled):
        write_to_file(crawled, '')


def write_to_file(path, data):
    f = open(path, "w")
    f.write(data)
    f.close()


def append_to_file(path, data):
    with open(path, "a") as file:
        file.write(data + "\n")


def delete_from_file(path):
    open(path, 'w').close()


def file_to_set(file):
    results = set()
    with open(file, "rt") as f:
        for line in f:
            results.add(line.replace("\n", ""))
        return results


def set_to_file(links, file):
    with open(file, "w") as f:
        for l in sorted(links):
            f.write(l + "\n")
