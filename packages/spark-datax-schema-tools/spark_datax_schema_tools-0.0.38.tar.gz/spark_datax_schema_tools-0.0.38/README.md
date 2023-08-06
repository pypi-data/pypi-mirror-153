# spark_datax_schema_tools


[![Github License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Updates](https://pyup.io/repos/github/woctezuma/google-colab-transfer/shield.svg)](pyup)
[![Python 3](https://pyup.io/repos/github/woctezuma/google-colab-transfer/python-3-shield.svg)](pyup)
[![Code coverage](https://codecov.io/gh/woctezuma/google-colab-transfer/branch/master/graph/badge.svg)](codecov)




spark_datax_schema_tools is a Python library that implements for dataX schemas
## Installation

The code is packaged for PyPI, so that the installation consists in running:
```sh
pip install spark-datax-schema-tools 
```


## Usage

wrapper take schemas for DataX

```sh

example1: (generate dummy_data)
================================
from spark_datax_schema_tools import generate_components
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[*]").appName("SparkAPP").getOrCreate()
df2 = generate_components(spark=spark,
                          path_excel="/content/Summary RQ22021-HF1.xlsx",
                          uuaa_name="NZTG",
                          table_name="t_nztg_trade_core_inf_bo_eom")

df2.show2()



example2: (generate transmission detail with schema json)
============================================================
from spark_datax_schema_tools import generate_transmission_holding
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[*]").appName("SparkAPP").getOrCreate()
df2 = generate_transmission_holding(spark=spark,
                                    uuaa_name="NZTG",
                                    table_name="t_nztg_trade_core_inf_bo_eom",
                                    table_version="0",
                                    frequency="monthly",
                                    group="CIB",
                                    solution_model="CDD",
                                    path_excel="Summary RQ22021-HF1.xlsx")


example3: (generate transmission detail without schema json)
============================================================
from spark_datax_schema_tools import generate_transmission_holding
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[*]").appName("SparkAPP").getOrCreate()
df2 = generate_transmission_holding(spark=spark,
                                    uuaa_name="NZTG",
                                    table_name="t_nztg_trade_core_inf_bo_eom",
                                    table_version="0",
                                    frequency="monthly",
                                    group="CIB",
                                    solution_model="CDD")
                                                                                                    
```
```sh
Parameter functions
===================
generate_transmission_holding:
  frequency: ["daily", "monthly"]
  group : ["CIB", "CLIENT_SOLUTIONS", "CORE_BANKING", "GLOBAL_DATA", "RISK_FINANCE"]
  solution_model: ["CIB", "CDD"]


```


## License

[Apache License 2.0](https://www.dropbox.com/s/8t6xtgk06o3ij61/LICENSE?dl=0).


## New features v1.0

 
## BugFix
- choco install visualcpp-build-tools



## Reference

 - Jonathan Quiza [github](https://github.com/jonaqp).
 - Jonathan Quiza [RumiMLSpark](http://rumi-ml.herokuapp.com/).
 - Jonathan Quiza [linkedin](https://www.linkedin.com/in/jonaqp/).
