#!/usr/src/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import ast
import sys
import getopt
import os
import logging
import pandas as pd
import json
import coloredlogs
from urllib.parse import unquote
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q
from typing import List, Optional
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ELASTIC_URL: str = os.environ.get('ELASTIC_URL', 'localhost')
ELASTIC_PORT: int = ast.literal_eval(os.environ.get('ELASTIC_PORT', '9200'))
ELASTIC_SCHEME: str = os.environ.get('ELASTIC_SCHEME', 'http')
ELASTIC_INDEX: str = os.environ.get('ELASTIC_INDEX', 'test')
ELASTIC_QUERY_STRING: str = os.environ.get('ELASTIC_QUERY_STRING', '')
ELASTIC_QUERY: str = os.environ.get('ELASTIC_QUERY', '')
SIZE: int = ast.literal_eval(os.environ.get('SIZE', '5000'))
MAX_SIZE: int = ast.literal_eval(os.environ.get('MAX_SIZE', '0'))
MAX_CONTENT: int = ast.literal_eval(os.environ.get('MAX_CONTENT', '5000'))
LOG_FORMAT: str = os.environ.get('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOG_LEVEL: str = os.environ.get('LOG_LEVEL', 'INFO')
FILE_OUTPUT_NAME: str = os.environ.get('FILE_OUTPUT_NAME', 'output')
FILE_FORMAT: str = os.environ.get('FILE_FORMAT', 'csv')
FILE_OUTPUT_PATH: str = os.environ.get('FILE_OUTPUT_PATH', None)
QUERY: str = os.environ.get('QUERY', '*')
QUERY_STRING: str = os.environ.get('QUERY_STRING', '*')
SCROLL_STR: str = os.environ.get('SCROLL_SIZE', '1m')
QUERY_GREATER_THAN: str = os.environ.get('QUERY_GREATER_THAN', '')
QUERY_LESS_THAN: str = os.environ.get('QUERY_LESS_THAN', '')

UNITS_MAPPING = [
    (1 << 50, ' PB'),
    (1 << 40, ' TB'),
    (1 << 30, ' GB'),
    (1 << 20, ' MB'),
    (1 << 10, ' KB'),
    (1, (' byte', ' bytes')),
]

logger = logging.getLogger(__name__)
coloredlogs.install(level=LOG_LEVEL, logger=logger)
coloredlogs.install(fmt=LOG_FORMAT)


class ElasticParams:
    def __init__(self, gte=None,
                 lte=None,
                 size=10,
                 query='',
                 query_string='',
                 scroll='1m',
                 scroll_id=None,
                 file=None,
                 headers=False,
                 sort=None,
                 showquery=False,
                 rawquery='',
                 max_size: int = None,
                 max_content: int = None,
                 output_path=None,
                 count=0):
        self.gte = gte
        self.lte = lte
        self.size = size
        self.query = query
        self.query_string = query_string
        self.scroll = scroll
        self.scroll_id = scroll_id
        self.file = file
        self.headers = headers
        self.sort = sort
        self.showquery = showquery
        self.rawquery = rawquery
        self.max_size = max_size
        self.max_content = max_content
        self.output_path = output_path
        self.count = count

    def __hash__(self):
        return hash((self.gte,
                     self.lte,
                     self.size,
                     self.query,
                     self.query_string,
                     self.scroll,
                     self.scroll_id,
                     self.file,
                     self.headers,
                     self.sort,
                     self.showquery,
                     self.rawquery,
                     self.max_size,
                     self.max_content,
                     self.output_path,
                     self.count))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __ne__(self, other):
        return not self.__eq__(other)


def doc_help() -> str:
    return """
    Usage: 
    -h, --help: Show this help message and exit"""


def get_size(filepath: str, unit: str) -> float:
    """
    Get the size of a file in bytes, KB, MB, GB, TB, PB
    :type filepath: object
    """
    size = os.path.getsize(filepath)
    if unit == 'b':
        return size
    elif unit == 'kb':
        return size / float(1 << 7)
    elif unit == 'KB':
        return size / float(1 << 10)
    elif unit == 'mb':
        return size / float(1 << 17)
    elif unit == 'MB':
        return size / float(1 << 20)
    elif unit == 'gb':
        return size / float(1 << 27)
    elif unit == 'GB':
        return size / float(1 << 30)
    elif unit == 'tb':
        return size / float(1 << 37)
    elif unit == 'TB':
        return size / float(1 << 40)


def pretty_size(bytesParm, units=None) -> str:
    """Get human-readable file sizes.
    simplified version of https://pypi.python.org/pypi/hurry.filesize/
    """
    global suffix, factor

    if units is None:
        units = UNITS_MAPPING
    for factor, suffix in units:
        if bytesParm >= factor:
            break
    amount = int(bytesParm / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix


def connect(hosts) -> Elasticsearch:
    try:
        client = Elasticsearch(hosts,
                               max_retries=3,
                               request_timeout=30,
                               http_compress=True,
                               headers={"Content-Type": "application/json"})
        # client.info()
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Elasticsearch: {e}")
        return None


def index_exists(es, index):
    return es.indices.exists(index)


def info(es: Elasticsearch):
    try:
        return es.info()
    except Exception as e:
        logger.error(f"Failed to get Elasticsearch info: {e}")
        return None


def search(es: Elasticsearch,
           index: str,
           parameters: ElasticParams) -> Optional[pd.DataFrame]:
    """
    Search for documents in Elasticsearch.
    :param es: Elasticsearch
    :param index: string
    :param parameters: ElasticParams
    :return:
    """
    # print(f"Searching for {parameters.gte}")
    try:
        date_gte = datetime.strptime(parameters.gte, "%Y-%m-%dT%H:%M:%S") if parameters.gte else None
        date_lte = datetime.strptime(parameters.lte, "%Y-%m-%dT%H:%M:%S") if parameters.lte else None
        must = []

        f = Q('range',
              **{'@timestamp':
                  {
                      'gte': date_gte.strftime('%Y-%m-%d %H:%M:%S'),
                      'lte': date_lte.strftime('%Y-%m-%d %H:%M:%S'),
                      'format': 'yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis'
                  }
              })

        q = Q('bool', must=must, filter=[f])

        body: dict = {
            'size': parameters.size,
            'query': q.to_dict(),
        }

        if parameters.query_string != '':
            body.get('query').get('bool')['must'] = [{'query_string': {'query': parameters.query_string}}]

        if parameters.query != '':
            q = parameters.query.split(',')
            for i in q:
                must_string = i.split('=')
                # body.get('query').get('bool')['must'].append(Q('match', **{must_string[0]: must_string[1]}))

        if parameters.rawquery != '':
            body['query'] = json.loads(unquote(parameters.rawquery))

        if parameters.showquery:
            print(json.dumps(body, indent=4))
            # with open(file_name, 'w', encoding='utf-8') as f:
            #     json.dump(body, f, ensure_ascii=False, indent=4)
            return None

        if parameters.scroll_id is None:
            response = es.search(index=index,
                                 body=body,
                                 size=parameters.size,
                                 sort=parameters.sort,
                                 scroll=parameters.scroll)
        else:
            response = es.scroll(scroll=parameters.scroll, scroll_id=parameters.scroll_id)

        if len(response.get('hits').get('hits')) > 0:
            if parameters.max_size is not None and parameters.max_size <= int(get_size(parameters.file, 'MB')):
                logger.debug(
                    f"File size is {get_size(parameters.file, 'MB')} MB. Max size is {parameters.max_size} MB.")
                return None

            l: List = response.get('hits').get('hits')
            data_list: List = []

            for i in l:
                data_list.append(i['_source'].values())

            # file = open(parameters.file)
            # file.seek(0, os.SEEK_END)

            # print(f"{pretty_size(file.tell())}")

            data = pd.DataFrame(data_list, columns=i['_source'].keys())
            data.to_csv(parameters.file, mode='a', header=parameters.headers, index=False)
            parameters.count += len(data_list)
            parameters.scroll_id = response.get('_scroll_id')

            return search(es,
                          index,
                          parameters)

        return response
    except Exception as e:
        logger.error(f"Failed to search Elasticsearch: {e}")
        return None


def create_if_not_exist(file_name: str, path: str = None) -> str:
    if path is None:
        path = f"{os.getcwd()}/"
    temp_file_name = file_name
    logger.debug(f"{os.getcwd()}")
    logger.debug(f"Creating file {temp_file_name} in {path}")
    file_name = f'{path}{temp_file_name}'
    existGDBPath = f'{path}{temp_file_name}'
    wkspFldr = os.path.dirname(existGDBPath)
    logger.debug(f"Current path {wkspFldr}")
    file_name = f"{wkspFldr}{temp_file_name}"

    try:
        logger.debug(f"Creating file {file_name}")
        open(file_name, 'r').close()
    except IOError as e:
        open(file_name, 'w').close()
        logger.error(f"Error: {e}")
    except Exception as e:
        logger.error(f"Error: {e}")

    return file_name


def run_standalone():
    try:
        params = ElasticParams(gte=QUERY_GREATER_THAN,
                               lte=QUERY_LESS_THAN,
                               query_string=ELASTIC_QUERY_STRING,
                               query=ELASTIC_QUERY,
                               size=SIZE,
                               max_size=None,
                               output_path=FILE_OUTPUT_PATH,
                               scroll=SCROLL_STR,
                               max_content=MAX_CONTENT)
        es: Elasticsearch = None
        query_type: str = ''
        file_output_name: str = FILE_OUTPUT_NAME
        file_format: str = FILE_FORMAT
        output_path: str = FILE_OUTPUT_PATH
        elastic_scheme: str = ELASTIC_SCHEME
        elastic_url: str = ELASTIC_URL
        elastic_port: int = ELASTIC_PORT
        elastic_index: str = ELASTIC_INDEX

        logger.debug(f"[MAIN] {params.__dict__}")
        opts, args = getopt.getopt(sys.argv[1:],
                                   "h:u:p:i:g:l:qs:q:t:o:f:s:op:c:show:r:ms:mc:",
                                   ["help=",
                                    "url=",
                                    "port=",
                                    "index=",
                                    "greater_than=",
                                    "less_than=",
                                    "query_string=",
                                    "query=",
                                    "type=",
                                    "output=",
                                    "format=",
                                    "scroll=",
                                    "output_path=",
                                    "columns=",
                                    "showquery=",
                                    "size=",
                                    "rawquery=",
                                    "max_size=",
                                    "max_content=",
                                    ])

        for opt, arg in opts:
            if opt == "-h" or opt == "--help":
                print(doc_help())
                sys.exit(0)
            if opt == "-p" or opt == "--port":
                elastic_port = arg
            if opt == "-i" or opt == "--index":
                elastic_index = arg
            if opt == "-u" or opt == "--url" or opt == "-host" or opt == "--host":
                elastic_url = arg
            if opt == "--query_string":
                params.query_string = arg
            if opt == "-q" or opt == "--query":
                params.query = arg
            if opt == "-t" or opt == "--type":
                query_type = arg
            if opt == "-o" or opt == "--output":
                file_output_name = arg
            if opt == "-f" or opt == "--format":
                file_format = arg
            if opt == "--greater_than":
                params.gte = arg
            if opt == "--less_than":
                params.lte = arg
            if opt == "--scroll":
                params.scroll = arg
            if opt == "-l" or opt == "--limit":
                params.limit = int(arg)
            if opt == "-d" or opt == "--output_path":
                params.output_path = arg
            if opt == "-c" or opt == "--columns":
                params.headers = arg.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
            if opt == "--showquery":
                params.showquery = arg.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
            if opt == "--rawquery":
                params.rawquery = arg
            if opt == "--max_size":
                params.max_size = ast.literal_eval(arg)
            if opt == "--max_content":
                params.max_content = ast.literal_eval(arg)

        es = connect([f"{elastic_scheme}://{elastic_url}:{elastic_port}"])
        logger.debug(
            f"Parameters {params.query_string}:{params.query}:{file_output_name}:{file_format}:{params.scroll}:{output_path}:{params.headers}:{params.showquery}")

        if es is None:
            raise Exception("Elasticsearch not connected")

        params.file = create_if_not_exist(f'{file_output_name}.{file_format}', output_path)

        if es is not None:
            logger.debug(es)
            if query_type != '':
                if query_type == "info":
                    res = info(es)
                    logger.debug(f"{res}" + "\n")
            else:
                logger.debug(f"{params.gte}")
                res = search(es,
                             elastic_index,
                             params)
                logger.debug(f"{res}" + "\n")
        sys.exit(0)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user... Exiting")
        sys.exit(0)
    except Exception as e:
        logger.error("{0}".format(e))
        sys.exit(1)
    except getopt.GetoptError as err:
        logger.error("{0}".format(err))
        sys.exit(1)


if __name__ == "__main__":
    run_standalone()
