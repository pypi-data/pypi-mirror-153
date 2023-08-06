"""
PDS Validate Wrapper

Tool that downloads PDS Validate Tool and executes based upon
input arguments.
"""
import argparse
import fileinput
import glob
import logging
import os
import requests
import sys

from datetime import datetime
from subprocess import Popen, CalledProcessError, PIPE, STDOUT
from urllib.parse import urljoin
from xml.etree import ElementTree as et

from .util import get_latest_release

from pds_github_util.assets.assets import download_asset, unzip_asset
from pds_github_util.utils.ldd_gen import convert_pds4_version_to_alpha
from pds_github_util.utils import addStandardArguments

GITHUB_ORG = 'NASA-PDS'
GITHUB_REPO = 'validate'
PDS_NS_URL = 'http://pds.nasa.gov/pds4/pds/v1'

# Schema download constants
PDS_SCHEMA_URL = 'https://pds.nasa.gov/pds4/pds/v1'
PDS_DEV_SCHEMA_URL = 'https://pds.nasa.gov/datastandards/schema/develop/pds/'
DOWNLOAD_PATH = '/tmp'

_logger = logging.getLogger(__name__)


def exec_validate(executable, args, data_path, pds4_version, failure_expected=False, log_path=os.path.expanduser('~')):
    dtime = datetime.now().strftime('%Y%m%d%H%M%S')
    log_out = os.path.join(log_path, f'validate_report_{dtime}.txt')
    if not os.path.exists(os.path.dirname(log_out)):
        os.makedirs(os.path.dirname(log_out))

    # Get test files to validate
    test_data = set_test_data(data_path, pds4_version)

    # Test valid  vs invalid data.
    # test_data should not be None because the schema generation should at least produce 1 XML
    for key, files in test_data.items():
        if not files:
            continue

        validate_args = args.copy()
        validate_args.append('-t')
        validate_args.extend(files)

        cmd = ['bash', executable]
        cmd.extend(validate_args)
        with Popen(cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, universal_newlines=True) as p:
            with open(log_out, 'w') as f:
                for line in p.stdout:
                    print(line, end='') # process line here
                    f.write(line)

        success = False
        if p.returncode != 0 and key == "fail":
            success = True
        elif p.returncode == 0 and key == "valid":
            success = True
        else:
            raise CalledProcessError(p.returncode, p.args)

    return success


def download_schemas(download_path, pds4_version, dev_release=False):
    pds4_version_short = convert_pds4_version_to_alpha(pds4_version)

    if not dev_release:
        base_url = PDS_SCHEMA_URL
    else:
        base_url = PDS_DEV_SCHEMA_URL

    fname = 'PDS4_PDS_' + pds4_version_short
    try:
        for suffix in ['.xsd', '.sch']:
            url = urljoin(base_url, fname + suffix)
            _logger.info(f'Downloading {url}')
            r = requests.get(url, allow_redirects=True)
            r.raise_for_status()
            with open(os.path.join(download_path, fname + suffix), 'wb') as f:
                f.write(r.content)
    except requests.exceptions.HTTPError:
        # if ops version fails, let's try to download from dev
        if not dev_release:
            _logger.warning("Schemas not found online in production. Trying development version...")
            download_schemas(download_path, pds4_version, True)
        else:
            raise


def set_test_data(data_path, pds4_version):
    """ Set Test Data for Validate Run

    Walk the input test root paths, find all the test data files,
    and insert the PDS4 version

    :param data_path: root path to the test data
    :param pds4_version: PDS4 version to insert into the test data
    :return: dictionary of valid/fail paths to the test data
    """
    test_data = { "valid": [], "fail": []}
    for path in data_path:
        for root, dirs, files in os.walk(path):
            for f in files:
                if f.lower().endswith(".xml") or f.lower().endswith(".lblx"):
                    file_path = os.path.join(root, f)
                    insert_pds4_version(file_path, pds4_version)
                    if "fail" in f.lower():
                        test_data["fail"].append(file_path)
                    else:
                        test_data["valid"].append(file_path)
    return test_data


def insert_pds4_version(file_path, pds4_version):
    """ Insert PDS4 Version into label

    :param file_path: absolute path to file(s)
    :param pds4_version: PDS4 version to insert
    """
    for line in fileinput.input(files=file_path, inplace=True):
        if '<information_model_version>' in line:
            print(f'        <information_model_version>{pds4_version}</information_model_version>')
        else:
            print(line, end='')


def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__)
    addStandardArguments(parser)
    parser.add_argument('--deploy_dir',
                        help='directory to deploy the validate tool on the file system',
                        default='/tmp')
    parser.add_argument('--token',
                        help='github token')
    parser.add_argument('--schemas',
                        help='path(s) to schemas to validate against')
    parser.add_argument('--schematrons',
                        help='path(s) to schematrons to validate against')
    parser.add_argument('--skip_content_validation',
                        help='validate: skip content validation',
                        action='store_true', default=False)
    parser.add_argument('--failure_expected', dest='failure_expected',
                        help='validate expected to fail',
                        action='store_true', default=False)
    parser.add_argument('--datapath',
                        help='path(s) to data to validate',
                        nargs='+')
    parser.add_argument('--output_log_path',
                        help='path(s) to output validate run log file',
                        default=os.path.join('tmp', 'logs'))
    parser.add_argument('--with_pds4_version',
                        help=('force the following PDS4 version. software will '
                              'download and validate with this version of the '
                              'PDS4 Information Model. this version should be '
                              'the semantic numbered version. e.g. 1.14.0.0'))
    parser.add_argument('--development-release',
                        help=('flag to indicate this should be tested with a '
                              'development release of the PDS4 Standard.'),
                        action='store_true', default=False)

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel, format="%(levelname)s %(message)s")

    token = args.token or os.environ.get('GITHUB_TOKEN')

    if not token:
        _logger.error('Github token must be provided or set as environment variable (GITHUB_TOKEN).')
        sys.exit(1)

    try:
        validate_args = ['-R', 'pds4.label']

        if args.skip_content_validation:
            validate_args.append('--skip-content-validation')

        schemas = []
        if args.schemas:
            schemas.extend(glob.glob(args.schemas, recursive=True))

        schematrons = []
        if args.schematrons:
            # validate_args.append('-S')
            schematrons.extend(glob.glob(args.schematrons, recursive=True))

        if args.development_release:
            if not args.with_pds4_version:
                raise argparse.ArgumentError('--with_pds4_version must be specified when using --development_release')

        if args.with_pds4_version:
            download_schemas(DOWNLOAD_PATH, args.with_pds4_version, dev_release=args.development_release)
            schemas.extend(glob.glob(os.path.join(DOWNLOAD_PATH, '*.xsd')))
            schematrons.extend(glob.glob(os.path.join(DOWNLOAD_PATH, '*.sch')))

        if schemas:
            validate_args.append('-x')
            validate_args.extend(schemas)

        if schematrons:
            validate_args.append('-S')
            validate_args.extend(schematrons)

        release = get_latest_release(token, GITHUB_ORG, GITHUB_REPO)
        pkg = download_asset(release, args.deploy_dir, startswith="validate", file_extension='.zip')
        sw_dir = unzip_asset(pkg, args.deploy_dir)

        exec_validate(os.path.join(sw_dir, 'bin', 'validate'),
                      validate_args,
                      args.datapath,
                      args.with_pds4_version,
                      failure_expected=args.failure_expected,
                      log_path=args.output_log_path)

    except CalledProcessError:
        _logger.error('FAILED: Validate failed unexpectedly. See output logs.')
        sys.exit(1)

    _logger.info('SUCCESS: Validation complete.')


if __name__ == '__main__':
    main()
