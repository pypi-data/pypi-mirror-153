import os
import sys
from setuptools import setup, find_packages
from fnmatch import fnmatchcase
from distutils.util import convert_path

standard_exclude = ('*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')
def find_package_data(where='.', package='', exclude=standard_exclude, exclude_directories=standard_exclude_directories):
    out = {}
    stack = [(convert_path(where), '', package)]
    while stack:
        where, prefix, package = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                        stack.append((fn, '', new_package))
                else:
                    stack.append((fn, prefix + name + '/', package))
            else:
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out

setup(name='docassemble.cladmin',
      version='0.0.1',
      description=('A docassemble extension containing Chat Legal admin documents.'),
      long_description='Chat Legal documents',
      long_description_content_type='text/markdown',
      author='System Administrator',
      author_email='dqyhii9@gmail.com',
      license='The MIT License (MIT)',
      url='https://docassemble.org',
      packages=find_packages(),
      namespace_packages=['docassemble'],
      install_requires=['3to2>=1.1.1', 'Babel>=2.9.1', 'CairoSVG>=2.5.2', 'ConfigArgParse>=1.5.3', 'Deprecated>=1.2.13', 'Docassemble-Flask-User>=0.6.26', 'Docassemble-Pattern>=3.6.5', 'Flask>=2.1.1', 'Flask-Babel>=2.0.0', 'Flask-Cors>=3.0.10', 'Flask-Login>=0.6.0', 'Flask-Mail>=0.9.1', 'Flask-SQLAlchemy>=2.5.1', 'Flask-SocketIO>=5.1.1', 'Flask-WTF>=1.0.1', 'Hyphenate>=1.1.0', 'Jinja2>=3.1.1', 'Mako>=1.2.0', 'Markdown>=3.3.6', 'MarkupSafe>=2.1.1', 'Pillow>=9.1.0', 'PyJWT>=2.3.0', 'PyLaTeX>=1.4.1', 'PyNaCl>=1.5.0', 'PyPDF2>=1.27.5', 'PySocks>=1.7.1', 'PyYAML>=5.1.2', 'Pygments>=2.0.2', 'SQLAlchemy>=0.6.9', 'SecretStorage>=3.3.1', 'SocksiPy-branch>=1.01', 'WTForms>=3.0.1', 'Werkzeug>=2.1.1', 'XlsxWriter>=3.0.3', 'acme>=1.26.0', 'airtable-python-wrapper>=0.15.3', 'alembic>=0.1.1', 'aloe>=0.2.0', 'amqp>=5.1.0', 'ansicolors>=1.1.8', 'asn1crypto>=1.5.1', 'astunparse>=1.6.3', 'async-generator>=1.10', 'async-timeout>=4.0.2', 'atomicwrites>=1.4.0', 'attrs>=21.4.0', 'azure-common>=1.1.28', 'azure-core>=1.23.1', 'azure-identity>=1.9.0', 'azure-keyvault-secrets>=4.4.0', 'azure-nspkg>=3.0.2', 'azure-storage-blob>=12.11.0', 'backports.zoneinfo>=0.2.1', 'bcrypt>=3.2.0', 'beautifulsoup4>=4.11.1', 'bidict>=0.22.0', 'billiard>=3.6.4.0', 'bleach>=5.0.0', 'blinker>=1.4', 'boto>=2.49.0', 'boto3>=1.21.40', 'botocore>=1.24.40', 'cachetools>=5.0.0', 'cairocffi>=1.3.0', 'celery>=5.2.6', 'certbot>=1.15.0', 'certbot-apache>=1.15.0', 'certbot-nginx>=1.15.0', 'certifi>=2021.10.8', 'cffi>=1.15.0', 'chardet>=4.0.0', 'charset-normalizer>=0.1.8', 'click>=8.1.2', 'click-didyoumean>=0.3.0', 'click-plugins>=1.1.1', 'click-repl>=0.2.0', 'clicksend-client>=5.0.72', 'colorama>=0.4.4', 'commonmark>=0.9.1', 'configobj>=5.0.6', 'configparser>=5.2.0', 'convertapi>=1.4.0', 'crayons>=0.4.0', 'cryptography>=36.0.2', 'cssselect2>=0.5.0', 'da-pkg-resources>=0.0.1', 'defusedxml>=0.7.1', 'distro>=1.7.0', 'dnspython>=2.2.1', 'docassemble-textstat>=0.7.2', 'docassemble.cldiscretionarytrust', 'docassemble.demo>=1.3.38', 'docassemble.discretionarytrust', 'docassemble.estateplanning', 'docassemble.frontpage', 'docassemble.hhdocuments', 'docassemblekvsession>=0.7', 'docopt>=0.6.2', 'docutils>=0.17.1b1.dev0', 'docxcompose>=1.3.4', 'docxtpl>=0.15.2', 'email-validator>=1.1.3', 'et-xmlfile>=1.1.0', 'eventlet>=0.33.0', 'future>=0.18.2', 'gcs-oauth2-boto-plugin>=3.0', 'geographiclib>=1.52', 'geopy>=2.2.0', 'gherkin-official>=4.1.3', 'google-api-core>=2.7.2', 'google-api-python-client>=2.44.0', 'google-auth>=2.6.4', 'google-auth-httplib2>=0.1.0', 'google-auth-oauthlib>=0.5.1', 'google-cloud-core>=2.3.0', 'google-cloud-storage>=2.3.0', 'google-cloud-translate>=3.7.2', 'google-cloud-vision>=2.7.2', 'google-crc32c>=1.3.0', 'google-i18n-address>=2.5.0', 'google-reauth>=0.1.1', 'google-resumable-media>=2.3.2', 'googleapis-common-protos>=1.56.0', 'googledrivedownloader>=0.4', 'greenlet>=1.0.0', 'grpcio>=1.44.0', 'grpcio-status>=1.44.0', 'gspread>=5.3.2', 'guess-language-spirit>=0.5.3', 'h11>=0.13.0', 'httplib2>=0.20.4', 'humanize>=4.0.0', 'idna>=3.3', 'importlib-metadata>=4.11.3', 'importlib-resources>=5.7.0', 'iniconfig>=1.1.1', 'iso8601>=1.0.2', 'isodate>=0.6.1', 'itsdangerous>=2.1.2', 'jdcal>=1.4.1', 'jeepney>=0.8.0', 'jellyfish>=0.6.1', 'jmespath>=1.0.0', 'joblib>=1.1.0', 'josepy>=1.13.0', 'keyring>=1.2.3', 'kombu>=5.2.4', 'libcst>=0.4.1', 'links-from-link-header>=0.1.0', 'lxml>=1.0.4', 'mdx-smartypants>=1.5.1', 'minio>=7.1.6', 'mod-wsgi>=4.7.1', 'monotonic>=1.6', 'msal>=1.17.0', 'msal-extensions>=0.3.1', 'msrest>=0.6.21', 'mypy-extensions>=0.4.3', 'namedentities>=1.5.2', 'netifaces>=0.11.0', 'nltk>=2.0.5', 'nose>=1.3.7', 'num2words>=0.5.10', 'numpy>=1.0.4', 'oauth2client>=4.1.3', 'oauthlib>=3.2.0', 'openpyxl>=3.0.9', 'ordered-set>=4.1.0', 'outcome>=1.1.0', 'packaging>=21.3', 'pandas>=1.4.2', 'parsedatetime>=2.6', 'passlib>=1.7.4', 'pathlib>=1.0.1', 'pdfminer.six>=20220319', 'phonenumbers>=5.9.2', 'pip>=20.1.1', 'pkginfo>=1.2.1', 'pluggy>=1.0.0', 'ply>=3.11', 'portalocker>=2.4.0', 'prompt-toolkit>=3.0.29', 'proto-plus>=1.20.3', 'protobuf>=3.20.0', 'psutil>=5.9.0', 'psycopg2-binary>=2.9.3', 'py>=1.11.0', 'pyOpenSSL>=22.0.0', 'pyPdf>=1.13', 'pyRFC3339>=1.1', 'pyasn1>=0.4.8', 'pyasn1-modules>=0.2.8', 'pycountry>=22.3.5', 'pycparser>=2.21', 'pycryptodome>=3.14.1', 'pycryptodomex>=3.14.1', 'pycurl>=7.45.1', 'pyotp>=2.6.0', 'pyparsing>=3.0.8', 'pypdftk>=0.5', 'pypng>=0.0.21', 'pytest>=7.1.1', 'python-augeas>=1.1.0', 'python-dateutil>=2.8.2', 'python-docx>=0.8.11', 'python-editor>=1.0.4', 'python-engineio>=4.3.1', 'python-http-client>=3.3.7', 'python-ldap>=3.4.0', 'python-socketio>=5.5.2', 'pytz>=2013.9', 'pytz-deprecation-shim>=0.1.0.post0', 'pyu2f>=0.1.5', 'pyzbar>=0.1.9', 'qrcode>=7.3.1', 'rauth>=0.7.3', 'readme-renderer>=34.0', 'redis>=4.2.2', 'regex>=2022.3.15', 'reportlab>=3.6.9', 'repoze.lru>=0.7', 'requests>=2.27.1', 'requests-oauthlib>=1.3.1', 'requests-toolbelt>=0.9.1', 'retry-decorator>=1.1.1', 'rfc3339>=6.2', 'rfc3986>=2.0.0', 'rich>=12.2.0', 'rsa>=4.7.2', 'ruamel.yaml>=0.17.21', 'ruamel.yaml.clib>=0.2.6', 's3transfer>=0.5.2', 's4cmd>=2.1.0', 'scikit-learn>=0.14.1', 'scipy>=1.8.0', 'selenium>=2.0-dev-9429', 'sendgrid>=6.9.7', 'setuptools>=56.0.0', 'simplekv>=0.14.1', 'six>=1.0.0', 'sklearn>=0.0', 'sniffio>=1.2.0', 'sortedcontainers>=2.4.0', 'soupsieve>=1.0.2', 'starkbank-ecdsa>=2.0.3', 'tailer>=0.4.1', 'telnyx>=1.5.0', 'threadpoolctl>=3.1.0', 'tinycss2>=1.1.1', 'titlecase>=2.3', 'toml>=0.10.2', 'tomli>=2.0.1', 'tqdm>=4.64.0', 'trio>=0.20.0', 'trio-websocket>=0.9.2', 'twilio>=5.0.0', 'twine>=4.0.0', 'typing-extensions>=4.1.1', 'typing-inspect>=0.7.1', 'tzdata>=2022.1', 'tzlocal>=4.0.2', 'uWSGI>=2.0.20', 'ua-parser>=0.10.0', 'uritemplate>=4.1.1', 'urllib3>=1.26.9', 'us>=2.0.2', 'user-agents>=2.2.0', 'vine>=5.0.0', 'wcwidth>=0.2.5', 'webdriver-manager>=3.5.4', 'webencodings>=0.5.1', 'wheel>=0.37.1', 'wrapt>=1.14.0', 'wsproto>=1.1.0', 'xfdfgen>=0.4', 'xlrd>=2.0.1', 'xlwt>=1.3.0', 'zipp>=3.8.0', 'zope.component>=5.0.1', 'zope.event>=4.5.0', 'zope.hookable>=5.1.0', 'zope.interface>=3.3.0.1'],
      zip_safe=False,
      package_data=find_package_data(where='docassemble/cladmin/', package='docassemble.cladmin'),
     )

