import os
os.environ["SPARK_HOME"] = "C:\\Users\\Walter\\Spark-Hadoop\\spark-2.3.1-bin-hadoop2.7"
os.environ["HADOOP_HOME"]="C:\\winutils"

from pyspark import *

def unionSet(friendlistA, friendlistB):
    #Find the union of two sets
    #Spark union does not perform mathmatical set union, so must make out own

    #append one friends list to the other, including all duplicates
    combinedList = friendlistA + friendlistB

    #create a mathmatical union by iterating through friendListA components in the combinedList
    #and adding them to the new set if they appear in both
    unionList = set([friendlistA for friendlistA in combinedList if combinedList.count(friendlistA) > 1])

    return unionList

def orderkeys(user, friendsList):
    #order friendsList by keys

    #temporary holding list
    holder = []
    friends = friendsList.split(' ')


    if int(friends[0]) < int(user):
        holder.append(int(friends[0]))
        holder.append(int(user)) #user id int is lower than friends, re-order
    else:
        holder.append(int(user))
        holder.append(int(friends[0])) #usr id int is greater than friends, keep in normal order


    sortedFriends = ' '.join(str(user) for user in holder)

    return sortedFriends

if __name__ == "__main__":
    sc = SparkContext.getOrCreate()
    lines = sc.textFile('facebook_combined2.txt', 1)

    # #reduces all rows of user friend pair in single user friendsList pairs
    # #Unable to get this working correctly
    # lines = lines.map(lambda x, y: (x, y)).reduceByKey(lambda x, y: (x + ',' + y))

    #flatMaps the user friendsList pairs, then reduces them into their mathmatical union set to get mutualfriends
    mutualFriends = lines.flatMap(lambda friends: [(orderkeys(user, friends), (friends.split(' '))[1:])
                                              for user in (friends.split()[1:])]) \
        .reduceByKey((lambda x, y: unionSet(x, y)))

    #save output as file
    print(mutualFriends)
    mutualFriends.saveAsTextFile("output")
    sc.stop()