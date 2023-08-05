import datetime
import time
import logging

logger = logging.getLogger(__name__)


def main():
    """running the showtime"""
    while True:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("keyboard quit")
