import csv
from os import listdir, makedirs, system
from os.path import isfile, join, isdir
from PreProcessingDicts import page_dict, page_uid_dict, region_dict, region_vote_dict

fb_dir_path = "../FacebookAdLibraryReport_2020-06-10_US_last_90_days/regions/"
# fb_adviser = pd.read_csv("FacebookAdLibraryReport_2020-06-10_US_last_90_days/FacebookAdLibraryReport_2020-06-10_US_last_90_days_advertisers.csv")
files = listdir(fb_dir_path)
spend_df = {"UID": [], "REGION": [], "SPENT": []}
pages_df = {"UID": [], "NAME": []}
# open spending csv
spend_csv = open('../data/spending.csv', mode='w')
spend_writer = csv.writer(spend_csv, delimiter=',')
#open region csv
region_csv = open('../data/region.csv', mode='w')
region_writer = csv.writer(region_csv, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')
#page csv
page_csv = open('../data/page.csv', mode='w')
page_writer = csv.writer(page_csv, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')
#balance csv
balance_csv = open('../data/balance.csv', mode='w')
balance_writer = csv.writer(balance_csv, delimiter=',')

# Regions we skip because they do not have electoral votes.
SKIP_REGIONS = set([
    'Guam', 'American Samoa', 'Northern Mariana Islands', 'Puerto Rico',
    'Unknown', 'Virgin Islands (U.S.)'
])
skip_regions_ids = set([])
for r in SKIP_REGIONS:
    skip_regions_ids.add(region_dict[r])

#parse each file
for f in files:
    begin = f.rfind("_")
    end = f.rfind(".")
    region = f[begin+1:end]
    region_id = region_dict[region]
    data = dict()
    if region_id in skip_regions_ids:
        continue
    num_votes = region_vote_dict[region]
    with open(fb_dir_path+f) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)
        for row in reader:
            fbid = row[0]
            spent = row[-1]
            if int(fbid) in page_dict and spent != '\xe2\x89\xa4100' and spent != '≤100':
                uid = page_uid_dict[int(fbid)]
                if uid in data:
                    data[uid] += int(spent)
                else:
                    data[uid] = int(spent)
    # write uid and spent in region to csv
    for uid, value in data.items():
        # 'UID', 'REGION', 'SPENT'
        spend_writer.writerow([uid, region_id, value])
    #write region value to region csv
    # 'REGION_ID', 'REGION', 'VOTE_NUM'
    region_writer.writerow([region_id, "'{}'".format(region), num_votes])
#write to page and balance csv
for fbid, name in page_dict.items():
    uid = page_uid_dict[int(fbid)]
    # 'PAGE_ID', 'NAME', 'IS_OFFICIAL'
    page_writer.writerow([uid, "'{}'".format(page_dict[fbid]), 1])
    # each default campaign has 0 money left
    # 'UID', 'BALANCE'
    balance_writer.writerow([uid, 0])
region_csv.close()
spend_csv.close()
page_csv.close()
balance_csv.close()
