#https://datatofish.com/line-chart-python-matplotlib
# import pandas as pd
# import matplotlib.pyplot as plt



# df=pd.read_csv("output/measure_PSA_test_total.csv").dropna()
# #pd.read_csv("output/measure_PSA_test_long_total.csv").dropna()
# df.to_csv(r"output/PSA_test_total_table.csv")

# plt.plot(df['date'], df['had_PSA_test'], color='red', marker='o')
# plt.title('Number os PSA tests per month', fontsize=14)
# #May resample dates and re-write x label axis
# plt.xlabel('Month (first day)', fontsize=14)
# plt.ylabel('PSA tests', fontsize=14)
# plt.grid(True)
# plt.savefig('output/PSA_tests_plot.jpg',bbox_inches='tight', dpi=150)
# plt.show()
# #fig1.write_html("output/PSA_tests_per_month.html")

# Error message at the end of running run_model:
#   File "c:\users\pjfol\anaconda3\lib\subprocess.py", line 516, in run
#     raise CalledProcessError(retcode, process.args,
# subprocess.CalledProcessError: Command '['docker', 'image', 'inspect', '--format', 'ok', 'ghcr.io/opensafely-core/python:analysis/PSA_graphs.py']' returned non-zero exit status 1.




#New 2021/10/11 - working in ypnb book locally, but gives error whem running model
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
#Alternative: from matplotlib import plyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['font.size'] = 14

import seaborn as sns
#%matplotlib inline

# df1_PSA_long=pd.read_csv(r'output/measure_PSA_test_long_total.csv')

df2_PSA_short=pd.read_csv(r'output/measure_PSA_test_total.csv')

# #https://pythonguides.com/matplotlib-plot-bar-chart
# plt.barh(df1_PSA_long.date,df1_PSA_long.had_PSA_test_long)

# plt.title('Tests per month, long SNOMED codelist (indicated by first day)')
# plt.ylabel('Month', fontsize=15)
# plt.xlabel('PSA  tests (long list)', fontsize=15)
# #plt.show() must be commented out otherwise graph if printed blank
# #See https://chartio.com/resources/tutorials/how-to-save-a-plot-to-a-file-using-matplotlib/ for explanations on options
# plt.savefig('ouptput/Tests_long_list.jpg',bbox_inches='tight')

#https://pythonguides.com/matplotlib-plot-bar-chart
plt.barh(df2_PSA_short.date,df2_PSA_short.had_PSA_test)

plt.title('Tests per month, short SNOMED codelist (indicated by first day)')
plt.ylabel('Month', fontsize=15)
plt.xlabel('PSA  tests (short list)', fontsize=15)
#plt.show() must be commented out otherwise graph if printed blank
#See https://chartio.com/resources/tutorials/how-to-save-a-plot-to-a-file-using-matplotlib/ for explanations on options
plt.savefig('output/Tests_short_list.jpg',bbox_inches='tight')