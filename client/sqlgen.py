import config

__author__ = 'Peter Hinson'


class SQLGen(object):
    def __init__(self):
        self.out_file = open(config.SQL_OUTPUT_FILE, "w+")

    def close(self):
        self.out_file.close()

    def generate(self, flatstore, filename, meta=None):
        file_url = "%s/%s" % (config.UPLOAD_URL, filename)

        output = "UPDATE feedapi INNER JOIN flatstore ON flatstore.id=feedapi.nid SET " \
                 "feedapi.url='%s', feedapi.link='%s', feedapi.checked=0 WHERE " \
                 "feedapi.feed_type='1' AND " \
                 "flatstore.table_name='%s';\n" % (
                     file_url,
                     file_url,
                     flatstore
                 )

        if meta and False:
            output += """UPDATE content_type_dataset INNER JOIN flatstore ON
            flatstore.id=content_type_dataset.nid SET
                          content_type_dataset.field_temporal_value='%s',
                          content_type_dataset.field_source_value='%s',
                          content_type_dataset.field_units_value='%s',
                          content_type_dataset.field_footnote_value="%s"
                          WHERE flatstore.table_name='%s';\n""" % (
                meta['type']['frequency'].title(),
                "%s %s" % (meta['datasource']['division'], meta['type']['lastUpdate']),
                meta['type']['unit'],
                (meta['type']['description'] and meta['type']['description'].replace('"',
                                                                                     '\\"').replace(
                    "'", "\\'") or ''),
                flatstore
            )

        self.out_file.write(output)

# Singleton
sql_gen = SQLGen()
