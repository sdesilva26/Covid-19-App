#!/bin/bash
cd ~/Documents/Repositories/Portfolio/Covid_19_Plots/
git checkout master
~/anaconda3/envs/covid19/bin/python ./scripts/data_script.py "./data/COVID-19-total-announced-deaths.xlsx" > /tmp/data_script.log 2>&1
git add . &&
git commit -m "cron commit with updated data" &&
git push heroku &&
git push origin