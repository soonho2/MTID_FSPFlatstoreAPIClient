import csv
import datetime
import logging
from operator import itemgetter
import os

from dateutil.relativedelta import relativedelta

import config


logger = logging.getLogger('Formatter')


class FlatstoreFormatter(object):
    date_in_format = '%Y-%m-%d'
    date_out_format = '%b_%y'
    date_increment = relativedelta(months=1)
    date_field = 'date'
    value_field = 'price'
    country_field = u'Country'
    lower_date = True
    default_row_label = u'World'
    trim_date = True  # Trim empty dates off the start and end of the collection
    reformat_date = True  # Use date formatting to sort and manage the collection
    earliest_date = None
    latest_date = None
    skip_null = False
    data_type = 'values'

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def format(self, data, start_date, end_date=datetime.date.today()):
        if self.data_type == 'country':
            return self.format_countries(data)

        dates = []
        meta = data['meta']
        results = data['results']
        rows = []

        for country in results:
            row = {
                self.country_field: 'country_en' in country and country['country_en'] or
                                    self.default_row_label
            }

            self.check_date_range(country)

            for entry in country['data']:
                if self.value_field in entry and self.date_field in entry:
                    if self.reformat_date:
                        row[self.format_date(entry[self.date_field])] = entry[self.value_field]
                        if entry[self.date_field] not in dates:
                            dates.insert(0, entry[self.date_field])
                    else:
                        row[entry[self.date_field]] = entry[self.value_field]
                        if entry[self.date_field] not in dates:
                            dates.insert(0, entry[self.date_field])

            rows += [row]

        # Do this after looping through the data - so we have established start and end dates
        # dates = self.get_date_range(start_date, end_date)
        if self.reformat_date and rows:
            dates = self.get_date_range(start_date, end_date, dates)
        headers = [self.country_field] + dates
        return headers, rows, meta

    def format_countries(self, data):
        country_csv = 'assets/countries.csv'
        meta = None
        results = data['results']
        rows = []
        headers = ['Country', 'Region', 'Type', 'Country1', 'lat1', 'lon1', 'top1', 'right1',
                   'bottom1', 'left1']

        for entry in results:
            row = {'Country': entry['country_en'].encode('ascii', 'ignore'),
                   'Country1': entry['country_en'].encode('ascii', 'ignore'),
                   'Region': entry['region_en'] and entry['region_en'].encode('ascii', 'ignore') or \
                             "",
                   'Type': "Country"}

            rows += [row]

        # Post process against existing country data. Adds longitude, latitude
        with open(country_csv) as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                found = False
                for api_row in rows:
                    if api_row['Country'].lower() == row['Country'].lower() or \
                        (api_row['Country'] == 'Viet Nam' and row['Country'] == 'Vietnam'):
                        # Found a match.. copy the lon, lat, etc
                        for field in ['lat1', 'lon1', 'top1', 'right1', 'bottom1', 'left1']:
                            api_row[field] = row[field]
                        found = True
                if not found:
                    rows += [row]

        # Sort:
        rows = sorted(rows, key=itemgetter('Country'))
        return headers, rows, meta

    def output_csv(self, headers, rows, filename):
        filepath = os.path.join(config.OUTPUT_DIR, filename)
        with open(filepath, 'wb') as f:
            writer = csv.DictWriter(f, headers, extrasaction='ignore', delimiter=',',
                                    quotechar='"',
                                    quoting=csv.QUOTE_ALL)
            writer.writerow(dict((fn, fn) for fn in headers))

            logger.info("%s - wrote %d rows with %s headers" % (filename, len(rows), len(headers)))

            for row in rows:
                writer.writerow(row)

        return filepath

    def check_date_range(self, country):
        # We're trying to establish the min and max dates of a given data set
        if self.reformat_date and 'data' in country and len(country['data']):
            test_high_date = datetime.datetime.strptime(country['data'][0][self.date_field],
                                                        self.date_in_format)
            test_low_date = datetime.datetime.strptime(country['data'][-1][self.date_field],
                                                       self.date_in_format)

            if self.latest_date is None or test_high_date > self.latest_date:
                self.latest_date = test_high_date
            if self.earliest_date is None or test_low_date < self.earliest_date:
                self.earliest_date = test_low_date

    def format_date(self, in_date):
        if isinstance(in_date, basestring):
            # Received a stirng. Format string to date object
            in_date = datetime.datetime.strptime(in_date, self.date_in_format)

        date_str = in_date.strftime(self.date_out_format)

        if self.lower_date:
            return date_str.lower()
        else:
            return date_str

    def get_date_range(self, start_date=None, end_date=None, dates=[]):
        if self.trim_date or not start_date:
            start_date = self.earliest_date
        if self.trim_date or not end_date:
            end_date = self.latest_date

        current_date = end_date
        formatted_dates = []

        if self.skip_null:
            for date in dates:
                formatted_dates.append(self.format_date(date))
        else:
            while current_date >= start_date:
                formatted_dates.insert(0, self.format_date(current_date))
                current_date = current_date - self.date_increment

        return formatted_dates
