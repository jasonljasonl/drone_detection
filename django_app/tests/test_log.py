import logging

def test_log():
    logging.basicConfig(filename='test_log.log', encoding='utf-8', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    logger.info('')

test_log()