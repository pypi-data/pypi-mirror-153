
class ConfigBase:
    def updateSpark(self, spark):
        self.spark = spark

    def get_dbutils(self, spark):
        try:
            from pyspark.dbutils import DBUtils
            dbutils = DBUtils(spark)
        except ImportError:
            try:
                import IPython
                dbutils = IPython.get_ipython().user_ns["dbutils"]
            except ModuleNotFoundError:
                from prophecy.test.utils import ProphecyDBUtil
                dbutils = ProphecyDBUtil

        return dbutils