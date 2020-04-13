from utils import *
import matplotlib.pyplot as plt


data = readCSV('sample_popularity.csv')

years = [row[0] for row in data]
values = [float(row[1]) for row in data]



plt.bar(years, values)
# plt.show()
plt.savefig('sample_popularity.png', dpi=300)
