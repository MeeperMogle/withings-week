#!/usr/bin/python3

import os
from datetime import datetime, timedelta


def percentage(fpn):
    return round((fpn) * 10000) / 100


class Data:
    def __init__(self, data):
        split_data = data.split(',')
        self.valid = len(split_data) > 6
        
        if self.valid:
            self.created = datetime.strptime(split_data[0], '"%Y-%m-%d %H:%M:%S"')
            
            self.weight = float(split_data[1])
            
            self.fat_abs = float(split_data[2])
            self.fat_rel = percentage(self.fat_abs / self.weight)
            
            self.muscle_abs = float(split_data[4])
            self.muscle_rel = percentage(self.muscle_abs / self.weight)
            
            self.water_abs = float(split_data[5])
            
    def readable(self):
        return 'Created: {}, {}% fat, {}% muscle'.format(self.created, self.fat_rel, self.muscle_rel)


data_filename = list(filter(lambda s: s != 'cookies.txt' and not s.endswith('.sh') and not s.endswith('.py')
                                      and not s.startswith('matvaror') and not s.startswith('.idea'), os.listdir('.')))[0]

with open(data_filename, 'r', errors='ignore') as file_handle:
    lines = file_handle.readlines()
    
stop_at_html_lines = []
    
for line in lines:
    if "<html>" in line:
        break
    
    stop_at_html_lines.append(line)

data_points = []
    
week_ago = datetime.now() - timedelta(days=7)
    
done = 0
for line in stop_at_html_lines:
    if '2017-12' in line or '2018' in line:
        this_data = Data(line)
        
        if this_data.created > week_ago:
            data_points.append(this_data)
            
        done += 1
        
        if done == 10:
            break

weight_avg = 0
fat_abs_avg = 0
muscle_abs_avg = 0
            
for data in data_points:
    #print(data.readable())
    weight_avg += data.weight
    fat_abs_avg += data.fat_abs
    muscle_abs_avg += data.muscle_abs

num_datapoints = len(data_points)

try:
    weight_avg = weight_avg / num_datapoints
    fat_abs_avg = fat_abs_avg / num_datapoints
    muscle_abs_avg = muscle_abs_avg / num_datapoints

    # print('Average weight: {}, fat (kg): {}, muscle (kg): {}'.format(weight_avg, fat_abs_avg, muscle_abs_avg))
    lbm_avg = percentage((1 - (fat_abs_avg / weight_avg)) * weight_avg) / 100
    print('LBM of average: {}\nFat percentage: {}'.format(lbm_avg, percentage((weight_avg - lbm_avg) / weight_avg)))
except ZeroDivisionError:
    print('No data points in last week')

