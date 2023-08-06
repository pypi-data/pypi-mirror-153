import pandas as pd
import numpy as np
import sys
from time import sleep
import matplotlib.pyplot as plt
import subprocess as sp
from sklearn.metrics import r2_score as r2
import matplotlib.patches as mpatches
import pandas

sp.call("wget https://raw.githubusercontent.com/code4fukui/covid19vaccine/main/data/20210609.csv", shell=True)
sp.call("cat 20210609.csv|sed '2,$s/,-/,/g' >new", shell=True)
sp.call("mv 20210609.csv", shell=True)
data = pd.read_csv('20210609.csv')
data.fillna(0, inplace=True)
sp.call("rm 20210609.csv", shell=True)

# print(data[:7])
dataDelete = data.iloc[range(125), :]
print(dataDelete)

# fig = plt.figure()
# fig.add_subplot(1, 1, 1)

print(dataDelete.plot())
print(plt.show())

# class main:
#     def main(self, gender, date=400, degree=7):
#         n = len(data[gender])
#         y = data[gender][n-date:n]
#         for i in y:
#             print(i)

#         x = np.arange(n-date, n)
#         valid = ~(np.isnan(x) | np.isnan(y))
#         model = np.poly1d(np.polyfit(x[valid], y[valid], degree))
#         date1 = data['data'][n-1]
#         x1 = np.arange(n-date, n+7)
#         y1 = model(x1)
#         ny1 = []

#         for i in y1:
#             if i < 0:
#                 i = 0
#             ny1.append(i)

#         x2 = np.arange(n-date, n)
#         y2 = model(x2)
#         r2s = round(r2(y, y2), 3)
#         plt.plot(x, y, 'k')
#         plt.plot(x1, ny1, 'b')
#         ax = plt.subplot()
#         handles, labels = ax.get_legend_handles_labels()
#         st = 'daily deaths in' + str(gender)+'\n'+str(date) + 'date from' + str(
#             date1)+'\n'*str(degree) + 'th regression\n' + str(r2s)
#         handles.append(mpatches.Patch(color='none', label=st))
#         plt.legend(handles=handles)
#         plt.savefig(gender+".png")
#         plt.show()


# gender = ""
# date = 400

# if len(sys.argv) == 1:
#     print('country name is needed!')
#     sys.exit()
# if len(sys.argv) == 2:
#     if sys.argv[1] in data.columns:
#         country = str(sys.argv[1])
#     else:
#         print('correct country name!')
#         sys.exit()
# if len(sys.argv) == 3:
#     if sys.argv[1] in data.columns:
#         country = str(sys.argv[1])
#         if int(sys.argv[2]) > len(data[country]):
#             print('use smaller days')
#             sys.exit()
#         else:
#             days = int(sys.argv[2])
#     else:
#         print('correct country name')
#         sys.exit()
# if len(sys.argv) == 4:
#     if sys.argv[1] in data.columns:
#         country = str(sys.argv[1])
#         if int(sys.argv[2]) > len(data[country]):
#             print('use sampller days')
#             sys.exit()
#         else:
#             days = int(sys.argv[2])
#             if int(sys.argv[3]) > 4:
#                 degree = int(sys.argv[3])
#             else:
#                 print('use higher degree number')
#                 sys.exit()
#     else:
#         print('correct country name')
#         sys.exit()
# m = main()
# m.main(gender=gender, date=date)
