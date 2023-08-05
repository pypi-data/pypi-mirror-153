from ecli.lib.logger import Logger
from ecli.lib.shell import shell_map, shell_exts

# Setup Logging

logger = Logger().init_logger(__name__)

class PluginMetadata:

    def __init__(self):
        self.package_name = __package__.split('.')[0]
        self.DefaultDocString = "Generic executable (try running {p} {n} ---help)"
        self.logger = logger

    def get_metadata(self, filepath, name, cmd_ext, cmd_type):
        
        docstring = self.DefaultDocString.format(p=self.package_name, n=name)
        plugin_invocation = 'standard'
        plugin_is_interactive = False
        metadata = (docstring, plugin_invocation)
        docstring_match = []
        invocation_match = []
        interactive_match = []

        if cmd_ext in shell_exts:
          try:
              with open(filepath, 'r') as f:
                  content = ''.join(f.readlines())
                  docstring_match = shell_map[cmd_ext]['docstring_search'].findall(content)
                  invocation_match = shell_map[cmd_ext]['invocation_search'].findall(content)
                  interactive_match = shell_map[cmd_ext]['interactive_search'].findall(content)
          except Exception as err:
              self.logger.debug('Reading command file failed with error: {}'.format(err))
              pass

          if len(docstring_match) > 0:
              docstring = docstring_match[0]
          if len(invocation_match) > 0:
              plugin_invocation = invocation_match[0]
          if len(interactive_match) > 0:
              plugin_is_interactive = interactive_match[0]

          metadata = {
            'docstring': docstring, 
            'invocation': plugin_invocation, 
            'interactive': plugin_is_interactive
          }

          self.logger.debug('{n} metadata: {m}'.format(n=name, m=metadata))

        return metadata

    def docstring_parameter(self, *sub):
        def dec(obj):
            obj.__doc__ = obj.__doc__.format(*sub)
            return obj
        return dec        