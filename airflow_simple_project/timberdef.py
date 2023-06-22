from pyspark.sql import SparkSession
from pyspark.sql.functions import format_number

def spark_code():
    

    spark = SparkSession \
    .builder \
    .appName("maarketdata") \
    .master("local[1]") \
    .getOrCreate()
    
    schema = "date DATE, open FLOAT, high FLOAT, low FLOAT, close FLOAT, volume FLOAT, adj_close FLOAT"

    data = spark.read.csv("/home/saksham/timberland_stock.csv",
                          schema=schema,sep=",",header=True)

    output_path = "/home/saksham/outputfiles/"
    # data.printSchema()
    # data.show()

    data.createOrReplaceTempView("stock")
    # What day had the Peak High in Price?
    df=spark.sql("select date from stock where high=(select max(high) from stock)")
    df_output=output_path+"df_output.csv"
    df.write.csv(df_output, header=True, mode="overwrite")
    # df.show()
    # What is the mean of the Close column?
    # What is the max and min of the Volume column?

    # df2 = spark.sql("select round(avg(close),2)as mean_close, round(max(volume),2) as max_vol, \
    #                 round(min(volume),2) \
    #                 as min_vol from stock")
    df2 = spark.sql("select format_number(avg(close),2)as mean_close, format_number(max(volume),2) as max_vol, \
                format_number(min(volume),2) \
                as min_vol from stock")
    df2_output=output_path+"df2_output.csv"
    df2.write.csv(df2_output, header=True, mode="overwrite")
    # df2.show()

    # How many days was the Close lower than 60 dollars?
    df3 = spark.sql("select count(date)as close_cnt from stock where close < 60")
    df3_output=output_path+"df3_output.csv"
    df3.write.csv(df3_output, header=True, mode="overwrite")
    # df3.show()


    # What percentage of the time was the High greater than 80 dollars ?

    df4 = spark.sql("select count(date) as high_cnt from stock where high > 80")
    # df4.show()

    df4.createOrReplaceTempView("t1")


    df5 = spark.sql("select count(*) as total_cnt from stock")
    # df5.show()

    df5.createOrReplaceTempView("t2")

    df6 = spark.sql(" select t1.high_cnt,t2.total_cnt, \
                    format_number((t1.high_cnt/t2.total_cnt * 100),2) as percentage from t1 full outer join t2")
    df6_output=output_path+"df6_output.csv"
    df6.write.csv(df6_output, header=True, mode="overwrite")
    # df6.show()

    # What is the Pearson correlation between High and Volume?
    # answer: Pearson correlation is a statistical measure that quantifies the linear relationship 
    # between two continuous variables determines strength -- direction - linear association ,coefficient r range[-1,1].
    #  r close to 1 strong relation it high increase then volume also will increase and vice versa

    df7 = spark.sql("select format_number(corr(high,volume),2) as relation from stock")
    df7_output=output_path+"df7_output.csv"
    df7.write.csv(df7_output, header=True, mode="overwrite")
    # df7.show()

    # What is the max High per year?

    df8 = spark.sql("select max(high) as max_high, YEAR(date) as year from stock group by YEAR(date) order by YEAR(date)")
    df8_output=output_path+"df8_output.csv"
    df8.write.csv(df8_output, header=True, mode="overwrite")
    # df8.show()

    # What is the average Close for each Calendar Month?

    df9 = spark.sql("select format_number(avg(close),2) as avg_close, MONTH(date) as month \
                    from stock group by MONTH(date) order by MONTH(date)")
    
    df9_output=output_path+"df9_output.csv"
    df9.write.csv(df9_output, header=True, mode="overwrite")
    # df9.show()

    # df10 = spark.sql("select format_number(avg(close),2) as avg_close, MONTH(date) as month \
    #                     ,YEAR(date) as year from stock group by MONTH(date),YEAR(date) \
    #                     order by MONTH(date),YEAR(date)")
    df10 = spark.sql("select format_number(avg(close),2) as avg_close, MONTH(date) as month \
                        ,YEAR(date) as year from stock group by MONTH(date),YEAR(date) \
                        order by YEAR(date),MONTH(date)")

    # df10.show()

    df10_output=output_path+"df10_output.csv"
    df10.write.csv(df10_output, header=True, mode="overwrite")