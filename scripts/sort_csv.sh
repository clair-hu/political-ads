#!/bin/bash
sort -k1 -n -t, -o ../data/region.csv ../data/region.csv
sort -k1 -n -t, -o ../data/page.csv ../data/page.csv
sort -k1 -n -t, -o ../data/balance.csv ../data/balance.csv
sort -k2,2 -k1,1 -n -t, -o ../data/spending.csv ../data/spending.csv