# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2012-2014 Vifib SARL and Contributors.
# All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from six.moves import configparser
import os
import time
import traceback
import tempfile
import datetime
import shutil
import hashlib
import base64
from random import choice
from string import ascii_lowercase

from slapos.libnetworkcache import NetworkcacheClient
from slapos.networkcachehelper import helper_download_network_cached


class NetworkCache:
  def __init__(self, configuration_path):
    if not os.path.exists(configuration_path):
      raise ValueError("You need configuration file")
    self.configuration = configuration_path
    self._load()
 
  def _load(self):
    network_cache_info = configparser.RawConfigParser()
    network_cache_info.read(self.configuration)
    network_cache_info_dict = dict(network_cache_info.items('networkcache'))
    def get_(name):
      return network_cache_info_dict.get(name)

    self.download_binary_cache_url = get_('download-binary-cache-url')
    self.download_cache_url = get_('download-cache-url')
    self.download_binary_dir_url = get_('download-binary-dir-url')
    self.signature_certificate_list = get_('signature-certificate-list')

    # Not mandatory
    self.dir_url = get_('upload-dir-url')
    self.cache_url = get_('upload-cache-url')
    key_file_key = 'signature-private-key-file'
    self.signature_private_key_file = get_(key_file_key)
    key_file_old_key = 'signature_private_key_file'
    if key_file_old_key in network_cache_info_dict:
      raise ValueError(
        '%s is not supported anymore, use %s' % (key_file_old_key, key_file_key))
    self.shacache_ca_file = get_('shacache-ca-file')
    self.shacache_cert_file = get_('shacache-cert-file')
    self.shacache_key_file = get_('shacache-key-file')
    self.shadir_cert_file = get_('shadir-cert-file')
    self.shadir_key_file = get_('shadir-key-file')
    self.shadir_ca_file = get_('shadir-ca-file')

    if network_cache_info.has_section('shacache'):
      self.directory_key = network_cache_info.get('shacache', 'key')
    else:
      self.directory_key = "slapos-upgrade-testing-key"

  def upload(self, path, metadata_dict, is_sha256file=False):
    """
    Upload an existing file, using a file_descriptor.
    """
    if is_sha256file: 
      key = self.directory_key + "-sha256-content"
    else:
      key = self.directory_key

    file_descriptor = open(path, 'rb')
    if not (self.dir_url and self.cache_url):
      raise ValueError("upload-dir-url and/or upload-cache-url is not defined")

    # backward compatibility
    metadata_dict.setdefault('file', 'notused')
    metadata_dict.setdefault('urlmd5', 'notused')

    # convert '' into None in order to call nc nicely
    with NetworkcacheClient(self.cache_url, self.dir_url,
          signature_private_key_file=self.signature_private_key_file or None,
          signature_certificate_list=self.signature_certificate_list or None,
          shacache_ca_file=self.shacache_ca_file or None,
          shacache_cert_file=self.shacache_cert_file or None,
          shacache_key_file=self.shacache_key_file or None,
          shadir_cert_file=self.shadir_cert_file or None,
          shadir_key_file=self.shadir_key_file or None,
          shadir_ca_file=self.shadir_ca_file or None,

        ) as nc:
      return nc.upload(file_descriptor, key, **metadata_dict)


  def download(self, path, wanted_metadata_dict={}, 
                 required_key_list=[], strategy=None, is_sha256file=False):

    if is_sha256file:
      key = self.directory_key + "-sha256-content"
    else:
      key = self.directory_key

    result = helper_download_network_cached(
              self.download_binary_dir_url, 
              self.download_binary_cache_url,
              self.signature_certificate_list,
              key, wanted_metadata_dict, 
              required_key_list, strategy)

    if result:
      # XXX check if nc filters signature_certificate_list!
      # Creates a file with content to desired path.
      file_descriptor, metadata_dict = result
      f = open(path, 'w+b')
      try:
        shutil.copyfileobj(file_descriptor, f)
        # XXX method should check MD5.
        return metadata_dict
      finally:
        f.close()
        file_descriptor.close()
    return False



def strategy(entry_list):
  """Get the latest entry. """
  timestamp = 0
  best_entry = None
  for entry in entry_list:
    if entry['timestamp'] > timestamp:
      best_entry = entry
      timestamp = entry['timestamp']

  return best_entry 

class Signature:

  def __init__(self, config, logger=None):
    self.config = config
    self.logger = logger

  def log(self, message, *args):
    if self.logger is not None:
      self.logger.debug(message, *args)
    elif args:
      print(message % args)
    else:
      print(message)

  def get_file_hash(self, path):
    with open(path, 'rb') as f:
      h = hashlib.sha256()
      h.update(f.read())
      base = base64.b64encode(h.digest())
    return base

  def save_file_hash(self, path, destination):
    base = self.get_file_hash(path) 
    with open(destination, "wb") as f:
      f.write(base)

  def _download(self, path):
    """
    Download a tar of the repository from cache, and untar it.
    """
    shacache = NetworkCache(self.config.slapos_configuration)

    if shacache.signature_certificate_list is None:
      raise ValueError("You need at least one valid signature for download")

    download_metadata_dict = shacache.download(path=path, 
           required_key_list=['timestamp'], strategy=strategy)

    if download_metadata_dict:
      self.log('File downloaded in %s', path)
      current_sha256 = self.get_file_hash(path)
      with tempfile.NamedTemporaryFile() as f_256:
        sha256path = f_256.name
        if shacache.download(path=sha256path, required_key_list=['timestamp'],
                              strategy=strategy, is_sha256file=True):
          self.log('sha 256 downloaded in %s', sha256path)
          expected_sha256 = f_256.read()

          if current_sha256 == expected_sha256:
            return True
          else:
            raise ValueError("%s != %s" % (current_sha256, expected_sha256))

  def download(self):
    """
    Get status information and return its path
    """
    info, path = tempfile.mkstemp()
    if self._download(path):
      try:
        shutil.move(path, self.config.destination)
      except Exception as e:
        self.log(e)
        self.log('Fail to move %s to %s, maybe permission problem?', path, self.config.destination)
        os.remove(path)
    else:
      os.remove(path)
      raise ValueError("No result from shacache")

  def _upload(self, path):
    """
    Creates uploads repository to cache.
    """
    shacache = NetworkCache(self.config.slapos_configuration)

    sha256path = path + ".sha256"
    self.save_file_hash(path, sha256path)
 
    metadata_dict = {
      # XXX: we set date from client side. It can be potentially dangerous
      # as it can be badly configured.
      'timestamp': time.time(),
      'token': ''.join([choice(ascii_lowercase) for _ in range(128)]) 
    }
    try:
      sha512sum = shacache.upload(path=path, metadata_dict=metadata_dict)
      if sha512sum:
        self.log(
          'Uploaded %s to cache (using %s key) with SHA512 %s.', path,
          shacache.directory_key, sha512sum)
        sha512sum_path = shacache.upload(
          path=sha256path, metadata_dict=metadata_dict, is_sha256file=True)
        if sha512sum_path:
          self.log(
            'Uploaded %s to cache (using %s key) with SHA512 %s.', sha256path,
            shacache.directory_key, sha512sum_path)
        else:
          self.log('Fail to upload sha256file file to cache.')
      else:
        self.log('Fail to upload %s to cache.', path)
    except Exception:
      self.log('Unable to upload to cache:\n%s.', traceback.format_exc())
      return

  def upload(self):
    self._upload(self.config.file)
 
# Class containing all parameters needed for configuration
class Config:
  def __init__(self, option_dict=None):
    if option_dict is not None:
      # Set options parameters
      for option, value in option_dict.__dict__.items():
        setattr(self, option, value)

