from pyspark import SparkContext

sc = SparkContext("spark://spark-master:7077", "RecommendedPacks")

# Each worker loads a piece of the data file
data = sc.textFile("/tmp/data/access.log", 2)

# Tell each worker to split each line of it's partition
pairs = data.map(lambda line: line.split("\t"))
pairs.persist()
# Re-layout the data to ignore the user id
pages = pairs.map(lambda pair: (pair[1], 1))
# Shuffle the data so that each key is only on one worker
# and then reduce all the values by adding them together
count = pages.reduceByKey(lambda x,y: int(x)+int(y))

# Bring the data back to the master node so we can print it out
# TODO: Use this so that Top 5 popular packs are displayed on home page
#output = count.collect()
#for page_id, count in output:
#    print ("page_id %s count %d" % (page_id, count))
#print ("Popular items done")

# Group data into (user_id, list of item ids they clicked on)
coclicks = pairs.groupByKey()
item_lists = coclicks.map(lambda pair: pair[1])
# Get all possible pairings of items
permutations = item_lists.cartesian(item_lists)

output = coclicks.collect()
for list in output:
    print("List for user %s below: " % list[0])
    for item in list[1]:
        print("item %s" % item)
"""

# Remove duplicates and pairs of same item
permutations.filter(lambda tuple: tuple[0] < tuple[1])
# Transform into (user_id, (item1, item2))
coclick_pairs = coclicks.map(lambda group: (group[0], (group[1] > group[1])))

# Collect and print the output
output = coclick_pairs.collect()
for user, pair in output:
    print("user %s item1 %s item2 %s" % (user, pair[0], pair[1]))

# Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2)
coclick_pair_to_user = coclick_pairs.groupByKey()

# Collect and print the output
output = coclick_pair_to_user.collect()
for pages, count in output:
    print("page %s page %s count %d" % (pages[0], pages[1], count))

# Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
coclick_pair_counts = coclick_pair_to_user.map(lambda coclickCount: (coclickCount[0], len(coclickCount[1])))

# Collect and print the output
output = coclick_pair_counts.collect()
for pages, count in output:
    print("page %s page %s count %d" % (pages[0], pages[1], count))

# Filter out any results where less than 3 users co-clicked the same pair of items
coclick_counts_filtered = coclick_pair_to_user.filter(lambda x: x[1] > 3)

# Collect and print the output so we can have a look see
output = coclick_counts_filtered.collect()
for pages, count in output:
    print("page %s page %s count %d" % (pages[0], pages[1], count))
print("Recommendations done")
"""
sc.stop()
