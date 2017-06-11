import json
from collections import defaultdict
f = open('data.json', 'r')
article_list = json.loads(f.read())
print len(article_list['response']['docs'])

count_source = defaultdict(int)
count_source_cat = defaultdict(int)
count_source_subcat=defaultdict(int)
Article_and_Title={}

Article_Extract = []

title_list=[]
f2=open('article_list101-500.csv','w')
f1=open('title_article100.csv','w')
f3=open('title_and_article100.csv', 'w')

for i in range(100):
    key=title_list.append(article_list['response']['docs'][i]['title'])
    val=Article_Extract.append(article_list['response']['docs'][i]['details'])
    Article_and_Title[key]=val

Article_and_Title = dict(zip(title_list, Article_Extract))
'''
for element in title_list:
    print>>f, element

for element in title_list:
    f2.write("%s\n" % element)
'''

for k, v in Article_Extract:
    f3.write("%s %s\n" % (k,v))
    

f3.close()

for i in article_list['response']['docs']:
    try:
        count_source[i['category']] +=1
    except:
        continue

#print 	count_source

for k, v in sorted(count_source.items()):
    print k,v

# run itemgetter code to sort by values

'''
for i in article_list['response']['docs']:
    if 'category' in i:
	    count_source_cat[i['category']] +=1

#print 	count_source

for k, v in sorted(count_source_cat.items()):
    print k,v
'''
'''
for current_article in article_list['response']['docs']:
    if 'sub_categories' in current_article:
	    for subcat in current_article['sub_categories']:
		    count_source_subcat[subcat] +=1

#print 	count_source_subcat

for k, v in sorted(count_source_subcat.items()):
    print k,v
'''

# can put attr ='author', 'tags', 'sub_categories'
attr='category'
for current_article in article_list['response']['docs']:
    if attr in current_article:
	    for current in current_article[attr]:
		    count_source_subcat[current] +=1

print 	len(count_source_subcat)
print len(count_source_subcat.keys())
sum=0
for k, v in count_source_subcat.items():
    sum = sum + v
print sum

print count_source_subcat.values().sum()
'''
for k, v in sorted(count_source_subcat.items()):
    try:
	    print k,v
    except:
	    continue

#print 	count_source_subcat
'''