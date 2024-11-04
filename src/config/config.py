import configparser
import platform
import logging
import sys
from pathlib import Path
from src.config.default_config import default_config


class Config:
    """
    Reads the configuration from the file and provides it to
    the rest of the app
    """
    @staticmethod
    def config_error(message):
        """
        Prints out an error in lieu of logging (since the logging class has
        not been instantiated yet when config is being read)
        :param message: Specific test pertinent to the issue
        :return: Nothing
        """
        logging.error('Configuration error, cannot proceed.')
        logging.error(message)
        logging.error('Please contact the administrator.')
        sys.exit(1)

    @staticmethod
    def config_info(message):
        logging.info(message)

    def __init__(self):
        os = platform.system()

        # make sure that the config file exists
        config_file = Path()
        if os == 'Linux':
            config_file = Path(Path.home(), '.config/ProjectTBD/config.ini')
        elif os == 'Windows':
            config_file = Path(Path.home(), 'AppData/Roaming/ProjectTBD/config.ini')
        elif os == 'Darwin':
            config_file = Path(Path.home(), 'Library/Application Support/ProjectTBD/config.ini')
        else:
            Config.config_error("Unsupported operating system.")
        if not config_file.exists():
            # if there is no config file, we can't continue
            # there is also no logger class yet, so just print out the errors
            # and exit
            Config.config_info(f'config file {config_file} does not exist, creating it')
            try:
                config_file.parent.mkdir(parents=True, exist_ok=True)
                with open(config_file, 'w') as f:
                    f.write(default_config)
                    Config.config_info(f'config file {config_file} created')
                # shutil.copy(Path('config/config.ini'), config_file)
            except PermissionError:
                Config.config_error(f'Permission denied, cannot create config file {config_file}')
        config = configparser.ConfigParser()

        # read the file in
        config.read(config_file)

        # load the specific configuration
        # minimum overall logging level
        try:
            self.logging_min_log_level = Config._log_level_check(config['Logging']['min_log_level'])
        except KeyError:
            Config.config_error('The key "min_log_level" is not present in the config file')
            sys.exit(1)

        # the minimum logging level for the console handler
        try:
            self.logging_console_min_log_level = Config._log_level_check(config['Logging']['console_min_log_level'])
        except KeyError:
            Config.config_error('The key "console_min_log_level" is not present in the config file')
            sys.exit(1)

        # the minimum logging level for the file handler
        try:
            self.logging_file_min_log_level = Config._log_level_check(config['Logging']['file_min_log_level'])
        except KeyError:
            Config.config_error('The key "file_min_log_level" is not present in the config file')
            sys.exit(1)

        # make sure the log file exists
        if os == 'Linux':
            self.logging_log_file_path = Path(Path.home(), '.config/ProjectTBD/logs/error.log')
        elif os == 'Windows':
            self.logging_log_file_path = Path(Path.home(), 'AppData/Roaming/ProjectTBD/logs/error.log')
        elif os == 'Darwin':
            self.logging_log_file_path = Path(Path.home(), 'Library/Application Support/ProjectTBD/logs/error.log')
        else:
            Config.config_error("Unsupported operating system.")
        if not self.logging_log_file_path.exists():
            # create the log file
            Config.config_info(f'log file {self.logging_log_file_path} does not exist, creating it')
            try:
                self.logging_log_file_path.parent.mkdir(parents=True, exist_ok=True)
                Config.config_info(f'log file {self.logging_log_file_path} created')
            except PermissionError:
                Config.config_error(f'Permission denied, cannot create log file {self.logging_log_file_path}')

        # create the folder for the accounts, message sets and addressee sets
        for d in ['accounts', 'message_sets', 'addressee_sets']:
            dir_name = f'{d}_dir'
            os_dirs = {'Linux': Path(Path.home(), f'.config/ProjectTBD/{d}'),
                       'Windows': Path(Path.home(), f'AppData/Roaming/ProjectTBD/{d}'),
                       'Darwin': Path(Path.home(), f'Library/Application Support/ProjectTBD/{d}')}
            self.__setattr__(dir_name, os_dirs[os])
            if not self.__getattribute__(dir_name).exists():
                Config.config_info(f'Directory {self.__getattribute__(dir_name)} does not exist, creating it')
                try:
                    self.__getattribute__(dir_name).mkdir(parents=True, exist_ok=True)
                    Config.config_info(f'Directory {self.__getattribute__(dir_name)} created')
                except PermissionError:
                    Config.config_error(f'Permission denied, cannot create accounts directory {self.__getattribute__(dir_name)}')

        # # create the folder for the message sets JSONS
        # # create the folder for the accounts JSONS
        # if os == 'Linux':
        #     self.accounts_dir = Path(Path.home(), '.config/ProjectTBD/message-sets')
        # elif os == 'Windows':
        #     self.accounts_dir = Path(Path.home(), 'AppData/Roaming/ProjectTBD/accounts')
        # elif os == 'Darwin':
        #     self.accounts_dir = Path(Path.home(), 'Library/Application Support/ProjectTBD/accounts')
        # if not self.accounts_dir.exists():
        #     Config.config_info(f'accounts directory {self.accounts_dir} does not exist, creating it')
        #     try:
        #         self.accounts_dir.mkdir(parents=True, exist_ok=True)
        #         Config.config_info(f'accounts directory {self.accounts_dir} created')
        #     except PermissionError:
        #         Config.config_error(f'Permission denied, cannot create accounts directory {self.accounts_dir}')

    @staticmethod
    def _log_level_check(conf_level):
        """
        Given the level from the conf file (like "debug"),
        returns the actual logger level (logging.DEBUG)
        This could have been added to the Logger class, but it is good to have
        it here, because we can check the config before starting any
        other processes.
        :param conf_level: min_log_level from the config file
        :return: logging.log_level
        """
        # Only very new versions have switch/case, best not rely on it
        if conf_level.lower() == 'debug':
            return logging.DEBUG
        if conf_level.lower() == 'info':
            return logging.INFO
        if conf_level.lower() == 'warning' or \
                conf_level.lower() == 'warn':
            return logging.WARNING
        if conf_level.lower() == 'error':
            return logging.ERROR
        if conf_level.lower() == 'critical':
            return logging.CRITICAL
        else:
            # If there is an error, we need to display it (but the
            # class is not instantiated, so we just use plain logging)
            Config.config_error(f'"{conf_level}" is not a legal config level')
            # we can't use the configuration, let's exit
            sys.exit(1)


config = Config()


if __name__ == '__main__':
    conf = Config()
    assert conf.logging_log_file_path == '/Users/mike/nonexistent_file/error.log'
    assert conf.logging_min_log_level == 'debug'
