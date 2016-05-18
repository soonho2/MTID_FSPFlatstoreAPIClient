import os

from dateutil.relativedelta import relativedelta


DEBUG = True

# Drupal Config
HOST_BASE_URL = "http://data.foodsecurityportal.org/"  # Base URL of site. Include trailing slash
DOC_ROOT_PATH = "/home/lnkd/fsp_api/public/"  # Include trailing slash

RELATIVE_UPLOAD_PATH = "tools/generated"

# API Config
BASE_URL = "http://data.foodsecurityportal.org/"  # API url. Include trailing slash.
HTTP_USERNAME = None
HTTP_PASSWORD = None
API_DATE_FORMAT = '%Y%m%d'

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'outputs').replace('\\', '/')
DEFAULT_DATE_RANGE = relativedelta(years=7)

SQL_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "sql_output.sql")  # Path to SQL output

# importing local config if any
try:
    from config_local import *
except ImportError:
    pass

UPLOAD_URL = "%s%s" % (HOST_BASE_URL, RELATIVE_UPLOAD_PATH)
UPLOAD_PATH = "%s%s" % (DOC_ROOT_PATH, RELATIVE_UPLOAD_PATH)


formatters = {
    'monthly': {
        'date_in_format': '%Y-%m-%d',
        'date_out_format': '%b %y',
        'lower_date': False,
        'date_increment': relativedelta(months=1),
        'date_field': 'date',
        'value_field': 'price',
        'country_field': 'Country'
    },
    'monthly_commodity': {
        'date_in_format': '%Y-%m-%d',
        'date_out_format': '%b %y',
        'lower_date': False,
        'date_increment': relativedelta(months=1),
        'date_field': 'date',
        'value_field': 'price',
        'country_field': 'Commodity'
    },
    'monthly_underscore': {
        'date_in_format': '%Y-%m-%d',
        'date_out_format': '%b_%y',
        'date_increment': relativedelta(months=1),
        'lower_date': True,
        'date_field': 'date',
        'value_field': 'price',
        'country_field': 'country'
    },
    'weekly_commodity': {
        'date_in_format': '%Y-%m-%d',
        'date_out_format': '%m/%d/%Y',
        'date_increment': relativedelta(weeks=1),
        'lower_date': False,
        'date_field': 'date',
        'value_field': 'price',
        'country_field': 'Commodity'
    },
    'daily_commodity': {
        'date_in_format': '%Y-%m-%d',
        'date_out_format': '%m/%d/%Y',
        'date_increment': relativedelta(days=1),
        'lower_date': False,
        'skip_null': True,
        'date_field': 'date',
        'value_field': 'price',
        'country_field': 'Commodity'
    },
    'indicators_year': {
        'date_in_format': '%Y',
        'date_out_format': '%Y',
        'lower_date': False,
        'date_increment': relativedelta(years=1),
        'date_field': 'year',
        'value_field': 'value',
        'country_field': 'Country'
    },
    'indicators_year_range': {
        # e.g. 2012-14
        'date_field': 'year',
        'value_field': 'value',
        'reformat_date': False,
        'trim_date': False,
        'country_field': 'Country'
    },
    'country': {
        # e.g. 2012-14
        'data_type': 'country',
        'date_field': None,
        'value_field': None,
        'reformat_date': False,
        'trim_date': False,
        'country_field': 'Country'
    },
}
targets = [
    {
        'flatstore': 'flatstore_countries',
        'formatter': 'country',
        'call': 'countries'
    },
    {
        'flatstore': 'flatstore_commodities_futures_',
        'formatter': 'daily_commodity',
        'date_range': relativedelta(days=60),
        'calls': [
            ['prices/23', 'Maize'],
            ['prices/24', 'Rice'],
            ['prices/19', 'Soft Wheat'],
            ['prices/13', 'Hard Wheat'],
            ['prices/25', 'Soybean'],
        ]
    },

    {
        'flatstore': 'flatstore_world_commodity_pric',
        'formatter': 'monthly_commodity',
        'calls': [
            ['prices/11', 'Maize'],
            ['prices/10', 'Rice'],
            ['prices/8', 'Wheat'],
            ['prices/9', 'Soybean'],
            ['prices/46', 'Oil']
        ]
    },
    {
        'flatstore': 'flatstore_world_rice_price',
        'call': 'prices/10'
    },
    {
        'flatstore': 'flatstore_world_maize_price',
        'call': 'prices/11'
    },
    {
        'flatstore': 'flatstore_world_soybean_price',
        'call': 'prices/9'
    },
    {
        'flatstore': 'flatstore_world_wheat_price',
        'call': 'prices/8'
    },
    {
        'flatstore': 'flatstore_world_oil_price',
        'call': 'prices/46'
    },
    {
        'flatstore': 'flatstore_global_oil_prices',
        'call': 'prices/46'
    },
    {
        'flatstore': 'flatstore_rice',
        'call': 'prices/15'
    },
    {
        'flatstore': 'flatstore_gdp',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=65),
        'call': 'indicators/gdp'
    },
    {
        'flatstore': 'flatstore_maize',
        'call': 'prices/17'
    },
    {
        'flatstore': 'flatstore_wheat',
        'call': 'prices/16'
    },


    # TODO: insert flatstore_under_5_mortality_ra .. missing currently
    {
        'flatstore': 'flatstore_percent_children_und',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=10),
        'call': 'indicators/children_undernourished'
    },
    {
        'flatstore': 'flatstore_under_5_mortality_ra',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=10),
        'call': 'indicators/under_5_mortality_rate'
    },

    {
        'flatstore': 'flatstore_fao_export_wheat',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=60),
        'call': 'indicators/Wheat_Exports'
    },
    {
        'flatstore': 'flatstore_fao_export_maize',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=60),
        'call': 'indicators/maize_exports'
    },
    {
        'flatstore': 'flatstore_fao_export_rice',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=60),
        'call': 'indicators/rice_exports'
    },
    {
        'flatstore': 'flatstore_fao_export_soybeans',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=60),
        'call': 'indicators/soybean_exports'
    },
    {
        'flatstore': 'flatstore_fao_import_wheat',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=60),
        'call': 'indicators/wheat_imports'
    },
    {
        'flatstore': 'flatstore_fao_import_maize',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=60),
        'call': 'indicators/maize_imports'
    },
    {
        'flatstore': 'flatstore_fao_import_rice',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=60),
        'call': 'indicators/rice_imports'
    },
    {
        'flatstore': 'flatstore_fao_import_soybeans',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=60),
        'call': 'indicators/soybean_imports'
    },
    {
        'flatstore': 'flatstore_fao_production_rice',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=60),
        'call': 'indicators/Rice_Production'
    },
    {
        'flatstore': 'flatstore_fao_production_maize',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=60),
        'call': 'indicators/Maize_Production'
    },
    {
        'flatstore': 'flatstore_fao_production_wheat',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=60),
        'call': 'indicators/wheat_production'
    },
    {
        'flatstore': 'flatstore_fao_production_soybe',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=60),
        'call': 'indicators/soybean_production'
    },
    {
        'flatstore': 'flatstore_fao_receipts_of_food',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=60),
        'call': 'indicators/Maize_Production'
    },
    {
        'flatstore': 'flatstore_fao_population_under',
        'formatter': 'indicators_year_range',
        'date_range': relativedelta(years=80),
        'call': 'indicators/Population_Undernourished'
    },
    {
        'flatstore': 'flatstore_fao_calorie_supply_p',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=80),
        'call': 'indicators/Calorie_Supply_Per_Ca_Crop'
    },
    {
        'flatstore': 'flatstore_ghi',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=80),
        'call': 'indicators/GHI'
    },
    {
        'flatstore': 'flatstore_population',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=80),
        'call': 'indicators/population'
    },
    {
        'flatstore': 'flatstore_population_density',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=80),
        'call': 'indicators/Population_Density'
    },
    {
        'flatstore': 'flatstore_gni_per_capita',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=80),
        'call': 'indicators/GNI_Per_Ca'
    },
    {
        'flatstore': 'flatstore_inflation',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=80),
        'call': 'indicators/Global_Inflation'
    },
    {
        'flatstore': 'flatstore_unemployment',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=80),
        'call': 'indicators/unemployment'
    },
    {
        'flatstore': 'flatstore_cpi',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=80),
        'call': 'indicators/cpi'
    },
    {
        'flatstore': 'flatstore_percent_below_povert',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=80),
        'call': 'indicators/National_Poverty_Rates'
    },
    {
        'flatstore': 'flatstore_agriculture_value_ad',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=80),
        'call': 'indicators/Agriculture_Value_Added'
    },
    {
        'flatstore': 'flatstore_agricultural_land_pe',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=80),
        'call': 'indicators/Agricultural_Land'
    },
    {
        'flatstore': 'flatstore_external_debt_percen',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=80),
        'call': 'indicators/external_debt'
    },
    {
        'flatstore': 'flatstore_fdi',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=80),
        'call': 'indicators/Foreign_Direct_Investment'
    },

    {
        'flatstore': 'flatstore_calorie_supply_per_c',
        'formatter': 'indicators_year',
        'date_range': relativedelta(years=80),
        'call': 'indicators/Calorie_Supply_per_Ca_Livestock'
    },
    {
        'flatstore': 'flatstore_weekly_commodities_p',
        'formatter': 'weekly_commodity',
        'date_range': relativedelta(years=2),
        'calls': [
            ['prices/4', 'Maize'],
            ['prices/3', 'Rice'],
            ['prices/1', 'Soft Wheat'],
            ['prices/18', 'Hard Wheat'],
            ['prices/2', 'Soybean'],
        ]
    },

]

# List of all flatstore tables. Used to print out missing datasets at end of run.
all_flatstores = ["flatstore_countries",
                  "flatstore_global_oil_prices",
                  "flatstore_world_maize_price",
                  "flatstore_fao_price_wholesale_",
                  "flatstore_population_density",
                  "flatstore_agriculture_value_ad",
                  "flatstore_agricultural_land_pe",
                  "flatstore_external_debt_percen",
                  "flatstore_fdi",
                  "flatstore_world_wheat_price",
                  "flatstore_price_wholesale_soyb",
                  "flatstore_world_rice_price",
                  "flatstore_world_soybean_price",
                  "flatstore_world_oil_price",
                  "flatstore_calorie_supply_per_c",
                  "flatstore_weekly_commodities_p",
                  "flatstore_commodities_futures_",
                  "flatstore_fao_receipts_of_food",
                  "flatstore_fao_population_under",
                  "flatstore_fao_calorie_supply_p",
                  "flatstore_ghi",
                  "flatstore_regions",
                  "flatstore_population",
                  "flatstore_gni_per_capita",
                  "flatstore_inflation",
                  "flatstore_cpi",
                  "flatstore_percent_below_povert",
                  "flatstore_countries",
                  "flatstore_world_commodity_pric",
                  "flatstore_rice",
                  "flatstore_gdp",
                  "flatstore_maize",
                  "flatstore_wheat",
                  "flatstore_under_5_mortality_ra",
                  "flatstore_percent_children_und",
                  "flatstore_unemployment",
                  "flatstore_fao_import_soybeans",
                  "flatstore_fao_import_wheat",
                  "flatstore_fao_import_rice",
                  "flatstore_fao_import_maize",
                  "flatstore_fao_export_soybeans",
                  "flatstore_fao_export_wheat",
                  "flatstore_fao_export_rice",
                  "flatstore_fao_export_maize",
                  "flatstore_fao_production_soybe",
                  "flatstore_fao_production_wheat",
                  "flatstore_fao_production_rice",
                  "flatstore_fao_production_maize"
]
