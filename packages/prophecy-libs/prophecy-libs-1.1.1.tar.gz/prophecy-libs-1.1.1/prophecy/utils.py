from pyspark.sql import *


class ProphecyDataFrame:
    def __init__(self, df: DataFrame, spark: SparkSession):
        self.jvm = spark.sparkContext._jvm
        self.sqlContext = SQLContext(spark.sparkContext, sparkSession=spark, jsqlContext=spark._jwrapped)
        if type(df) == DataFrame:
            self.extended_dataframe = self.jvm.io.prophecy.libs.package.ExtendedDataFrameGlobal(df._jdf)
            self.dataframe = df
        else:
            self.extended_dataframe = self.jvm.io.prophecy.libs.package.ExtendedDataFrameGlobal(df._jdf)
            self.dataframe = DataFrame(df, self.sqlContext)

    def interim(self, subgraph, component, port, subPath, numRows, interimOutput, detailedStats=False):
        print("custom interim")
        result = self.extended_dataframe.interim(subgraph, component, port, subPath, numRows, interimOutput,
                                                 detailedStats)
        return DataFrame(result, self.sqlContext)

    def __getattr__(self, item: str):
        if item == "interim":
            self.interim

        if hasattr(self.extended_dataframe, item):
            return getattr(self.extended_dataframe, item)
        else:
            return getattr(self.dataframe, item)
