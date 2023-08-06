import pandas as pd
from ab_testing import ABTest

df = pd.read_csv('Docs/ab_data.csv',usecols=['user_id','group','converted'])

ab_obj = ABTest(df,response_column='converted',group_column='group')

print(ab_obj.conversion_rate())
# ab_object.conversion_rate() -> DF with result  


# ab_object.graph()

# ab_object.significant_test() -> p-value -> Ans with reject

# ab_object.report(path = "")


# Data Set Random from email testing - Fake data set

# Link to Use
"""
-Dataset https://www.kaggle.com/zhangluyuan/ab-testing?select=ab_data.csv

-ABTest https://towardsdatascience.com/ab-testing-with-python-e5964dd66143

"""
