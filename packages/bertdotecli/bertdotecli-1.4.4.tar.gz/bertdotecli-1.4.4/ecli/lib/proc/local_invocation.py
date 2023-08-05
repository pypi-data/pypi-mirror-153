from ecli.lib.dictutils import DictUtils
from ecli.lib.logger import Logger
from ecli.lib.shell.which import which
import os
import re
import sys
from subprocess import Popen, PIPE, STDOUT, call, run
import threading
import time

# Import third-party and custom modules
try:
    from ecli.lib.shell import shell_map
    import colorama
except ImportError as e:
    print('Error in %s ' % os.path.basename(__file__))
    print('Failed to import at least one required module')
    print('Error was %s' % e)
    print('Please install/update the required modules:')
    print('pip install -U -r requirements.txt')
    sys.exit(1)

colorama.init(convert=True, autoreset=True) # Needed for Windows, supposedly ignored by linux

# Setup Logging
logger = Logger().init_logger(__name__)

class CliInvocation:

    def __init__(self):

        self.proc = None
        self.done = False
        self.invocation = type('obj', (object,), {
            'stdout': None,
            'failed': False,
            'returncode': 0
        }
        )        
        self.logger = logger

    def call(self, **kwargs):
        
        cmd = [kwargs['cmd_spec']]
        cmd_args = kwargs.get('cmd_args', [])
        ext = kwargs['cmd_ext']
        cmd_invocation = kwargs.get('invocation')
        cmd_is_interactive = kwargs.get('interactive')
        debug_enabled = kwargs.get('debug_enabled', False)
        suppress_output = kwargs.get('suppress_output', False)
        exe = shell_map[ext]['invocation'][cmd_invocation]['executable']
        
        # Adjust shell environment
        curr_env = os.environ.copy()
        env_variables = kwargs['env_variables']
        modified_env = DictUtils().Merge(env_variables,curr_env)

        if exe is None:
            self.logger.error("Specified executable is invalid, got '%s'" % exe)
            sys.exit(1)           
        executable = which(exe)
        if not executable:
            self.logger.error('No executable found for %s' % exe)
            sys.exit(1)
        if debug_enabled:
            process_invocation = [executable] + shell_map[ext]['invocation'][cmd_invocation]['flags_w_debug'] + cmd + cmd_args
        else:
            process_invocation = [executable] + shell_map[ext]['invocation'][cmd_invocation]['flags'] + cmd + cmd_args
        self.logger.debug('Process Invocation: %s' % process_invocation)
        if cmd_is_interactive:
          call(process_invocation, shell=True, env=modified_env)
          sys.exit()
        else:
          def thread_target():
              try:
                  if sys.version_info[0] >= 3:
                      with Popen(process_invocation, 
                          stdout=PIPE, 
                          stderr=STDOUT, 
                          bufsize=1, 
                          universal_newlines=True, 
                          env=modified_env
                          ) as self.proc:
                          if not suppress_output:
                              for line in self.proc.stdout:
                                  sys.stdout.write(line)  # process line here
                          if self.proc.returncode != 0:
                              self.invocation.failed = True
                              self.invocation.returncode = p.returncode
                              self.invocation.stdout = 'Encountered error code {errcode} in the specified command {args}'.format(
                                  errcode=p.returncode, args=p.args)
                              self.done = True
                      self.done = True
                      self.invocation.returncode = self.proc.returncode
                  else:
                      # Invoke process
                      self.proc = Popen(
                          process_invocation,
                          stdout=PIPE,
                          stderr=STDOUT)
                      # Poll for new output until finished
                      while True:
                          nextline = self.proc.stdout.readline()
                          if nextline == '' and self.proc.poll() is not None:
                              break
                          if not suppress_output:                        
                              sys.stdout.write(nextline)
                              sys.stdout.flush()
                      self.done = True
                      self.invocation.returncode = self.proc.returncode
              except Exception:
                  self.done = True

        try:
            if sys.version_info[0] >= 3:
                t = threading.Thread(target=thread_target, daemon=True)
            else:
                t = threading.Thread(target=thread_target)
            t.start()
        except Exception:
            pass
        try:
            while not self.done:
                time.sleep(0.1)
            return self.invocation

        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            try:
                self.proc.terminate()
            except Exception:
                pass