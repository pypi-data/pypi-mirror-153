# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cursed_hr',
 'gallia',
 'gallia.db',
 'gallia.services',
 'gallia.transports',
 'gallia.uds',
 'gallia.uds.core',
 'gallia.udscan',
 'gallia.udscan.scanner',
 'opennetzteil',
 'penlog']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.8.0,<0.9.0',
 'aiohttp>=3.8.1,<4.0.0',
 'aiosqlite>=0.17.0,<0.18.0',
 'argcomplete>=2.0.0,<3.0.0',
 'python-can>=4.0.0,<5.0.0',
 'pyxcp>=0.16.0,<0.17.0',
 'tabulate>=0.8.9,<0.9.0',
 'zstandard>=0.17.0,<0.18.0']

entry_points = \
{'console_scripts': ['cursed-hr = cursed_hr.cursed_hr:main',
                     'discover-xcp = gallia.udscan.scanner.find_xcp:main',
                     'gallia = gallia.cli:main'],
 'gallia_scanners': ['discover-can-ids = '
                     'gallia.udscan.scanner.find_can_ids:FindCanIDsScanner',
                     'discover-endpoints = '
                     'gallia.udscan.scanner.find_endpoints:FindEndpoints',
                     'discover-iso-tp-addr = '
                     'gallia.udscan.scanner.find_iso_tp_addr:FindISOTPAddrScanner',
                     'scan-dump-seeds = '
                     'gallia.udscan.scanner.scan_sa_dump_seeds:SaDumpSeeds',
                     'scan-identifiers = '
                     'gallia.udscan.scanner.scan_identifiers:ScanIdentifiers',
                     'scan-memory-functions = '
                     'gallia.udscan.scanner.scan_memory_functions:ScanWriteDataByAddress',
                     'scan-reset = gallia.udscan.scanner.scan_reset:ScanReset',
                     'scan-services = '
                     'gallia.udscan.scanner.scan_services:ScanServices',
                     'scan-sessions = '
                     'gallia.udscan.scanner.scan_sessions:IterateSessions',
                     'simple-dtc = gallia.udscan.scanner.simple_dtc:DTCScanner',
                     'simple-ecu-reset = '
                     'gallia.udscan.scanner.simple_ecu_reset:EcuReset',
                     'simple-get-vin = '
                     'gallia.udscan.scanner.simple_get_vin:GetVin',
                     'simple-iocbi = gallia.udscan.scanner.simple_iocbi:IOCBI',
                     'simple-ping = gallia.udscan.scanner.simple_ping:Ping',
                     'simple-read-by-identifier = '
                     'gallia.udscan.scanner.simple_read_by_identifier:ReadByIdentifier',
                     'simple-read-error-log = '
                     'gallia.udscan.scanner.simple_read_error_log:ReadErrorLog',
                     'simple-rmba = '
                     'gallia.udscan.scanner.simple_rmba:ReadMemoryByAddressScanner',
                     'simple-rtcl = gallia.udscan.scanner.simple_rtcl:RTCL',
                     'simple-send-pdu = '
                     'gallia.udscan.scanner.simple_send_pdu:SendPDU',
                     'simple-test-xcp = '
                     'gallia.udscan.scanner.simple_test_xcp:TestXCP',
                     'simple-wmba = '
                     'gallia.udscan.scanner.simple_wmba:WriteMemoryByAddressScanner',
                     'simple-write-by-identifier = '
                     'gallia.udscan.scanner.simple_write_by_identifier:WriteByIdentifier',
                     'vecu = gallia.virtual_ecu:VirtualECU']}

setup_kwargs = {
    'name': 'gallia',
    'version': '1.0.0a6',
    'description': 'Extendable Pentesting Framework',
    'long_description': '# Gallia\n\n[![docs](https://img.shields.io/badge/-docs-green)](https://fraunhofer-aisec.github.io/gallia)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gallia)](https://pypi.python.org/pypi/gallia/)\n[![PyPI - License](https://img.shields.io/pypi/l/gallia)](https://www.apache.org/licenses/LICENSE-2.0.html)\n[![PyPI](https://img.shields.io/pypi/v/gallia)](https://pypi.python.org/pypi/gallia/)\n\nGallia is an extendable pentesting framework with the focus on the automotive domain.\nThe scope of gallia is conducting penetration tests from a single ECU up to whole cars, with the main focus on the UDS interface.\nTaking advantage of this modular design, the [logging and archiving](https://github.com/Fraunhofer-AISEC/penlog) functionality was developed separately.\nActing as a generic interface, the logging functionality implements reproducible tests and enables post-processing analyzer tasks.\nThe [rendered documentation](https://fraunhofer-aisec.github.io/gallia) is available via Github Pages.\n\nKeep in mind that this project is intended for research and development usage only!\nInappropriate usage might cause irreversible damage to the device under test.\nWe do not take any responsibility for damage caused by the usage of this tool.\n\n## Quickstart\n\n```\n$ pip install gallia\n$ gallia simple-dtc --target "isotp://can0?src_addr=0x123&dst_addr=0x312&tx_padding=0xaa&rx_padding=0xaa" read\n```\n\nFor specifying the `--target` argument see the [transports documentation](https://fraunhofer-aisec.github.io/gallia/transports.html).\n\n## Acknowledgments\n\nThis work was partly funded by the German Federal Ministry of Education and Research (BMBF) as part of the [SecForCARs](https://www.secforcars.de/) project (grant no. 16KIS0790).\nA short presentation and demo video is available at this [demo page](https://www.secforcars.de/demos/10-automotive-scanning-framework.html).\n',
    'author': 'AISEC Pentesting Team',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Fraunhofer-AISEC/gallia',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
