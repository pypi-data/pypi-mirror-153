import click
from ecli.lib.dictutils import DictUtils
from ecli.lib.plugin.metadata import PluginMetadata
from ecli.lib.plugin.finder import PluginFinder
try:
    # Python 2
    from future_builtins import filter
except ImportError:
    # Python 3
    pass
import logging
from ecli.lib.logger import Logger
from ecli.lib.proc import local_invocation
import os
from ecli.lib.shell import shell_map
import sys
if sys.platform == 'win32':
    from ecli.lib.cryptography.wincred import GetGenericCredential

# Setup Logging
logger = Logger().init_logger(__name__)
# Get This Package's name
package_name = __package__.split('.')[0]

class Plugins:

    def __init__(self, application_path, **kwargs):
        self.PluginMetadata = PluginMetadata()
        self.LocalCliInvocation = local_invocation.CliInvocation()
        self.logger = logger
        PluginsDirName = kwargs.get('PluginsDirName','plugins')
        plugins_from_config = kwargs.get('PluginsFromConfig','plugins')
        # Determine plugin paths
        user_home = os.path.expanduser("~")
        user_plugin_path = os.path.join(user_home, '.ecli', 'plugins')
        if os.path.isdir(user_plugin_path):
            user_plugins = [os.path.join(user_plugin_path, l) for l in os.listdir(user_plugin_path) if os.path.isdir(os.path.join(user_plugin_path, l))]
        else:
            user_plugins = []
        self.plugin_paths = [
            '/etc/%s' % PluginsDirName,
            os.path.join(application_path, 'local', PluginsDirName),
            os.path.join(application_path, PluginsDirName),
            './%s' % PluginsDirName,
        ] + user_plugins + plugins_from_config
        self.PluginFinder = PluginFinder()
        self.DictUtils = DictUtils()  

    def add_plugin(self, func, **kwargs):
        """Adds provided executables spec as available cli commands"""
        cmd_name = kwargs['cmd_name']
        cmd_file_path = kwargs['cmd_file_path']
        cmdDocstring = kwargs.get('cmd_metadata', {}).get('docstring')
        cmdFileExt = kwargs['cmdFileExt']
        cmd_type = kwargs['cmd_type']
        cmd_invocation = kwargs.get('cmd_metadata', {}).get('invocation')
        cmd_is_interactive = kwargs.get('cmd_metadata',{}).get('interactive')
        debug_on = self.logger.level == logging.DEBUG
        env_variables = kwargs.get('env_variables', {})
        plugin_dir_prefix = kwargs.get('plugin_dir_prefix', '')
        def dec(obj):
            if cmd_type == 'command':
                @obj.command(name=cmd_name, context_settings=dict(
                    ignore_unknown_options=True,
                    help_option_names=['---help']
                ))
                @self.PluginMetadata.docstring_parameter(cmdDocstring)
                @click.argument('cmd_args', nargs=-1, type=click.UNPROCESSED)
                @click.option('--use-cred-mgr', is_flag=True,
                    help="Retrieve corresponding script username/password from OS Credential Manager\nExpects entry in credential manager for '%s'\nNote: This must be a Generic Credential\nfor Windows Hosts" % cmd_name)
                def exec_plugin(cmd_args, **kwargs):
                    '''{0}'''
                    extra_args = kwargs.get('extra_arguments', [])
                    args = list(cmd_args) + extra_args
                    shell_env_variables = shell_map[cmdFileExt].get('env_variables', {})
                    modified_env_variables = self.DictUtils.Merge(env_variables, shell_env_variables)
                    cmd_spec = cmd_file_path
                    if kwargs.get('use_cred_mgr'):
                        if sys.platform == 'win32':
                            try:
                                username, password = GetGenericCredential(cmd_name)
                                if not username:
                                    self.logger.warning('No value for Username found in the credential entry for %s' % cmd_name)
                                elif not password:
                                    logger.warning('No value for Password found in the credential entry for %s' % cmd_name)
                                modified_env_variables['username'] = username
                                modified_env_variables['password'] = password
                            except OSError as e:
                                self.logger.warning("Error retrieving '%s' entry in OS credential manager, error was %s" % (cmd_name, e))
                        else:
                            logger.warning('This feature is no yet supported on this platform (%s)' % sys.platform)
                    self.LocalCliInvocation.call(
                        cmd_spec = cmd_spec, 
                        cmd_args = args,
                        cmd_ext = cmdFileExt,
                        invocation = cmd_invocation,
                        interactive = cmd_is_interactive,
                        env_variables = modified_env_variables,
                        debug_enabled = debug_on
                        )
            elif cmd_type == 'namespace':
                cmd_prefix = '%s%s.' % (plugin_dir_prefix, cmd_name)
                self.add_plugins(obj, 
                    plugin_paths=[cmd_file_path], 
                    plugin_prefix=cmd_prefix,
                    debug_on=debug_on
                    )
            return obj
        return dec(func)

    def add_plugins_from_path(self, func, **kwargs):
        
        # Find and add executables in $PATH matching pattern '^ecli-.*' (default)
        default_filter = "^%s-(?!script.py)(.*)$" % package_name
        plugin_file_filter = kwargs.get('plugin_file_filter', default_filter)
        plugin_dir_filter = kwargs.get('plugin_dir_filter', default_filter)
        debug_on = self.logger.level == logging.DEBUG
        for cmd_name, plugin_dir_prefix, cmd_file_path, cmd_ext, cmd_type, cmd_metadata in self.PluginFinder.find_executables(
          file_pattern=plugin_file_filter, 
          dir_pattern=plugin_dir_filter,           
          ):
            self.add_plugin(func,
                cmd_name=cmd_name, 
                cmd_file_path=cmd_file_path, 
                cmdFileExt=cmd_ext,
                cmd_type=cmd_type,
                cmd_metadata=cmd_metadata,
                debug_on=debug_on
                )      
        return func

    def add_plugins(self, func, **kwargs):
        # Find and add executables in local plugins directory matching pattern
        plugin_file_filter = kwargs.get('plugin_file_filter', "(.*)")
        # Don't search through .git folders
        plugin_dir_filter = kwargs.get('plugin_dir_filter', "^((?!\\.git).)*$")
        plugin_paths = kwargs.get('plugin_paths', [])
        debug_on = self.logger.level == logging.DEBUG
        plugin_prefix = kwargs.get('plugin_prefix', '')
        for plugin_path in plugin_paths:
            # print('plugin path: %s' % plugin_path)
            # sys.exit()
            for cmd_name, plugin_dir_prefix, cmd_file_path, cmd_ext, cmd_type, cmd_metadata in self.PluginFinder.find_executables(
                file_pattern=plugin_file_filter, 
                dir_pattern=plugin_dir_filter, 
                search_paths=[plugin_path],
                plugin_prefix=plugin_prefix):
                func = self.add_plugin(func,
                    cmd_name=cmd_name,
                    plugin_dir_prefix=plugin_dir_prefix,
                    cmd_file_path=cmd_file_path, 
                    cmdFileExt=cmd_ext,
                    cmd_type=cmd_type,
                    cmd_metadata=cmd_metadata,
                    debug_on=debug_on
                    )        
        return func