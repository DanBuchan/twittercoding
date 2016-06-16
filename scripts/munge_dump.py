import csv
from collections import defaultdict
import pprint
pp = pprint.PrettyPrinter(indent=4)


def return_code(category, codes, out_str):
    found = False
    code = ""
    for line in codes:
        #print(line)
        if category in line[5]:
            found = True
            code = ","+line[6]
    if found is True:
        out_str += code
    else:
        out_str += ",-"
    return(out_str)

tweets = defaultdict(list)
with open('/Users/dbuchan/Code/twittercoding/test_dump.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        print(row[0])
        tweets[row[0]].append(row)

# pp.pprint(tweets)
# print("tweet_id,username,label,user,T1: Multimedia,T2: Type of tweet,"
#       "T3: Interaction with,T4: Is there an @mention?,T5: Source of @mention,"
#       "T6a: Personal?,T6b: Political?,T7: Personal topic,T8: Political Topic,"
#
for tweet_id in tweets:
    codes = tweets[tweet_id]
    pp.pprint(codes)
    out_str = tweet_id+","+tweets[tweet_id][0][1]+","+tweets[tweet_id][0][2] \
              + ","+tweets[tweet_id][0][4]
    out_str = return_code("T1:", codes, out_str)
    out_str = return_code("T2:", codes, out_str)
    out_str = return_code("T3:", codes, out_str)
    out_str = return_code("T4:", codes, out_str)
    out_str = return_code("T5:", codes, out_str)
    out_str = return_code("T6a:", codes, out_str)
    out_str = return_code("T6b:", codes, out_str)
    out_str = return_code("T7:", codes, out_str)
    out_str = return_code("T8:", codes, out_str)
    out_str = return_code("T9:", codes, out_str)
    out_str = return_code("T10:", codes, out_str)

    print(out_str)
