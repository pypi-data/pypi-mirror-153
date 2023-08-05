Monkey Crawler
==============

Small framework to crawl misc data sources and process records.

Installation guide
------------------

::

    pip install monkey.crawler

User guide
----------

Crawler attributes
-source_name: the name that identifies the data source
-handler: the handler that will process every record
-offset: the number of record that will be skipped by the crawler before to start


CSV Crawler
_SOURCE_DELIMITER_KEY = 'source_delimiter'
_SOURCE_FILE_ENCODING_KEY = 'source_encoding'
_SOURCE_FILE_KEY = 'source_file'
_SOURCE_QUOTE_CHAR_KEY = 'source_quote_char'
_COLUMN_MAP_KEY = 'column_map'
_COLUMN_MAP_DELIMITER_KEY = 'column_map_delimiter'
   
