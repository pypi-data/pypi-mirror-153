default_config = {
  "bastion_mode": {
    "config_file": "sftp-config.json",
    "enabled": True,
    "keep_alive": True,
    "poll_wait_time": 5,
    "sftp_sync": True
  },
  "config_file_uri": "no config found",
  "logging": {
    "maxBytes": 10000000,
    "backupCount": 5,
    "debug": False,
    "verbose": False,
    "log_file": ''
  },
  "plugins": {
    "paths": ["./plugins"],
    "repository": ''
  }
}