import logging
import logging.config
import os

from client.drupaluploader import DrupalUploader
from client.sqlgen import sql_gen


os.chdir(os.path.dirname(os.path.realpath(__file__)))
logging.config.fileConfig(os.path.dirname(os.path.realpath(__file__)) + '/logging.conf')
from client.api import FSPAPI
from client.tablehandler import TableHandler

__author__ = 'Peter Hinson'

import config


class FSPFlatstoreAPIClient(object):
    def __init__(self):
        # Configure the API object
        self.api = FSPAPI(config.BASE_URL, config.HTTP_USERNAME, config.HTTP_PASSWORD)
        self.uploader = DrupalUploader()

    def run(self):
        for target in config.targets:
            # For each config target (flatstore table to pull data for), configure the handler
            FSPFlatstoreAPIClient.set_formatter_params(target)
            # Setup the handler to process the target
            handler = TableHandler(target, self.api)
            # Run the handler. If successful, it'll return the path to the generated CSV file
            filepath = handler.run()

            if filepath:
                # If a generated CSV file path was returned by the handler, copy it to UPLOAD_PATH,
                # typically a web accessible directory.
                self.uploader.copy_file(filepath)
                config.all_flatstores.remove(target['flatstore'])

        # Record the flatstore tables that we couldn't pull data for:
        msg = ""
        for i in range(0, len(config.all_flatstores)):
            msg +="%s\n" % config.all_flatstores[i]
        logging.info("Missing flatstore tables: \n" + msg)

    @staticmethod
    def set_formatter_params(target):
        # Sets the formatter for a given config target. If the target doesn't define a formatter,
        # use monthly.
        target['formatter'] = config.formatters[target.get('formatter', 'monthly')]


def main():
    fsp_combine = FSPFlatstoreAPIClient()
    fsp_combine.run()
    sql_gen.close()


if __name__ == "__main__":
    main()
