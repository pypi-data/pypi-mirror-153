""" Convert HAR (HTTP Archive) to YAML/JSON testCase for HttpRunner.

Usage:
    # convert to JSON format testCase
    >>> doc2case '-u url'

    # convert to YAML format testCase
    >>> doc2case 'url -p test_path -f yml or json'

"""
import argparse

from loguru import logger
import sys

from kernel import __description__
from kernel.core import SwaggerParser

try:
    from kernel import __version__ as SG_VERSION
except ImportError:
    SG_VERSION = None


if len(sys.argv) == 1:
    sys.argv.append('--help')

parser = argparse.ArgumentParser(description=__description__)
parser.add_argument('-v', '--version', dest='version', help="show version")
parser.add_argument('api_doc_url', type=str, help="Specifies the URL of the Swagger interface document to parse .")
parser.add_argument(
    '-p', '--test_path', help="Specify test path resolution.")
parser.add_argument(
    '-f', '--to-yml', '--to-yaml',
    dest='to_yaml',
    help="Convert to YAML format, if not specified, convert to JSON format by default.")


def mainRun():
    """ HAR converter: parse command line options and run commands.
    """

    args = parser.parse_args()
    if args.version:
        logger.info("{}".format(SG_VERSION))
        exit(0)

    api_doc_url = args.api_doc_url
    test_path = args.test_path
    output_file_type = "yml" if args.to_yaml else "json"

    if not api_doc_url:
        logger.error("Swagger interface document URL cannot be empty.")
        sys.exit(1)

    SwaggerParser(api_doc_url).gen_testCase(test_path, output_file_type)
    return 0


if __name__ == '__main__':
    mainRun()
