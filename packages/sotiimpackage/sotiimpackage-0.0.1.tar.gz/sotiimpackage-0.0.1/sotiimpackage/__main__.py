import logging
from SotiimPackage import unreleased


logging.basicConfig(level=logging.DEBUG)
if __name__ == "__main__":
    workshops= unreleased()
    logging.debug(unreleased.__doc__)

