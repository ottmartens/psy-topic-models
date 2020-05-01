
from utils import *
import matplotlib.pyplot as plt

data = readCSV('coherences_2.csv')


topic_counts = [row[0] for row in data]
coherences = [ float(row[1][:5]) for row in data]

plt.grid(axis='y', linestyle='dotted')
plt.bar(topic_counts, coherences)
plt.xlabel("Topic count")
plt.ylabel("Coherence")

plt.savefig('coherences_2.png', dpi=300)
