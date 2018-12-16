from pyspark import SparkContext

sc = SparkContext("spark://spark-master:7077", "RecommendedPacks")

data = sc.textFile("/tmp/data/access.log", 2)     # each worker loads a piece of the data file

pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition
pages = pairs.map(lambda pair: (pair[1], 1))      # re-layout the data to ignore the user id
count = pages.reduceByKey(lambda x,y: int(x)+int(y))        # shuffle the data so that each key is only on one worker
                                                       # and then reduce all the values by adding them together

output = count.collect()                          # bring the data back to the master node so we can print it out
for page_id, count in output:
    print ("page_id %s count %d" % (page_id, count))
print ("Popular items done")

# co-view recommendations

coclicks = pairs.groupByKey()     # Group data into (user_id, list of item ids they clicked on)
coclick_pairs = coclicks.map(lambda coclick: ((coclick[1], coclick[1]), coclick[0]))    # Transform into (user_id, (item1, item2))

output = coclick_pairs.collect()
for pages, user in output:
    print("page %s page %s user %d" % (pages[0], pages[1], user))

# Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2)
coclick_pair_to_user = coclick_pairs.groupByKey()

output = coclick_pair_to_user.collect()
for pages, users in output:
    print("page %s page %s users %d" % (pages[0], pages[1], users))

# Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
coclick_pair_counts = coclick_pair_to_user.map(lambda coclickCount: (coclickCount[0], len(coclickCount[1])))

output = coclick_pair_counts.collect()
for pages, count in output:
    print("page %s page %s count %d" % (pages[0], pages[1], count))

# Filter out any results where less than 3 users co-clicked the same pair of items
coclick_counts_filtered = coclick_pair_to_user.filter(lambda x: x[1] > 3)

# collect and print the output so we can have a look see
output = coclick_counts_filtered.collect()
for pages, count in output:
    print("page %s page %s count %d" % (pages[0], pages[1], count))
print("Recommendations done")

sc.stop()