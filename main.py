import argparse
from flask import Flask, render_template, jsonify

from log_parser import gather_logs, split_logs_with_separator

parser = argparse.ArgumentParser(
    prog='OpenLogViewer',
    description='This is a web app to display and filter application logs')

app = Flask(__name__)


@app.route('/')
def logs():
    args = parser.parse_args()

    logs = gather_logs(args.filename)
    split_log = split_logs_with_separator(logs, args.separator)

    colors = {"DEBUG": "#21B9E4",
              "INFO": "#32EE65",
              "ERROR": "#FB1645",
              "WARNING": "#FB8916",
              }

    filters = [{"column": 0,
                "color": "#21B9E4",
                "tag": "DEBUG",
                "active": True},
               {"column": 0,
                "color": "#FB1645",
                "tag": "INFO",
                "active": True}]

    return render_template('index.html', logs=split_log, filters=filters)


if __name__ == '__main__':
    parser.add_argument('filename',
                        help="The log file you want to see.")
    parser.add_argument('-s', '--separator',
                        help="The separator of log columns")

    app.run(debug=True)
