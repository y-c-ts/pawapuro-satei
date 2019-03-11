import numpy as np
import pandas as pd
from data import AVILITY_LIST,AVILITY_DICT

class DataAggreagation(object):
    def __init__(self, request):
        self.request = request
        self.remain_point_arr = np.zeros(4)
        self.current_base_avility_arr = np.zeros(6)
        self.current_special_avility_arr = np.array([])
        self.avility_level_dict = {}
        self.run()
        
    def run(self):
        self.set_remain_point_list()
        self.set_current_base_avility()
        self.set_current_special_avility()
        self.set_current_avility_level()
        self.set_position()
        self.set_sense()
        self.set_subposition()
        self.set_limit_list()
        self.set_base_level_list()

    def set_sense(self):
        self.sense = self.request.form['sense']
    
    def set_position(self):
        self.position = self.request.form['position']
    
    def set_subposition(self):
        self.subposi = self.request.form['subposi']
    
    def set_base_level_list(self):
        meet = self.request.form['meet-level']
        power = self.request.form['power-level']
        speed = self.request.form['speed-level']
        kata = self.request.form['kata-level']
        syubi = self.request.form['syubi-level']
        hokyu = self.request.form['hokyu-level']
        self.base_level_list = np.array([0, meet, power, speed, kata, syubi, hokyu])

    def set_limit_list(self):
        meet = self.request.form['meet-upper']
        power = self.request.form['power-upper']
        speed = self.request.form['speed-upper']
        kata = self.request.form['kata-upper']
        syubi = self.request.form['syubi-upper']
        hokyu = self.request.form['hokyu-upper']
        self.base_limit_list = np.array([0, meet, power,speed,kata,syubi,hokyu])
    
    def set_remain_point_list(self):
        power = self.request.form['power-remaining']
        speed = self.request.form['speed-remaining']
        technic = self.request.form['technic-remaining']
        mental = self.request.form['mental-remaining']
        self.remain_point_arr = np.array([power,speed,technic,mental])

    def set_current_base_avility(self):
        ballistic = self.request.form['current-ballistic']
        meat = self.request.form['current-meat']
        power = self.request.form['current-power']
        speed = self.request.form['current-speed']
        shoulder = self.request.form['current-kata']
        defense = self.request.form['current-defense']
        error = self.request.form['current-error']
        self.current_base_avility_arr = np.array([ballistic, meat, power, speed, shoulder, defense, error])

    def set_current_special_avility(self):
        avility_str = self.request.form['get_avility_str']
        avility_list = avility_str.split('_')
        avility_list.pop(-1)
        self.current_special_avility_arr = np.array(avility_list)

    def set_current_avility_level(self):
        for avility in AVILITY_LIST:
            try:
                level = self.request.form['Radio_' + avility].split('option')[1]
                self.avility_level_dict[avility] = level
            except:
                pass
            try:
                level = self.request.form['Radio_gold_' + avility].split('option')[1]
                name = AVILITY_DICT[avility][-1]
                self.avility_level_dict[name] = level
            except:
                pass