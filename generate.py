from app.main import Application

import logging


if __name__ == '__main__':
	logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
	application = Application()
	application.start()
