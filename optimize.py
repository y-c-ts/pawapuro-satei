import pandas as pd
import numpy as np
import itertools
from data import AVILITY_DICT,AVILITY_LIST,IS_GOLD,GOLD_LIST,GOLD_TO_BLUE,SECOND_AVILITY_LIST,SECOND_TO_FAST,BASE_MAX
import time
from pulp import *
import math


DANDO_IDX = 0
MEET_IDX = 1
POWER_IDX = 2
SPEED_IDX = 3
KATA_IDX = 4
SYUBI_IDX = 5
HOKYU_IDX = 6

class MaximizeScore(object):
    def __init__(self,data_agg_obj):
        self.remain_point_arr = data_agg_obj.remain_point_arr.astype(np.int)
        self.current_base_arr = data_agg_obj.current_base_avility_arr.astype(np.int)
        self.current_special_arr = data_agg_obj.current_special_avility_arr
        self.avility_level_dict = data_agg_obj.avility_level_dict
        self.is_gold_dict = dict(zip(AVILITY_LIST,IS_GOLD))
        self.position = data_agg_obj.position
        self.sense = data_agg_obj.sense
        self.subposi = data_agg_obj.subposi
        self.base_limit_list = data_agg_obj.base_limit_list.astype(np.int)
        self.base_level_list = data_agg_obj.base_level_list.astype(np.int)

        self.avility_df = self.apply_sense(pd.concat([pd.read_csv('./data/野手青特能.csv',index_col=0),pd.read_csv('./data/野手金特能.csv',index_col=0)]))
        self.green_avility = pd.read_csv('./data/野手緑特能.csv', index_col=0)

        self.meet_df = self.apply_sense(pd.read_csv('./data/ミート.csv',index_col=0).fillna(0))
        self.dando_df = self.apply_sense(pd.read_csv('./data/弾道.csv',index_col=0).fillna(0))
        self.power_df = self.apply_sense(pd.read_csv('./data/パワー.csv',index_col=0).fillna(0))
        self.speed_df = self.apply_sense(pd.read_csv('./data/走力.csv',index_col=0).fillna(0))
        self.syubi_df = self.apply_sense(pd.read_csv('./data/守備.csv',index_col=0).fillna(0))
        self.kata_df = self.apply_sense(pd.read_csv('肩.csv',index_col=0).fillna(0))
        self.hokyu_df = self.apply_sense(pd.read_csv('./data/捕球.csv',index_col=0).fillna(0))

        self.run()


    def run(self):
        self.apply_avility_level()
        self.remove_acquired_avility()
        add_base_arr, add_special_arr, df = self.search_max_satei()
        self.add_special_arr = add_special_arr
        self.final_base_arr = np.max([self.current_base_arr,add_base_arr],axis=0)
        self.final_special_arr = np.append(self.current_special_arr, add_special_arr)
        self.update_base_arr = add_base_arr
        self.remove_low_level_avility()

    def remove_acquired_avility(self):
        self.remove_acquired_special_avility()
        self.meet_df = self.get_satei_df(self.meet_df, MEET_IDX)
        self.dando_df = self.get_satei_df(self.dando_df, DANDO_IDX)
        self.power_df = self.get_satei_df(self.power_df, POWER_IDX)
        self.speed_df = self.get_satei_df(self.speed_df, SPEED_IDX)
        self.kata_df = self.get_satei_df(self.kata_df, KATA_IDX)
        self.syubi_df = self.get_satei_df(self.syubi_df, SYUBI_IDX)
        self.hokyu_df = self.get_satei_df(self.hokyu_df, HOKYU_IDX)

    def remove_acquired_special_avility(self):
        for avility in self.current_special_arr:
            if avility in GOLD_LIST:
                blue_avility = GOLD_TO_BLUE[avility]
                avility_list = AVILITY_DICT[blue_avility]
                if len(avility_list) == 2:
                    self.current_special_arr = np.append(self.current_special_arr,blue_avility)
                elif len(avility_list) == 3:
                    self.current_special_arr = np.append(self.current_special_arr,[avility_list[0],avility_list[1]])
            elif avility in SECOND_AVILITY_LIST:
                fast_avility = SECOND_TO_FAST[avility]
                self.current_special_arr = np.append(self.current_special_arr, fast_avility)
        self.avility_df.drop(self.current_special_arr, inplace=True)
        self.avility_df.drop('威圧感', inplace=True)

    def _get_index_changing_value(self, satei_series):
        change_idx_list = []
        for i in satei_series.index[:-1]:
            if satei_series[i] != satei_series[i+1]:
                change_idx_list.append(i+1)
        return change_idx_list

    def preprocess_base_df(self, base_df, base_idx):
        base_df = self.apply_base_level(base_df, base_idx, self.base_level_list[base_idx])
        satei_series = base_df['査定値']
        change_idx = self._get_index_changing_value(satei_series)
        df = pd.DataFrame()
        for i in range(len(change_idx)):
            if i == 0:
                tmp_df = base_df.loc[0:change_idx[0]]
            else:
                tmp_df = base_df[change_idx[i -1]-1:change_idx[i]]
            satei = tmp_df['査定値'].iloc[-1] - tmp_df['査定値'].iloc[0]
            sum_point = tmp_df.iloc[1:].sum()
            sum_point['査定値'] = satei
            append_df = pd.DataFrame(sum_point).T
            append_df.index = [tmp_df.index[-1]]
            df = df.append(append_df)
        return df

    def get_satei_df(self, base_df, base_idx):
        base_satei_df = self.preprocess_base_df(base_df, base_idx)
        current_base = self.current_base_arr[base_idx]
        if (BASE_MAX[base_idx] <= current_base) or (self.base_limit_list[base_idx] <= current_base):
            return pd.DataFrame()
        else:
            if base_idx !=0:
                use_base_satei_df = base_satei_df.loc[current_base+1:self.base_limit_list[base_idx]]
            else:
                use_base_satei_df = base_satei_df.loc[current_base+1:]
            base_df.drop('査定値',inplace=True,axis=1)
            if len(use_base_satei_df) > 0:
                base_df.loc[current_base+1:use_base_satei_df.index[0]].sum()
                satei = use_base_satei_df['査定値'].iloc[0]
                use_base_satei_df.iloc[0,:] = base_df.loc[current_base+1:use_base_satei_df.index[0]].sum()
                use_base_satei_df['査定値'].iloc[0] = satei
            else:
                return pd.DataFrame()

        return use_base_satei_df

    def apply_avility_level(self):
        satei_series = self.avility_df['査定値']
        self.avility_df.drop('査定値',axis=1,inplace=True)
        for k,v in self.avility_level_dict.items():
            if v == '0':
                if (k in GOLD_LIST) and (k not in self.current_special_arr):
                    self.avility_df.drop(k,inplace=True)
                continue
            elif v=='1':
                self.avility_df = self.apply_one_avility_level(self.avility_df, k, 0.7)
            elif v=='2':
                self.avility_df= self.apply_one_avility_level(self.avility_df, k, 0.5)
            elif v=='3':
                self.avility_df = self.apply_one_avility_level(self.avility_df, k, 0.4)
            elif v=='4':
                self.avility_df = self.apply_one_avility_level(self.avility_df, k, 0.3)
            else:
                self.avility_df = self.apply_one_avility_level(self.avility_df, k, 0.2)
        self.avility_df.loc[:,['筋力','敏捷','技術','精神','変化球']] = self.avility_df.loc[:,['筋力','敏捷','技術','精神','変化球']].applymap(math.floor)
        self.avility_df['査定値'] = satei_series
        return self.avility_df

    def apply_one_avility_level(self, df, avility, level):
        if avility in GOLD_LIST:
            df.loc[avility] = df.loc[avility] * level
        else:
            avility_detail_list = AVILITY_DICT[avility]
            is_gold = self.is_gold_dict[avility]
            if is_gold == 1:
                if len(avility_detail_list) == 3:
                    df.loc[avility_detail_list[0]] = df.loc[avility_detail_list[0]] * level
                    df.loc[avility_detail_list[1]] = df.loc[avility_detail_list[1]] * level
                else:
                    df.loc[avility] = df.loc[avility] * level
            else:
                if len(avility_detail_list) == 2:
                    df.loc[avility_detail_list[0]] = df.loc[avility_detail_list[0]] * level
                    df.loc[avility_detail_list[1]] = df.loc[avility_detail_list[1]] * level
                else:
                    df.loc[avility] = df.loc[avility] * level
        return df

    def apply_base_level(self, base_df, base_idx ,level):
        if base_idx != 0:
            base_df.loc[:,['筋力','敏捷','技術','変化球','精神']] = \
            (base_df.loc[:,['筋力','敏捷','技術','変化球','精神']] * (1 - (level * 0.02))).applymap(math.floor)
        return base_df

    def _get_cumsum_df(self, base_df, base_name):
        if len(base_df) > 0:
            base_df = base_df.copy()
            base_df['index'] = base_df.index
            base_df['index'] = base_df['index'].astype(str)
            base_df['index'] = base_name + '_' + base_df['index']
            base_df.index = base_df['index']
            base_df.drop('index', inplace=True, axis=1)
        else:
            return pd.DataFrame()
        return base_df.cumsum()

    def apply_sense(self, df):
        if self.sense == 'sense':
            df.loc[:,['筋力','敏捷','技術','変化球','精神']] = (df.loc[:,['筋力','敏捷','技術','変化球','精神']] * 0.9).applymap(math.floor)
        elif self.sense == 'nonsense':
            df.loc[:,['筋力','敏捷','技術','変化球','精神']] = (df.loc[:,['筋力','敏捷','技術','変化球','精神']] * 1.1).applymap(math.floor)
        return df

    def _get_search_df(self):
        dando_cum = self._get_cumsum_df(self.dando_df,'dando')
        meet_cum = self._get_cumsum_df(self.meet_df, 'meet')
        power_cum = self._get_cumsum_df(self.power_df, 'power')
        speed_cum = self._get_cumsum_df(self.speed_df,'speed')
        kata_cum = self._get_cumsum_df(self.kata_df, 'kata')
        syubi_cum = self._get_cumsum_df(self.syubi_df, 'syubi')
        hokyu_cum = self._get_cumsum_df(self.hokyu_df, 'hokyu')
        search_df = pd.concat([self.avility_df, meet_cum, power_cum, hokyu_cum,
                                    dando_cum, kata_cum, syubi_cum, speed_cum])
        return search_df

    def _pick_base_avility(self, final_avility_list):
        delete_ids = []
        base_arr = np.zeros(7)
        for i, avility in enumerate(final_avility_list):
            if 'dando' in avility:
                base_arr[DANDO_IDX] = avility.split('_')[1]
                delete_ids.append(i)
            elif 'meet' in avility:
                base_arr[MEET_IDX] = avility.split('_')[1]
                delete_ids.append(i)
            elif 'power' in avility:
                base_arr[POWER_IDX] = avility.split('_')[1]
                delete_ids.append(i)
            elif 'speed' in avility:
                base_arr[SPEED_IDX] = avility.split('_')[1]
                delete_ids.append(i)
            elif 'kata' in avility:
                base_arr[KATA_IDX] = avility.split('_')[1]
                delete_ids.append(i)
            elif 'syubi' in avility:
                base_arr[SYUBI_IDX] = avility.split('_')[1]
                delete_ids.append(i)
            elif 'hokyu' in avility:
                base_arr[HOKYU_IDX] = avility.split('_')[1]
                delete_ids.append(i)

        return base_arr, np.delete(final_avility_list,delete_ids)


    def search_max_satei(self):
        df = self._get_search_df()
        avility_names = df.index
        m = LpProblem(sense = LpMaximize)
        df['x'] = [LpVariable('x%d' % i, cat = LpBinary) for i in range(len(df))]
        m += lpDot(df['査定値'], df['x'])
        self.remove_duplicate_avility(df, avility_names, m)
        m += lpDot(df['筋力'], df['x']) <= self.remain_point_arr[0]
        m += lpDot(df['敏捷'], df['x']) <= self.remain_point_arr[1]
        m += lpDot(df['技術'], df['x']) <= self.remain_point_arr[2]
        m += lpDot(df['精神'], df['x']) <= self.remain_point_arr[3]
        m += lpSum(df.loc[df.index.str.contains('dando')]['x']) <= 1
        m += lpSum(df.loc[df.index.str.contains('meet')]['x']) <= 1
        m += lpSum(df.loc[df.index.str.contains('power')]['x']) <= 1
        m += lpSum(df.loc[df.index.str.contains('speed')]['x']) <= 1
        m += lpSum(df.loc[df.index.str.contains('syubi')]['x']) <= 1
        m += lpSum(df.loc[df.index.str.contains('kata')]['x']) <= 1
        m += lpSum(df.loc[df.index.str.contains('hokyu')]['x']) <= 1
        self.remove_impossible_avility('インコース○','アウトコース○',avility_names, m, df)
        self.remove_impossible_avility('ローボールヒッター','ハイボールヒッター',avility_names, m, df)
        self.remove_impossible_avility('広角打法','プルヒッター',avility_names, m, df)

        m.solve()
        df['val'] = df.x.apply(lambda v: value(v))
        get_avility_arr = df[df.val == 1].index
        print(df[df.val == 1].sum())
        base_arr, final_avility_arr = self._pick_base_avility(get_avility_arr)
        return base_arr, final_avility_arr,df

    def remove_impossible_avility(self, avility1, avility2, avility_names, lp_obj, df):
        if avility1 in avility_names and avility2 in avility_names:
            lp_obj += lpSum(df.loc[[avility1,avility2]]['x']) <= 1
        elif avility1 in avility_names:
            lp_obj += lpSum(df.loc[[avility1]]['x']) <= 0
        elif avility2 in avility_names:
            lp_obj += lpSum(df.loc[[avility2]]['x']) <= 0

    def remove_duplicate_avility(self, df, avility_list, lp_obj):
        for avility in avility_list:
            if avility in GOLD_LIST:
                blue_avility = GOLD_TO_BLUE[avility]
                one_avility_list = AVILITY_DICT[blue_avility]
                one_avility_df = df.loc[one_avility_list].dropna()
                length = len(one_avility_df)
                if length == 3:
                    df.loc[one_avility_list,:] = df.loc[one_avility_list,:].cumsum()
                    lp_obj += lpSum(df.loc[one_avility_list]['x']) <= 1
                elif length == 2:
                    if len(one_avility_list) == 3:
                        df.loc[one_avility_list[1:],:] = df.loc[one_avility_list[1:],:].cumsum()
                        lp_obj += lpSum(df.loc[one_avility_list[1:]]['x']) <= 1
                    else:
                        df.loc[one_avility_list,:] = df.loc[one_avility_list,:].cumsum()
                        lp_obj += lpSum(df.loc[one_avility_list]['x']) <= 1

    def remove_low_level_avility(self):
        for avility in self.add_special_arr:
            if avility in GOLD_LIST:
                blue_avility = GOLD_TO_BLUE[avility]
                one_avility_list = AVILITY_DICT[blue_avility]
                for av in one_avility_list[:-1]:
                    if av in self.current_special_arr:
                        del_idx = np.where(self.current_special_arr == av)[0][0]
                        self.current_special_arr = np.delete(self.current_special_arr,del_idx)
