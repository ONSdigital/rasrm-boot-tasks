import logging
import argparse
import json
import requests

def parse_args():
    parser = argparse.ArgumentParser(description='Batch HTTP Loader')
    parser.add_argument("file", help="JSON batch file to load")
    parser.add_argument("--username", help="Basic auth username", required=True)
    parser.add_argument("--password", help="Basic auth password", required=True)
    parser.add_argument("--host", help="HTTP host", required=True)
    parser.add_argument("--port", help="HTTP port", required=True)
    parser.add_argument("--scheme", help="HTTP port", default='http')
    return parser.parse_args()

def build_url(params, details):
    return "{}://{}:{}{}".format(params.scheme, params.host, params.port, details['context'])

def get_request_fn(details):
    return {
        'POST': requests.post,
        'PUT': requests.put,
        'GET': requests.get
    }[details['method'].upper()]
    
def execute_request(params, details):
    logging.debug("Details: {}".format(details))
    url = build_url(params, details)
    logging.debug("URL: {}".format(url))
    request_fn = get_request_fn(details)

    if type(details['payload']) is dict:
        r = request_fn(url, json=details['payload'], auth=(params.username, params.password))
    else:
        r = request_fn(url, data=details['payload'], auth=(params.username, params.password))

    logging.info("{} <- {} {} - {}".format(r.status_code, details['method'], url, details['payload']))

def execute_batch_file(params):
    json_file = params.file
    file = open(json_file, "r")
    with open(json_file, 'r') as file:
        json_str = file.read()
        
    batch = json.loads(json_str)

    [execute_request(params, details) for details in batch]
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    args = parse_args()

    execute_batch_file(args)
    
