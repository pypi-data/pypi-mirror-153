__version__ = "0.0.1"

import logging
import os

import fs
from fs import open_fs

from diff_match_patch import diff_match_patch

logger = logging.getLogger("shadowed")

class FileSystem():
  def __init__(self, real, shadow):
    if not os.path.exists(real):
      os.makedirs(real)
    self.real   = open_fs(str(real))
    if not os.path.exists(shadow):
      os.makedirs(shadow)
    self.shadow = open_fs(str(shadow))

  def create(self, path, content):
    try:
      info = self.real.getinfo(path, namespaces=["basic"])
      if info.is_dir:
        raise ValueError(f"Real path '{path}' isn't a file path.")
      raise ValueError(f"Real file '{path}' exists. Use 'adopt()' to add shadow.")
    except fs.errors.ResourceNotFound:
      pass

    self.real.writetext(path, content)
    logger.debug("created real %s", self.real.desc(path))
    self.shadow.writetext(path, content)
    logger.debug("created shadow %s", self.shadow.desc(path))

  def real_content(self, path):
    return self.real.readtext(path)

  def shadow_content(self, path):
    return self.shadow.readtext(path)

  def adopt(self, path):
    try:
      content = self.real_content(path)
    except fs.errors.ResourceNotFound as resource_not_found:
      raise ValueError(f"Real file '{path} doesn't exist. Use 'create()'.") \
            from resource_not_found

    self.shadow.writetext(path, content)
    logger.debug("created shadow %s", self.shadow.desc(path))

  def is_unchanged(self, path):
    return self.real_content(path) == self.shadow_content(path)

  def was_changed(self, path):
    return not self.is_unchanged(path)

  def update(self, path, content, merge=False):
    if self.was_changed(path):
      if not merge:
        raise ValueError(f"Real file '{path}' was changed and merging is not requested.")
      self.merge(path, content)
    else:
      self.real.writetext(path, content)
      logger.debug("updated real %s", self.real.desc(path))
      self.shadow.writetext(path, content)
      logger.debug("updated shadow %s", self.shadow.desc(path))

  def merge(self, path, new_content):
    current_content  = self.real_content(path)
    previous_content = self.shadow_content(path)

    # detect intended changes and apply them
    dmp                 = diff_match_patch()
    dmp.Match_Threshold = 0.4
    dmp.Match_Distance  = 15
    patches             = dmp.patch_make(previous_content, new_content)

    if patches:
      merged_content, _ = dmp.patch_apply(patches, current_content)

      self.real.writetext(path, merged_content)
      logger.debug("merged real %s", self.real.desc(path))
      self.shadow.writetext(path, new_content)
      logger.debug("updated shadow %s", self.shadow.desc(path))
