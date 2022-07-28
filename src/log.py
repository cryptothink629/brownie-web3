import logging


def file_handler(output, ):
    fh = logging.FileHandler(output)
    fh.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
        '%(asctime)s - %(module)s - %(name)s[line:%(lineno)d] - %(process)d - %(levelname)s: %(message)s')
    fh.setFormatter(fmt)
    return fh


def stream_handler():
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
    ch.setFormatter(fmt)
    return ch


logging.getLogger("web3.RequestManager").setLevel(logging.ERROR)
logging.getLogger("web3.providers.HTTPProvider").setLevel(logging.ERROR)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.addHandler(file_handler('web3.log'))
logger.addHandler(stream_handler())
