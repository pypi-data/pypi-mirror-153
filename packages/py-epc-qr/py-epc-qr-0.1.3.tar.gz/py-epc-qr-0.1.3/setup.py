# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_epc_qr']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0',
 'PyYAML>=6.0,<7.0',
 'qrcode>=7.3.1,<8.0.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['epcqr = py_epc_qr.__main__:main']}

setup_kwargs = {
    'name': 'py-epc-qr',
    'version': '0.1.3',
    'description': 'Generate EPC-compatible QR codes for wire transfers',
    'long_description': '[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![codecov](https://codecov.io/gh/timueh/py-epc-qr/branch/main/graph/badge.svg?token=LMQKVGWT2W)](https://codecov.io/gh/timueh/py-epc-qr)\n![tests](https://github.com/timueh/py-epc-qr/actions/workflows/pytest.yml/badge.svg)\n![lint_with_black](https://github.com/timueh/py-epc-qr/actions/workflows/black.yml/badge.svg)\n\n# Create QR codes for wire transfers\n\nSick of copy-and-pasting IBANs to forms?\nWhy not just scan a QR code and have your favorite banking app take care of the rest?\n\nWhy not be generous and support wikipedia with EUR10?\nGrab your phone, open your banking app, select the QR scanner and scan the image below which was created with this tool.\n\n![Support Wikipedia with 10 €](img/create_qr.gif "Support Wikipedia with 10 €")\n\n![Support Wikipedia with 10 €](img/qr_wikimedia.png "Support Wikipedia with 10 €")\n\n[The created QR code complies with the European Payments Council (EPC) Quick Response (QR) code guidelines.](https://en.wikipedia.org/wiki/EPC_QR_code)\n\n**1st Disclaimer**: The author of this code has no affiliation with the EPC whatsoever.\nHenceforth, you are welcome to use the code at your own dispense, but any use is at your own (commercial) risk.\n\n**2nd Disclaimer**: Currently, the EPC specifications are implemented only to work with IBAN-based consumer wire transfers within the European Economic Area (EEA), i.e. using the following pieces of information:\n\n- Recipient\n- IBAN\n- Amount\n- Unstructured remittance (aka reason for transfer)\n\nOf course, any helping hand is welcome to extend the core functionality to more generic transactions.\n\n## Installation\n\nTo use the code as a standalone command line interface (CLI) tool, then use [`pipx`](https://pypa.github.io/pipx/) as follows\n\n```bash\npipx install py-epc-qr\n```\n\nYou may verify the installation by calling `epcqr version`.\nThe output should be identical to what `pipx` printed.\n\nIf you intend to use the code instead directly in your own Python projects, then install the package using `pip`\n\n```bash\npip install py-epc-qr\n```\n\n\n## Usage\n\nYou may use the package as a standalone command line interface (CLI) or as part of your own code.\n\n### CLI\n\nHaving installed the package with `pipx` (see [above](#installation)), you may verify the installation upon calling\n\n```bash\n>> epcqr --help\nUsage: epcqr [OPTIONS] COMMAND [ARGS]...\n\n  Create EPC-compliant QR codes for wire transfers.\n\nOptions:\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n  --help                          Show this message and exit.\n\nCommands:\n  create   Create EPC-compliant QR code for IBAN-based wire transfer...\n  version  Show version and exit.\n```\n\nThe last lines show the available commands.\n\nThe core functionality lies behind `create`, for which you can call again the `help`.\n\n```bash\nepcqr create --help     \nUsage: epcqr create [OPTIONS]\n\n  Create EPC-compliant QR code for IBAN-based wire transfer within European\n  economic area.\n\nOptions:\n  --out TEXT        name of generated qr png file  [default: qr.png]\n  --from-yaml TEXT  specify yaml file from which to create qr\n  --help            Show this message and exit.\n```\n\n#### From interaction\n\nIf you call the `create` command without any options, it is started in an interactive mode.\nYou are asked to input all relevant information.\nIf your input is correct, an image will be created in your current directory.\n\n#### From template\n\nAlternatively, you can create the QR code from a `yaml` template, [for which the repository contains an example](template.yaml).\n\n### Code\n\nIf you intend to use the source code in your own Python projects, then a minimal working example looks as follows:\n\n```python\nfrom py_epc_qr.transaction import consumer_epc_qr\nepc_qr = consumer_epc_qr(\n    beneficiary= "Wikimedia Foerdergesellschaft",\n    iban= "DE33100205000001194700",\n    amount= 123.45,\n    remittance= "Spende fuer Wikipedia"\n    )\nepc_qr.to_qr()\n```\n\nThe relevant functions are gathered in [`transaction.py`](py_epc_qr/transaction.py)\n\n',
    'author': 'timueh',
    'author_email': 't.muehlpfordt@mailbox.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/timueh/py-epc-qr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
