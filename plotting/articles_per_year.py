
from utils import *
import matplotlib.pyplot as plt

data = readCSV('articles_per_year.csv')

data.sort(key=lambda row: row[0])

data = list(filter(lambda row: row[0] != '', data))

years = list(map(lambda row: int(row[0]), data))
counts = list(map(lambda row: int(row[1]), data))

plt.title('Article count by year')
plt.grid(axis='y', linestyle='dotted')
plt.bar(years, counts)

plt.savefig('articles_by_year.png', dpi=300)
