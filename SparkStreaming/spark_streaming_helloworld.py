import os, sys, time

SPARK_HOME="/usr/hdp/2.3.2.0-2950/spark-1.5.2-bin-hadoop2.6/"  
os.environ["SPARK_HOME"]=SPARK_HOME
os.environ["PYSPARK_PYTHON"]="/opt/anaconda/bin/python"
os.environ["PYSPARK_DRIVER_PYTHON"]="ipython"
os.environ["PYSPARK_DRIVER_PYTHON_OPTS"]="notebook"
os.environ["PYTHONPATH"]= os.path.join(SPARK_HOME, "python")+":" + os.path.join(SPARK_HOME, "python/lib/py4j-0.8.2.1-src.zip")
    
sys.path.insert(0, os.path.join(SPARK_HOME, "python"))
sys.path.insert(0, os.path.join(SPARK_HOME, 'python/lib/py4j-0.8.2.1-src.zip')) 
sys.path.insert(0, os.path.join(SPARK_HOME, 'bin') )

# import Spark Libraries
from pyspark import SparkContext, SparkConf, Accumulator, AccumulatorParam
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.mllib.linalg import Vector
from pyspark.streaming import StreamingContext


sc = SparkContext("local[4]", "Spark Streaming")
ssc = StreamingContext(sc, 1)

lines = ssc.socketTextStream("localhost", 9999)
words = lines.flatMap(lambda line: line.split(" "))
# Count each word in each batch
pairs = words.map(lambda word: (word, 1))
wordCounts = pairs.reduceByKey(lambda x, y: x + y)

# Print the first ten elements of each RDD generated in this DStream to the console
wordCounts.pprint()


ssc.start()             # Start the computation
ssc.awaitTermination()






#Kafka
# from pyspark.streaming.kafka import KafkaUtils
# directKafkaStream = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": brokers})