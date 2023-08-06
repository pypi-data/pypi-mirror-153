#from asyncio.log import logger
import logging
import json
import os


class LoggingUtils():
    default_ignore_error_list =[
        'RESOURCE_ALREADY_EXISTS']

    loglevel = logging.INFO

    @classmethod
    def set_logger_level(cls, loglevel_):
        cls.loglevel=loglevel_
        
    #DEBUG < INFO < WARNING < ERROR < CRITICAL
    @classmethod
    def get_logger(cls, modname='_profiler_'):
        import platform
        logpath=''
        if platform.system()=='Darwin':
            logpath='./Logs/dbrprofiler.log'
        else:
            logpath='/var/log/dbrprofiler.log'

        # Create a custom logger
        logger = logging.getLogger(modname)


        if logger.handlers == []:
            # Create handlers
            import sys
            c_handler = logging.StreamHandler(sys.stdout)
            f_handler = logging.FileHandler(logpath)

            # Create formatters and add it to handlers
            c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            c_handler.setFormatter(c_format)
            f_handler.setFormatter(f_format)

            # Add handlers to the logger
            logger.addHandler(c_handler)
            logger.addHandler(f_handler)
        logger.setLevel(cls.loglevel)
        return logger


    def check_error(response, ignore_error_list=default_ignore_error_list):
        return ('error_code' in response and response['error_code'] not in ignore_error_list) \
                or ('error' in response and response['error'] not in ignore_error_list) \
                or (type(response)==dict and response.get('resultType', None) == 'error' and 'already exists' not in response.get('summary', None))
