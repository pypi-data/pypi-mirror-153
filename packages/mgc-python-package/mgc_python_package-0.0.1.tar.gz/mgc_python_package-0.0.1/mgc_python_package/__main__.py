import logging
from mgc_python_package import unreleased

'''
 menssages:
 info  --> 10
 debug --> 20
 warning --> 30
 error --> 40
 critical --> 50
'''
logging.basicConfig(level=logging.DEBUG)
# execute everything in the block if and only if this file is executed as main
if __name__ == '__main__':
   logging.debug('>>> Starting the package....')
   workshops = unreleased();
   #logging.debug(unreleased.__doc__)
   logging.debug(help(unreleased))
   logging.debug(workshops)
   logging.debug('>>> Finishing the package....')