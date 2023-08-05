from ecli.lib.plugin.metadata import PluginMetadata
from ecli.lib.shell import shell_exts
import os
import re
import sys

class PluginFinder:

    def __init__(self):
        self.search_paths = os.environ.get('PATH', '').split(os.pathsep)
        self.PluginMetadata = PluginMetadata()
        self.plugin_dir_prefix_pattern = re.compile(
          'ecli.plugins[\W]+?|ecli.plugins'
          )

    def canonical_path(self, filepath):
        realpath = os.path.realpath(os.path.normcase(os.path.expanduser(filepath)))
        normalized_path = realpath.replace('\\', '/')
        return normalized_path

    def walk(self, top, maxdepth):
        dirs, nondirs = [], []
        for name in os.listdir(top):
            (dirs if os.path.isdir(os.path.join(top, name)) else nondirs).append(name)
        yield top, dirs, nondirs
        if maxdepth > 1:
            for name in dirs:
                for x in walk(os.path.join(top, name), maxdepth-1):
                    yield x

    def find_executables(self, **kwargs):
        file_pattern = kwargs.get('file_pattern')
        dir_pattern = kwargs.get('dir_pattern')
        search_paths = kwargs.get('search_paths', self.search_paths)
        filepred = re.compile(dir_pattern).search
        filter_files = lambda files: filter(filepred, files)
        plugin_prefix = kwargs.get('plugin_prefix', '')
        plugin_dir_prefix = kwargs.get('plugin_dir_prefix', '')
        seen = set()
        for dirpath in search_paths:
            if os.path.isdir(dirpath):
                rp = self.canonical_path(dirpath)
                if rp in seen:
                    continue
                seen.add(rp)

                fileobj_names = filter_files(os.listdir(dirpath))

                for fileobj_name in fileobj_names:
                    ext = None
                    fullpath = os.path.join(dirpath, fileobj_name)
                    canonical_path = self.canonical_path(fullpath)
                    if os.path.isdir(canonical_path):
                        plugin_dir_prefix = self.plugin_dir_prefix_pattern.sub(
                          '', os.path.basename(dirpath)
                          )
                        if plugin_dir_prefix:
                          plugin_dir_prefix += '.'
                        name = fileobj_name
                        if name in ['lib']:
                          continue
                        cmd_type = 'namespace'
                        metadata = {}
                    else:
                        cmd = os.path.basename(canonical_path)
                        cmd_type = 'command'
                        matched_name = re.search(file_pattern, cmd).group(1)
                        nameparts = os.path.splitext(matched_name)
                        name = '%s%s' % (plugin_prefix,nameparts[0])
                        name = name.replace('..','.')
                        ext = nameparts[1] if len(nameparts) > 1 else ext
                        if not ext in shell_exts:
                            continue
                        metadata = self.PluginMetadata.get_metadata(canonical_path, name, ext, cmd_type)
                    yield (name, plugin_dir_prefix, canonical_path, ext, cmd_type, metadata)