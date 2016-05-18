import logging
import pprint
import datetime
import requests
from client.formatter import FlatstoreFormatter
from client.sqlgen import sql_gen
from config import DEFAULT_DATE_RANGE, API_DATE_FORMAT, DEBUG

__author__ = 'Peter Hinson'

logger = logging.getLogger('Handler')

class TableHandler(object):
    def __init__(self, target, api):
        self.target = target
        self.api = api
        self.formatter = FlatstoreFormatter(**target.get('formatter', {}))

        # Set the end date, default to today
        self.end_date = target.get('end_date', datetime.date.today())
        # Set the start date, default to date_range - end_date
        self.start_date = target.get('start_date',
                                     datetime.date(self.end_date.year,
                                                   self.end_date.month,
                                                   1)-target.get('date_range', DEFAULT_DATE_RANGE))

    def run(self):
        headers, rows, meta = [], [], []
        params = {
            'startdate': self.start_date.strftime(API_DATE_FORMAT),
            'enddate': self.end_date.strftime(API_DATE_FORMAT)
        }
        calls = self.target.get('calls', [[self.target.get('call'), None]])

        for call, row_label in calls:
            try:
                results = self.api.call(call, payload=params)
                if not results['results']:
                    # No results
                    logger.warning("%s - Empty result set for %s" % (
                        self.target['flatstore'], call))
                    continue
            except requests.exceptions.HTTPError as e:
                # Call not found
                logger.error(e)
                continue

            if DEBUG:
                pprint.pprint(self.target['flatstore'] + ' ' + call)
                # pprint.pprint(results)

            if row_label:
                self.formatter.default_row_label = row_label
            headers, new_rows, meta = self.formatter.format(results, self.start_date, self.end_date)
            rows += new_rows

        if rows:
            filename = self.target['flatstore'].split('flatstore_')[1]+'.txt'
            sql_gen.generate(self.target['flatstore'], filename, (len(calls) > 1 and None or meta))

            return self.formatter.output_csv(
                headers,
                rows,
                filename
            )
        else:
            logger.warning("%s - No rows found, not saving CSV " % self.target['flatstore'])
            return None
