

def gather_logs(filename):
    with open(filename) as f:
        return [line.strip() for line in f]


def split_logs_with_separator(logs: list, separator: str):
    return [log.split(separator) for log in logs]
