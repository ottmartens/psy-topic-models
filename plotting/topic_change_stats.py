import csv


with open('topic_proportions_per_year.csv', 'r') as file:
    rows = list(csv.reader(file))
    file.close()



result = []

for topic in range(1, 101):

    prop_1979 =  float(rows[0][topic])
    prop_2019 = float(rows[-2][topic])

    abs_change = prop_2019 - prop_1979

    abs_change_percent = abs_change / prop_1979 * 100

    overall_change = 0

    last_prop = None
    topic_props = []

    for row in rows[:-1]:

        year = int(row[0])

        topic_prop = float(row[topic])
        topic_props.append(topic_prop)

        if last_prop is not None:
            if topic_prop > last_prop:
                overall_change += topic_prop - last_prop
            else:
                overall_change += last_prop - topic_prop

        last_prop = topic_prop
    

    biggestClimbPercent = 0
    biggestDescPercent = 0
    for first in topic_props:
        for second in topic_props[topic_props.index(first):]:

            climb = second - first
            climbPercent = climb / first

            if climbPercent > biggestClimbPercent:
                biggestClimbPercent = climbPercent
            

            descent = first - second
            descentPercent = descent / first

            if descentPercent > biggestDescPercent:
                biggestDescPercent = descentPercent


    result.append([topic, prop_1979, prop_2019, abs_change, abs_change_percent, overall_change, biggestClimbPercent, biggestDescPercent])

with open('topic_change_stats.csv', 'w') as resultFile:
    writer = csv.writer(resultFile)
    writer.writerow(['topic_no', '1979_prop', '2019_prop', 'abs_change', 'abs_change_percent', 'overall_change', 'max_ascent_percent', 'max_descent_percent'])

    writer.writerows(result)

    resultFile.close()


sorted_by_abs_change_percent = sorted(result, key=lambda row: row[4], reverse=True)

print('Biggest rise from 1979 to 2019')

for row in sorted_by_abs_change_percent[:5]:
    print(row[0], row[4])

print('Biggest fall from 1979 to 2019')

sorted_by_abs_change_percent.reverse()

for row in sorted_by_abs_change_percent[:5]:
    print(row[0], row[4])

print('Most varying popularity')
sorted_by_overall_change = sorted(result, key=lambda row: row[5], reverse=True)
for row in sorted_by_overall_change[:5]:
    print(row[0], row[5])

print('Most stable (low variability in popularity)')
sorted_by_overall_change.reverse()
for row in sorted_by_overall_change[:5]:
    print(row[0], row[5])

print('Max climbers')
sorted_by_max_increase = sorted(result, key=lambda row: row[6], reverse=True)
for row in sorted_by_max_increase[:5]:
    print(row[0], row[6])


sorted_by_max_decrease = sorted(result, key=lambda row: row[7], reverse=True)
print('Max descenders')
for row in sorted_by_max_decrease[:5]:
    print(row[0], row[7])









       



