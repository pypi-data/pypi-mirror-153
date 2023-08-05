import os
import re
import sys
from ecli.lib.shell.bash_init import bash_env_variables, bash_pre_exec

# Account for script packaged as an exe via cx_freeze
if getattr(sys, 'frozen', False):
  self_file_name = os.path.basename(sys.executable)
else:
  # Account for script packaged as zip app
  self_file_name = os.path.basename(__file__)

# Define how we handle different shell invocations
shell_map = {
  '.sh': {
    'docstring_search': re.compile('__docstring__[\W]+(.*).'),
    'invocation_search': re.compile('__invocation__[\W]+(.*).'),
    'interactive_search': re.compile('__interactive__[\W]+(.*).'),
    'invocation': {
      'standard': {
        'executable': 'bash',
        'env_variables': bash_env_variables,
        'pre_exec': bash_pre_exec,
        'flags': [],
        'flags_w_debug': ['-x']
      }
    }
  },
  '.ps1': {
    'docstring_search': re.compile('\$__docstring__[\W]+(.*).'),
    'invocation_search': re.compile('\$__invocation__[\W]+(.*).'),
    'interactive_search': re.compile('\$__interactive__[\W]+(.*).'),
    'messages':{
      'notfound': 'Please install with ""'
    },
    'invocation': {
      'standard': {
        'executable': 'pwsh',
        'flags': ['-ExecutionPolicy', 'Bypass', '-File'],
        'flags_w_debug': ['-ExecutionPolicy', 'Bypass', '-File'],
      }
    }
  }, 
  '.py': {
    'docstring_search': re.compile('__docstring__[\W]+(.*).'),
    'invocation_search': re.compile('__invocation__[\W]+(.*).'),
    'interactive_search': re.compile('__interactive__[\W]+(.*).'),
    'invocation': {
      'standard': {
        'executable': 'python',
        'flags': [],
        'flags_w_debug': ['-m', 'pdb']
      },
      'frozen': {
        'executable': 'ecli',
        'flags': ['python.eval', '---ecli-eval-file'],
        'flags_w_debug': ['python.eval', '---ecli-eval-file']
      }
    }
  }, 
  '.rb': {
    'docstring_search': re.compile('__docstring__[\W]+(.*).'),
    'invocation_search': re.compile('__invocation__[\W]+(.*).'),
    'interactive_search': re.compile('__interactive__[\W]+(.*).'),
    'invocation': {
      'standard': {
        'executable': 'ruby',
        'flags': [],
        'flags_w_debug': ['-r', 'debug'],
      }
    }
  }
}

# Define list of valid file extensions
shell_exts = [s for s in shell_map.keys()]
# Define valid shell file patterns
shell_patterns = ['.*%s$' % s for s in shell_exts]
# Define shell filter
shell_filter = '(%s)' % '|'.join(shell_exts)
