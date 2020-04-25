
from utils import *
import matplotlib.pyplot as plt

data = readCSV('articles_per_year.csv')

data.sort(key=lambda row: row[0])

data = list(filter(lambda row: row[0] != '', data))

years = list(map(lambda row: int(row[0]), data))
counts = list(map(lambda row: int(row[1]), data))

plt.grid(axis='y', linestyle='dotted')
plt.bar(years, counts)

plt.savefig('article_count_by_year.png', dpi=300)
