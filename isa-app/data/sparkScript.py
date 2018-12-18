from pyspark import SparkContext
import urllib.request
import urllib.parse
import urllib.error
import json

sc = SparkContext("spark://spark-master:7077", "RecommendedPacks")

# Each worker loads a piece of the data file
data = sc.textFile("/tmp/data/access.log", 2)

# Tell each worker to split each line of it's partition
pairs = data.map(lambda line: line.split("\t"))
pairs.persist()

# TODO: Use this so that Top 5 popular packs are displayed on home page
# Bring the data back to the master node so we can print it out
# Re-layout the data to ignore the user id
# pages = pairs.map(lambda pair: (pair[1], 1))
# Shuffle the data so that each key is only on one worker
# and then reduce all the values by adding them together
# count = pages.reduceByKey(lambda x,y: int(x)+int(y))
# output = count.collect()
# for page_id, count in output:
#     print ("page_id %s count %d" % (page_id, count))
# print ("Popular items done")

# Group data into (user_id, list of item ids they clicked on)
coclick_lists = pairs.groupByKey()
coclick_lists.persist()

output = coclick_lists.collect()
for list in output:
    print("(user_id = %s, clicks = { " % list[0], end='')
    for item in list[1]:
        print("%s, " % item, end='')
    print("})")

# Get the individual values for pageclicks (user_id, item)
coclick_values = coclick_lists.flatMapValues(lambda x: x)
# Join to get all pairs of values with matching keys (user_id, (item, item))
coclick_pairs = coclick_values.join(coclick_values)
# Remove identical pairs (item1, item1) and duplicates (item1, item2) == (item2, item1)
coclick_pairs = coclick_pairs.filter(lambda x: x[1][0] < x[1][1])
coclick_pairs.persist()

output = coclick_pairs.collect()
for tuple in output:
    print("(userid = %s, clicks = ( " % tuple[0], end='')
    for item in tuple[1]:
        print("%s, " % item, end='')
    print("))")

# Swap coclicks to keys ((item1, item2), 1)
coclick_key_pairs = coclick_pairs.map(lambda pair: (pair[1], 1))
# Reduce by key to get ((item1, item2), count of user_ids)
coclick_user_counts = coclick_key_pairs.reduceByKey(lambda l, r: int(l)+int(r))
# Filter out results with less than 3 users ((item1, item2), count_user_ids >= 3)
coclick_critical_counts = coclick_user_counts.filter(lambda pair: pair[1] >= 3)

# Remove count of user_ids (item1, item2)
# TODO: Sort by count, so we need to keep this field?
coclick_keys = coclick_critical_counts.map(lambda x: x[0])
# Get the list of recommended items for each ID (item1, list_of_recommended)
recommendations = coclick_keys.groupByKey().collect()

for r in recommendations:
    item_id = r[0]
    recommended_list = r[1]

    # Build recommendation to send to server.
    data = {
        'item_id': item_id,
        'recommended': [],
    }

    # Iterate over the recommended items with generated results.
    for item in recommended_list:
        data['recommended'].append(item)

    # Get current recommendation list for item.
    try:
        get_request = urllib.request.Request('http://models-api:8000/api/recommendations/%s/' % item_id)
        response = urllib.request.urlopen(get_request).read().decode("utf-8")
        current_recommendation = json.loads(response)
        for item in current_recommendation['recommended']:
            data['recommended'].append(item)

        # Remove the outdated version.
        delete_request = urllib.request.Request('http://models-api:8000/api/recommendations/%s/' % item_id, method='DELETE')
        urllib.request.urlopen(delete_request)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            # This is an expected case (no current recommendation list for item).
            pass

    # Feed into database as JSON.
    json_data = json.dumps(data).encode('utf-8')
    post_request = urllib.request.Request(
        url='http://models-api:8000/api/recommendations/',
        data=json_data,
        headers={'content-type': 'application/json'})
    urllib.request.urlopen(post_request)

sc.stop()
