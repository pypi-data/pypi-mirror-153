from pkg_resources import iter_entry_points
import click
from click_plugins import with_plugins
from ecli.lib.defaults import default_config
import getpass
import logging
import os
import sys
from ecli.lib.logger import Logger
from ecli.lib.options.mexclusive import MutuallyExclusiveOption
from ecli.lib.plugin import plugins
from ecli.lib.input.streams import Streams
from ecli.lib.dictutils import Struct
from bertdotconfig import Config
from ecli.lib.dictutils import DictUtils

# Private variables
__author__ = 'Bert Tejeda'
__version__ = '1.4.4'
# Configuration Files
config_file_name = 'ecli.config.yaml'
# Initialize App Config
config = Config(
    config_file_uri=config_file_name,
    default_value=default_config
).read()
# Dictutil
dictutil = DictUtils()
# Determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(os.path.abspath(__file__))
else:
    application_path = "."
# Initialize Plugins Library
cli_plugins = plugins.Plugins(application_path, PluginsFromConfig=config.properties.plugins.paths)
# Initialize Logger with the name 'main' to make sure any child loggers 
# do not propagate their messages to the default 'root' logger,
# less you get duplicate output
logger = Logger().init_logger('main')

@with_plugins(iter_entry_points('ecli.plugins'))
@click.group()
@click.version_option(version=__version__)
@click.option('--config', type=str, nargs=1,
              help='Specify a config file (default is config.yaml)')
@click.option('---debug', is_flag=True, help='Enable debug output')
@click.option('--show-plugin-paths','-lp', is_flag=True, 
    help='List possible plugin paths')
@click.option('--silent', is_flag=True, help='Suppress all output')
@click.option('--verbose', count=True,
              help='Increase verbosity of output')
@click.option('--log-file', type=str, nargs=1,
              help='Log output to specified file')
def cli(**kwargs):
    """This program is a modular command line tool designed to act as the single entrypoint
    to your team's automation."""
    global config, verbose, logger

    suppress_output = True if kwargs.get('silent') else False
    # Are we specifying an alternate config file?
    alternate_config_path = kwargs.get('config')
    if alternate_config_path:
        config = Config(
            config_file_uri=alternate_config_path,
            default_value=default_config
        ).read()
        # Verbose mode enabled?
    # TODO Find a better approach to this hacky method
    debug = kwargs['_debug'] or dictutil.deep_get(config, 'logging.debug', False)
    verbose = kwargs.get('verbose', None) or dictutil.deep_get(config, 'logging.verbose', False)
    # Set up logging with our desired output level
    if debug:
        loglevel = logging.DEBUG  # 10
    elif verbose:
        loglevel = logging.INFO  # 20
    else:
        loglevel = logging.INFO  # 20
    if config is None or config == {}:
        logger.debug('No valid config file found %s' % config_file_name)
        logger.debug('Using program defaults')
    if suppress_output:
        if sys.version_info[0] >= 3:
            logging.disable(sys.maxsize) # Python 3        
        else:
            logging.disable(sys.maxint) # Python 2
    # Add the log  file handler to the logger, if applicable
    log_file = dictutil.deep_get(config, 'logging.log_file', None) or kwargs.get('log_file', None)
    if log_file:
        logging_maxBytes = dictutil.deep_get(config, 'logging.maxBytes', 10000000)
        logging_backupCount = dictutil.deep_get(config, 'logging.backupCount', 5)        
        formatter = logging.Formatter(logger.handlers[0].formatter._fmt)
        filehandler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=logging_maxBytes, backupCount=logging_backupCount)
        filehandler.setFormatter(formatter)        
        logger.addHandler(filehandler)
    return

@cli.command(name='runtime.info', context_settings=dict(
    ignore_unknown_options=True
))
def show_runtime_info(**kwargs):
    """Display runtime information"""
    logger.info("Current config path: %s" % config.properties.config_file_uri)
    
@cli.command(name='plugins.install', context_settings=dict(
    ignore_unknown_options=True
))
@click.option('--username', '-u',
  help='git repo username')
@click.option('--password', '-p',
  help='git repo password')
@click.option('--token', '-t',
  help='git repo token')
@click.option('--repo-url', '-r',
  required=True, help='git repo URL')
@click.option('--public-repo', '-R', cls=MutuallyExclusiveOption,
  is_flag=True, mutually_exclusive=["use_saved_credentials"],
  help='Used when repo does not require credentials')
@click.option('--use-saved-credentials', '-S', cls=MutuallyExclusiveOption,
  mutually_exclusive=["public_repo"], 
  is_flag=True, help='Use saved credentials')
@click.option('--alternate-name', '-n',
  help='Specify a different name for the cloned ecli Plugin repo')
@click.option('--plugin-path', '-T',
  help='Specify a different local path for the cloned ecli Plugin repo')
@click.option('--prompt-for-credentials', '-P',
  is_flag=True, help='Prompt for credentials')
def install_plugin(**kwargs):
  """Install ecli plugins from a git repo"""
  # Fail early if git command is not available
  from first import first
  from ecli.lib.plugin.finder import PluginFinder
  from ecli.lib.shell.which import which
  import re

  if not which('git'):
    sys.exit('"git" command not found in PATH, please install or make available')

  # Pluginfinder
  plugin_finder = PluginFinder()

  prompted_username = None
  prompted_password = None

  alternate_plugin_name = kwargs.get('alternate_name')

  # Prompt for credentials, if applicable
  if kwargs['prompt_for_credentials']:
    if sys.stdin.isatty():
       print("Enter credentials")
       prompted_username = input("Username: ")
       prompted_password = getpass.getpass("Password: ")
    else:
       prompted_username = sys.stdin.readline().rstrip()
       prompted_password = sys.stdin.readline().rstrip()

  # Derive credentials form first non-null value in list
  username = first([
      kwargs['username'],
      prompted_username,
      os.environ.get('username'),
      dictutil.deep_get(config, 'plugins.auth.username')
      ])
  password = first([
      kwargs['password'],
      prompted_password,
      os.environ.get('password'),
      dictutil.deep_get(config, 'plugins.auth.password')
      ])
  token = first([
      kwargs['token'],
      os.environ.get('token'),
      dictutil.deep_get(config, 'plugins.auth.token')
      ])

  # Fail if credentials not provided under certian conditios
  if not any([kwargs['use_saved_credentials'], kwargs['public_repo']]) and not all([username, password]):
    print('Error: Username and password can only be empty when')
    print('using saved credentials or specifying a public repo, seek --help')
    sys.exit()
  elif kwargs['prompt_for_credentials'] and not all([username, password]):
    sys.exit('Error: You specified an invalid username and/or password, seek --help')

  # Plugin Package Repo URL
  repo_url = kwargs['repo_url']
  # Reconstruct url if credentials provided
  if all([username,password]):
    repo_url = re.sub('(http://)(.*)|(https://)(.*)', '\\1%s:%s@\\2' % (username, password), repo_url)
  elif token:
    repo_url = re.sub('(http://)(.*)|(https://)(.*)', '\\1%s@\\2' % token, repo_url)

  # Derive the plugin path
  if kwargs['plugin_path']:
    plugin_path = plugin_finder.canonical_path(kwargs['plugin_path'])
  else:
    user_plugin_home = plugin_finder.canonical_path("~/.ecli")
    user_plugin_path = os.path.join(user_plugin_home, 'plugins')
    if not os.path.isdir(user_plugin_home):
      try:
        os.mkdir(user_plugin_home)
      except Exception as e:
        sys.exit('Failed to create plugin directory, error was %s' % e)
    plugin_sfx = repo_url.split('/')[-1]
    if alternate_plugin_name:
      plugin_name = alternate_plugin_name
    else:
      plugin_name = re.sub('\\.git$', '', plugin_sfx)
    plugin_path = os.path.join(user_plugin_path, plugin_name)
 
  repo_url_sanitized = repo_url.replace(str(password),'***')
 
  logger.debug('Effective Repo URL: %s' % repo_url_sanitized)
  cmd = 'git clone %s %s' % (repo_url, plugin_path)
  cmd_sanitized = cmd.replace(str(password),'***')
  logger.debug('git clone command is %s' % cmd_sanitized)
  # Try the git clone operation
  try:
    os.system(cmd)
  except Exception as e:
    sys.exit('Failed to pull plugin package %s' % str(e).replace(str(password), '***'))

@cli.command(name='plugins.list.paths', context_settings=dict(
    ignore_unknown_options=True
))
def list_plugin_paths(**kwargs):
  """List Available Plugin Paths"""
  logger.info('Available Plugin Paths:')
  for p in cli_plugins.plugin_paths:
      print('- %s' % p)

@cli.command(name='python.eval', context_settings=dict(
  ignore_unknown_options=True, 
  allow_extra_args=True,
  help_option_names=['---help']
  ), hidden=True)
@click.option('---ecli-eval-file',
  help='Evaluate specified python script file')
@click.argument('code', callback=Streams().read_stdin, required=False)
def eval_python_code(code, **kwargs):
  """Executes arbitrary python code"""
  file = kwargs['_ecli_eval_file']
  if file:
    global my
    my_obj = { 'invocation': 
        {
        'path': os.path.abspath(file)
        } 
    }
    my = Struct(my_obj)
    exec(open(file).read(), globals())
  else:
    exec(code, globals())

# Add plugins from PATH
cli_plugins.add_plugins_from_path(cli)
# Add plugins from ecli plugin paths
cli_plugins.add_plugins(cli, plugin_paths=cli_plugins.plugin_paths)

@cli.command(name='plugins.update.all', context_settings=dict(
  ignore_unknown_options=True
))
@click.pass_context
def update_all_plugin_paths(ctx, **kwargs):
  """Updates all detected plugin paths"""
  from ecli.lib.plugin.finder import PluginFinder
  warning = """
The update operation will clear any local changes you've made
to files in the following plugin paths:
%s
Do you want to continue? [yes|y/no|n]""" % '\n'.join(['- %s' % p for p in cli_plugins.plugin_paths])
  choice = input(warning)
  if choice.lower().startswith('y'):
      logger.info('Updating all available plugin paths:')
  else:
      logger.info('Program Exit. Not updating')
      sys.exit()
  for p in cli_plugins.plugin_paths:
      canonical_p = PluginFinder().canonical_path(p)
      p_is_git_repo = os.path.isdir(os.path.join(canonical_p,'.git'))
      if os.path.isdir(canonical_p):
          if p_is_git_repo:
              logger.info('Attempting to update %s ...' % p)
              ctx.invoke(cli.commands['plugins.update'], extra_arguments=['--plugin-path', p, '--no-prompt'])
          else:
              logger.warning('%s is not a git repo, skipping' % p)

if __name__ == '__main__':
	sys.exit(cli())