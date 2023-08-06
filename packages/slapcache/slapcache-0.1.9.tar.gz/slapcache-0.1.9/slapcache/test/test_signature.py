# uncompyle6 version 3.6.5
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Apr  3 2019, 05:39:12) 
# [GCC 8.3.0]
# Embedded file name: /root/slapos.package/slapcache/test/test_signature.py
# Compiled at: 2015-06-10 21:40:55
from slapcache import signature
from slapos.libnetworkcache import NetworkcacheClient
from optparse import Values
import slapos.signature, time, difflib, tempfile, unittest, os
def _fake_call(self, *args, **kw):
  self.last_call = (args, kw)

UPGRADE_KEY = """[debian-default]
repository-list = 
	main = http://ftp.fr.debian.org/debian/ wheezy main
	main-src = http://ftp.fr.debian.org/debian/ wheezy main
	update = http://ftp.fr.debian.org/debian/ wheezy-updates main
	update-src = http://ftp.fr.debian.org/debian/ wheezy-updates main
	slapos = http://download.opensuse.org/repositories/home:/VIFIBnexedi:/branches:/home:/VIFIBnexedi/Debian_7.0/ ./
	re6stnet = http://git.erp5.org/dist/deb ./
key-list = 
	slapos = http://git.erp5.org/gitweb/slapos.package.git/blob_plain/HEAD:/debian-preseed/slapos.openbuildservice.key
	re6st = http://git.erp5.org/gitweb/slapos.package.git/blob_plain/HEAD:/debian-preseed/git.erp5.org.key
filter-package-list = 
	ntp
	openvpn
	slapos.node
	re6stnet
filter-promise-list = 
	core
signature-list = 
	debian+++jessie/sid+++
	debian+++7.4+++
	debian+++7.5+++
	debian+++7.3+++
	debian+++7+++

[opensuse-legacy]
repository-list = 
	suse = http://download.opensuse.org/distribution/12.1/repo/oss/
	slapos = http://download.opensuse.org/repositories/home:/VIFIBnexedi:/branches:/home:/VIFIBnexedi/openSUSE_12.1/
	re6st = http://git.erp5.org/dist/rpm
key-list = 
filter-promise-list = 
	core
filter-package-list = 
	ntp
	openvpn
	slapos.node
	re6stnet
signature-list = 
	opensuse+++12.1+++x86_64

[system]
reboot = 2011-10-10
upgrade = 2014-06-04

"""


UPGRADE_KEY_WITHOUT_KEY_LIST = """[debian-default]
repository-list = 
	main = http://ftp.fr.debian.org/debian/ wheezy main
	main-src = http://ftp.fr.debian.org/debian/ wheezy main
	update = http://ftp.fr.debian.org/debian/ wheezy-updates main
	update-src = http://ftp.fr.debian.org/debian/ wheezy-updates main
	slapos = http://download.opensuse.org/repositories/home:/VIFIBnexedi:/branches:/home:/VIFIBnexedi/Debian_7.0/ ./
	re6stnet = http://git.erp5.org/dist/deb ./
filter-package-list = 
	ntp
	openvpn
	slapos.node
	re6stnet
filter-promise-list = 
	core
signature-list = 
	debian+++jessie/sid+++
	debian+++7.4+++
	debian+++7.5+++
	debian+++7.3+++
	debian+++7+++

[opensuse-legacy]
repository-list = 
	suse = http://download.opensuse.org/distribution/12.1/repo/oss/
	slapos = http://download.opensuse.org/repositories/home:/VIFIBnexedi:/branches:/home:/VIFIBnexedi/openSUSE_12.1/
	re6st = http://git.erp5.org/dist/rpm
filter-promise-list = 
	core
filter-package-list = 
	ntp
	openvpn
	slapos.node
	re6stnet
signature-list = 
	opensuse+++12.1+++x86_64

[system]
reboot = 2011-10-10
upgrade = 2014-06-04

"""


SIGNATURE = """-----BEGIN CERTIFICATE-----
MIIB8DCCAVmgAwIBAgIJAPFf61p8y809MA0GCSqGSIb3DQEBBQUAMBAxDjAMBgNV
BAMMBUNPTVAtMCAXDTE0MDIxNzE2NDgxN1oYDzIxMTQwMTI0MTY0ODE3WjAQMQ4w
DAYDVQQDDAVDT01QLTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAsiqCyuv1
HO9FmtwnMbEa1/u8Dn7T0k7hVKYXVQYof+59Ltbb3cA3nLjFSJDr/wQT6N89MccS
PneRzkWqZKL06Kmj+N+XJfRyVaTz1qQtNzjdbYkO6RgQq+fvq2CO0+PSnL6NttLU
/a9nQMcVm7wZ8kmY+AG5LbVo8lmxDD16Wq0CAwEAAaNQME4wHQYDVR0OBBYEFEVi
YyWHF3W7/O4NaTjn4lElLpp7MB8GA1UdIwQYMBaAFEViYyWHF3W7/O4NaTjn4lEl
Lpp7MAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQEFBQADgYEAgIPGoxhUa16AgjZx
Jr1kUrs8Fg3ig8eRFQlBSLYfANIUxcQ2ScFAkmsvwXY3Md7uaSvMJsEl2jcjdmdi
eSreNkx85j9GtMLY/2cv0kF4yAQNRtibtDkbg6fRNkmUopDosJNVf79l1GKX8JFL
zZBOFdOaLYY/6dLRwiTUKHU6su8=
-----END CERTIFICATE-----"""
BASE_UPDATE_CFG_DATA = """

[networkcache]
download-binary-cache-url = http://www.shacache.org/shacache
download-cache-url = https://www.shacache.org/shacache
download-binary-dir-url = http://www.shacache.org/shadir
"""
UPDATE_CFG_DATA = """
[shacache]
key = slapos-upgrade-testing-key-with-config-file-invalid

""" + BASE_UPDATE_CFG_DATA
UPDATE_UPLOAD_CFG_DATA = """
[shacache]
key = slapos-upgrade-testing-key-with-config-file

""" + BASE_UPDATE_CFG_DATA
VALID_UPDATE_CFG_DATA = """
[shacache]
key = 'slapos-upgrade-testing-key-with-config-file-valid' 

""" + BASE_UPDATE_CFG_DATA
UPDATE_CFG_WITH_UPLOAD_DATA = UPDATE_CFG_DATA + """
signature-private-key-file = /etc/opt/slapos/signature.key
upload-cache-url = https://www.shacache.org/shacache
shacache-cert-file = /etc/opt/slapos/shacache.crt
shacache-key-file = /etc/opt/slapos/shacache.key
upload-dir-url = https://www.shacache.org/shadir
shadir-cert-file = /etc/opt/slapos/shacache.crt
shadir-key-file = /etc/opt/slapos/shacache.key
"""

def _fake_upload(self, *args, **kwargs):
    return True


class NetworkCacheTestCase(unittest.TestCase):

    def setUp(self):
        self.original_networkcache_upload = NetworkcacheClient.upload
        NetworkcacheClient.upload = _fake_upload
        self.config_dict = {'slapos_configuration': self._createConfigurationFile(), 
           'srv_file': '/tmp/test_base_promise_slapupdate', 
           'dry_run': False, 
           'verbose': False}

    def tearDown(self):
        NetworkcacheClient.upload = self.original_networkcache_upload

    def _createConfigurationFile(self):
        with open('/tmp/test_signature_000000_configuration.cfg', 'w') as (configuration_file):
            configuration_file.write(VALID_UPDATE_CFG_DATA)
        return '/tmp/test_signature_000000_configuration.cfg'

    def test_basic_configuration(self):
        info, self.configuration_file_path = tempfile.mkstemp()
        configuration_content = UPDATE_CFG_DATA + """
signature-certificate-list = %(certificate)s
""" % {'certificate': '\n'.join('  ' + l if l.strip() else '\n' for l in SIGNATURE.splitlines())}
        print(configuration_content)
        open(self.configuration_file_path, 'w').write(configuration_content)
        shacache = signature.NetworkCache(self.configuration_file_path)
        self.assertEqual(shacache.download_binary_cache_url, 'http://www.shacache.org/shacache')
        self.assertEqual(shacache.download_cache_url, 'https://www.shacache.org/shacache')
        self.assertEqual(shacache.download_binary_dir_url, 'http://www.shacache.org/shadir')
        self.assertEqual(shacache.signature_certificate_list, SIGNATURE)
        self.assertEqual(shacache.directory_key, 'slapos-upgrade-testing-key-with-config-file-invalid')
        self.assertEqual(shacache.dir_url, None)
        self.assertEqual(shacache.cache_url, None)
        self.assertEqual(shacache.signature_private_key_file, None)
        self.assertEqual(shacache.shacache_cert_file, None)
        self.assertEqual(shacache.shacache_key_file, None)
        self.assertEqual(shacache.shadir_cert_file, None)
        self.assertEqual(shacache.shadir_key_file, None)
        return

    def test_basic_configuration_with_upload(self):
        info, self.configuration_file_path = tempfile.mkstemp()
        configuration_content = UPDATE_CFG_WITH_UPLOAD_DATA + """
signature-certificate-list = %(certificate)s
""" % {'certificate': '\n'.join('  ' + l if l.strip() else '\n' for l in SIGNATURE.splitlines())}
        open(self.configuration_file_path, 'w').write(configuration_content)
        shacache = signature.NetworkCache(self.configuration_file_path)
        self.assertEqual(shacache.download_binary_cache_url, 'http://www.shacache.org/shacache')
        self.assertEqual(shacache.download_cache_url, 'https://www.shacache.org/shacache')
        self.assertEqual(shacache.download_binary_dir_url, 'http://www.shacache.org/shadir')
        self.assertEqual(shacache.signature_certificate_list, SIGNATURE)
        self.assertEqual(shacache.directory_key, 'slapos-upgrade-testing-key-with-config-file-invalid')
        self.assertEqual(shacache.dir_url, 'https://www.shacache.org/shadir')
        self.assertEqual(shacache.cache_url, 'https://www.shacache.org/shacache')
        self.assertEqual(shacache.shacache_cert_file, '/etc/opt/slapos/shacache.crt')
        self.assertEqual(shacache.shacache_key_file, '/etc/opt/slapos/shacache.key')
        self.assertEqual(shacache.shadir_cert_file, '/etc/opt/slapos/shacache.crt')
        self.assertEqual(shacache.shadir_key_file, '/etc/opt/slapos/shacache.key')
        self.assertEqual(shacache.signature_private_key_file, '/etc/opt/slapos/signature.key')

    def test_configuration_file_dont_exist(self):
        self.assertRaises(ValueError, signature.NetworkCache, '/abc/123')

    def test_download_not_existing_signature_from_cache(self):
        info, path = tempfile.mkstemp()
        info, self.configuration_file_path = tempfile.mkstemp()
        open(self.configuration_file_path, 'w').write(UPDATE_CFG_DATA)
        shacache = signature.NetworkCache(self.configuration_file_path)
        self.assertEqual(False, shacache.download(path=path, required_key_list=['timestamp'], strategy=signature.strategy))
        self.assertEqual('', open(path, 'r').read())

    def test_download_existing_from_cache(self):
        info, path = tempfile.mkstemp()
        info, self.configuration_file_path = tempfile.mkstemp()
        open(self.configuration_file_path, 'w').write(VALID_UPDATE_CFG_DATA)
        shacache = signature.NetworkCache(self.configuration_file_path)
        shacache.download(path=path, required_key_list=[
         'timestamp'], strategy=signature.strategy)
        self.maxDiff = None
        self.assertEqual(UPGRADE_KEY.splitlines(), open(path, 'r').read().splitlines())
        return

    def test_upload_to_cache(self):
        info, path = tempfile.mkstemp()
        info, _fake_signature_path = tempfile.mkstemp()
        info, self.configuration_file_path = tempfile.mkstemp()
        signature_certificate_file = '/tmp/signature_certificate_file_demo_test'
        if os.path.exists(signature_certificate_file):
            os.remove(signature_certificate_file)
        signature_private_key_file = '/tmp/signature_private_key_file_demo_test'
        if os.path.exists(signature_private_key_file):
            os.remove(signature_private_key_file)
        slapos.signature.generateCertificate(signature_certificate_file, signature_private_key_file, 'COMP-123A')
        configuration_content = UPDATE_UPLOAD_CFG_DATA + """
signature-private-key-file = %(signature_private_key_file)s
upload-cache-url = https://www.shacache.org/shacache
shacache-cert-file = %(tempfile)s
shacache-key-file = %(tempfile)s
upload-dir-url = https://www.shacache.org/shadir
shadir-cert-file = %(tempfile)s
shadir-key-file = %(tempfile)s
signature-certificate-list =
  %(certificate)s
""" % {
        'tempfile': _fake_signature_path,
        'signature_private_key_file': signature_private_key_file,
        'certificate': ''.join('  ' + l if l.strip() else '\n' for l in open(signature_certificate_file, 'r').readlines())
        }
        open(self.configuration_file_path, 'w').write(configuration_content)
        open(_fake_signature_path, 'w').write('# XXX ...')
        shacache = signature.NetworkCache(self.configuration_file_path)
        metadata_dict = {'timestamp': time.time()}
        shacache.upload(path=path, metadata_dict=metadata_dict)

    def test_signature_strategy(self):
        entry_list = [{'timestamp': 123824.0}, {'timestamp': 12345.0}, {'timestamp': 13345.0}, {'timestamp': 12344.0}, {'timestamp': 12045.0}]
        self.assertEqual(signature.strategy(entry_list), {'timestamp': 123824.0})
# okay decompiling slapcache/test/test_signature.pyc
