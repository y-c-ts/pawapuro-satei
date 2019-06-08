# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, url_for
import pandas as pd
import numpy as np
import os
from preprocess import DataAggreagation
from optimize import MaximizeScore
from data import GOLD_LIST
import pandas as pd

app = Flask(__name__)
@app.route('/', methods=['GET'])
def render_form():
    return render_template('index.html')

@app.route('/', methods=["POST"])
def show_result():
    data_agg_obj = DataAggreagation(request)
    max_satei_obj = MaximizeScore(data_agg_obj)
    is_gold_default = get_is_gold_list(max_satei_obj.current_special_arr)
    is_gold_new = get_is_gold_list(max_satei_obj.add_special_arr)

    return render_template('output.html', final_avility_list = max_satei_obj.final_special_arr,
    final_base_list = max_satei_obj.final_base_arr.astype(np.int), is_gold_default = is_gold_default,
    is_gold_new = is_gold_new,
    add_avility_list = max_satei_obj.add_special_arr, default_avility_list = max_satei_obj.current_special_arr,
    add_base_list = max_satei_obj.update_base_arr)



def get_is_gold_list(avility_list):
    is_gold_list = []
    for avility in avility_list:
        if avility in GOLD_LIST:
            is_gold_list.append(1)
        else:
            is_gold_list.append(0)
    return is_gold_list



if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
