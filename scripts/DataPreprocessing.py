#!/usr/bin/env python
# coding: utf-8

# In[30]:


import pandas as pd
from os import listdir
from os import makedirs
from os.path import isfile, join, isdir

fb_dir_path = "preprocessed/fb/"
google_dir_path = "preprocessed/google/"
if not isdir('preprocessed'):
    makedirs(fb_dir_path)
    makedirs(google_dir_path)


# In[31]:


fb_adviser = pd.read_csv("FacebookAdLibraryReport_2020-06-10_US_last_90_days/FacebookAdLibraryReport_2020-06-10_US_last_90_days_advertisers.csv")


# In[32]:


fb_adviser.head(5)


# In[33]:


campaigns = ['Joe Biden', 'Donald J. Trump', 'Democratic Governors Association (DGA)', 'Republican Governors Association (RGA)']
fb_campaign_adviser = fb_adviser[fb_adviser['Page Name'].isin(campaigns)]
fb_campaign_adviser.to_csv(fb_dir_path + 'fb_campaign_advisers.csv', index = False)


# In[34]:


# ================== region ===================
fb_ca_adviser = pd.read_csv("FacebookAdLibraryReport_2020-06-10_US_last_90_days/regions/FacebookAdLibraryReport_2020-06-10_US_last_90_days_California.csv")
fb_ca_adviser.head(5)


# In[35]:


dir_path = "FacebookAdLibraryReport_2020-06-10_US_last_90_days/regions/"
files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]


# In[36]:


fb_regoin_advisers = []
for file_name in files:
    region = file_name.split('_')[-1][:-4]
    fb_region_advisor = pd.read_csv(dir_path + file_name)
    fb_region_advisor = fb_region_advisor[fb_region_advisor['Page Name'].isin(campaigns)]
    fb_region_advisor.to_csv(fb_dir_path + "fb_campaign_advisers_" + region + ".csv", index = False)


# In[37]:


# ====== google ===== 
# democratic national committee not in the dataset, so i just filter based on Regions
# select rows only with Regions == 'US'
google_advertiser_stats = pd.read_csv("google-political-ads-transparency-bundle/google-political-ads-advertiser-stats.csv")
google_advertiser_stats = google_advertiser_stats.iloc[:,:7]
google_advertiser_stats = google_advertiser_stats[google_advertiser_stats['Regions'] == 'US']
google_advertiser_stats = google_advertiser_stats.sort_values(by = 'Spend_USD', ascending = False)
google_advertiser_stats.to_csv(google_dir_path + "google-political-ads-advertiser-stats.csv", index = False)
google_advertiser_stats.head(5)


# In[38]:


# names = google_advertiser_stats['Advertiser_Name'].unique()
# for i in names:
#     i = i.lower()
#     if 'trump' in i or 'joe' in i or 'democratic' in i or 'republican' in i:
#         print(i)


# In[39]:


# =============
# democratic national committee not in the dataset
# filter Advertiser_Name
advertisers = ["republican national committee", "donald j. trump for president, inc.",                "dnc services corp./dem. nat'l committee", "BIDEN FOR PRESIDENT"]
google_advertiser_weekly_spend = pd.read_csv("google-political-ads-transparency-bundle/google-political-ads-advertiser-weekly-spend.csv")
google_advertiser_weekly_spend = google_advertiser_weekly_spend.iloc[:,:5]
google_advertiser_weekly_spend = google_advertiser_weekly_spend.sort_values(by = 'Spend_USD', ascending = False)
google_advertiser_weekly_spend = google_advertiser_weekly_spend[google_advertiser_weekly_spend.Advertiser_Name.isin(advertisers)]
google_advertiser_weekly_spend.to_csv(google_dir_path + "google-political-ads-advertiser-weekly-spend.csv", index = False)
google_advertiser_weekly_spend.head(10)


# In[40]:


# names = google_advertiser_weekly_spend.Advertiser_Name.unique()
# for i in names:
#     i = i.lower()
#     if 'trump' in i or 'joe' in i or "nat'l" in i or 'republican' in i:
#         print(i)


# In[41]:


# ================
# democratic national committee not in the dataset, so i just filter based on Regions
# select rows only with Regions == 'US'
google_creative_stats = pd.read_csv("google-political-ads-transparency-bundle/google-political-ads-creative-stats.csv")


# In[42]:


google_creative_stats = google_creative_stats.iloc[:,:20]
google_creative_stats = google_creative_stats[google_creative_stats.Regions == 'US']
google_creative_stats.to_csv(google_dir_path + "google-political-ads-creative-stats.csv", index = False)
google_creative_stats.head()


# In[43]:


# ===========
google_geo_spend = pd.read_csv("google-political-ads-transparency-bundle/google-political-ads-geo-spend.csv")
google_geo_spend = google_geo_spend.iloc[:,:4]
google_geo_spend.to_csv(google_dir_path + "google-political-ads-geo-spend.csv", index = False)
google_geo_spend.head()


# In[44]:


# ===========
google_top_keywords = pd.read_csv("google-political-ads-transparency-bundle/google-political-ads-top-keywords-history.csv")
google_top_keywords.to_csv(google_dir_path + "google-political-ads-top-keywords-history.csv", index = False)
google_top_keywords.head()

