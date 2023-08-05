#!/bin/bash

# for swl
mkdir -p /mnt/g/data/rrdata
cd /mnt/g/data/rrdata

wget -o SwClass.rar http://www.swsindex.com/pdf/SwClass2021/SwClass.rar

sudo apt install unrar
unrar e SwClass.rar /mnt/g/data/rrdata/swclass

cp  /mnt/g/data/rrdata/swclass/'最新个股申万行业分类(完整版-截至7月末).xlsx'  \
    /mnt/g/data/rrdata/stock_swclass.csv





