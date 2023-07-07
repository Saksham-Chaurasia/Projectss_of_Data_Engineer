from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, hour, dayofmonth, month, year, dayofweek,monotonically_increasing_id,udf
from pyspark.sql.types import StringType

spark = SparkSession \
        .builder \
        .appName("uber Data") \
        .master("local[1]") \
        .getOrCreate()

df = spark.read.csv("D:/Projectssssss/uber_Data_Analysis project/uber_data.csv", header=True, inferSchema=True, 
                    nullValue='NA', nanValue='NaN')
df.show()
df.count()

# Convert pickup and dropoff datetime columns to date type
df = df.withColumn('tpep_pickup_datetime', to_date(col('tpep_pickup_datetime')))
df = df.withColumn('tpep_dropoff_datetime', to_date(col('tpep_dropoff_datetime')))

# Drop duplicates and add trip_id column
df = df.dropDuplicates().withColumn('trip_id', monotonically_increasing_id())

# Create datetime_dim DataFrame
datetime_dim = df.select('tpep_pickup_datetime', 'tpep_dropoff_datetime') \
    .withColumn('pick_hour', hour(col('tpep_pickup_datetime'))) \
    .withColumn('pick_day', dayofmonth(col('tpep_pickup_datetime'))) \
    .withColumn('pick_month', month(col('tpep_pickup_datetime'))) \
    .withColumn('pick_year', year(col('tpep_pickup_datetime'))) \
    .withColumn('pick_weekday', dayofweek(col('tpep_pickup_datetime'))) \
    .withColumn('drop_hour', hour(col('tpep_dropoff_datetime'))) \
    .withColumn('drop_day', dayofmonth(col('tpep_dropoff_datetime'))) \
    .withColumn('drop_month', month(col('tpep_dropoff_datetime'))) \
    .withColumn('drop_year', year(col('tpep_dropoff_datetime'))) \
    .withColumn('drop_weekday', dayofweek(col('tpep_dropoff_datetime'))) \
    .withColumn('datetime_id', monotonically_increasing_id())

# Create rate_code_dim DataFrame
rate_code_type = {
    1: 'Standard rate',
    2: 'JFK',
    3: 'Newark',
    4: 'Nassau or Westchester',
    5: 'Negotiated fare',
    6: 'Group ride'
}

rate_code_udf = udf(lambda code: rate_code_type.get(code, ''), StringType())

rate_code_dim = df.select('RatecodeID').distinct() \
    .withColumn('rate_code_id', monotonically_increasing_id()) \
    .withColumn('rate_code_name', rate_code_udf(col('RatecodeID')))

# Create payment_type_dim DataFrame
payment_type_name = {
    1: 'Credit Card',
    2: 'Cash',
    3: 'No charge',
    4: 'Dispute',
    5: 'Unknown',
    6: 'Voided trip'
}

payment_type_udf = udf(lambda payment_type: payment_type_name.get(payment_type, ''), StringType())

payment_type_dim = df.select('payment_type').distinct() \
    .withColumn('payment_type_id', monotonically_increasing_id()) \
    .withColumn('payment_type_name', payment_type_udf(col('payment_type')))

# Create passenger_count_dim DataFrame
passenger_count_dim = df.select('passenger_count').distinct() \
    .withColumn('passenger_count_id', monotonically_increasing_id()) \
    .withColumn('passenger_count_value', col('passenger_count').cast('int'))
# Create trip_distance_dim DataFrame
trip_distance_dim = df.select('trip_distance').distinct() \
    .withColumn('trip_distance_id', monotonically_increasing_id()) 

# Create pickup_location_dim DataFrame
pickup_location_dim = df.select('pickup_longitude', 'pickup_latitude') \
    .distinct() \
    .withColumn('pickup_location_id', monotonically_increasing_id())

# Create dropoff_location_dim DataFrame
dropoff_location_dim = df.select('dropoff_longitude', 'dropoff_latitude') \
    .distinct() \
    .withColumn('dropoff_location_id', monotonically_increasing_id())

# Create fact_table DataFrame
fact_table = df.join(passenger_count_dim, 'passenger_count') \
    .join(trip_distance_dim, 'trip_distance') \
    .join(rate_code_dim, 'RatecodeID') \
    .join(pickup_location_dim, ['pickup_longitude', 'pickup_latitude']) \
    .join(dropoff_location_dim, ['dropoff_longitude', 'dropoff_latitude']) \
    .join(payment_type_dim, 'payment_type') \
    .join(datetime_dim, ['tpep_pickup_datetime', 'tpep_dropoff_datetime']) \
    .select('VendorID', 'datetime_id', 'passenger_count_id', 'trip_distance_id', 'pickup_location_id',
            'dropoff_location_id', 'rate_code_id', 'payment_type_id', 'store_and_fwd_flag', 'fare_amount',
            'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 'improvement_surcharge', 'total_amount')

fact_table.show()
fact_table.count()

