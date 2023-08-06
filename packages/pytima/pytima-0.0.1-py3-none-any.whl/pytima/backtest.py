# -*- coding: utf-8 -*-
# @author: Wenting Tu
# @email: wtugmail@163.com
# @date: 2022/06

"""
==========
backtest: Backtest Tools
==========
"""

import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
from pytima.datasets import TimaDataset

def get_changed_time(ori_time, gap_val, gap_type):
    """负责基于某个ds，得到增加/减少某些gap的ds"""
    '''
    :param ori_time: 初始ds
    :param gap_val: gap值, e.g., 3
    :param gap_type: string, 'Month', 'Day', 'Week'
    :return: string, 变化后的ds
    '''
    assert gap_type in ['Month', 'Day', 'Week']
    ori_time_datetime = pd.to_datetime(ori_time, format='%Y-%m-%d')
    changed_time = None
    if gap_type == 'Month':
        changed_time = str(ori_time_datetime + relativedelta(months=gap_val))[:10]
    elif gap_type == 'Day':
        changed_time = str(ori_time_datetime + relativedelta(days=gap_val))[:10]
    elif gap_type == 'Week':
        changed_time = str(ori_time_datetime + relativedelta(weeks=gap_val))[:10]
    return changed_time

def generate_backtest_datasets(pytima_dataset, fixed_steps, time_min=None, time_max=None):
    if time_min==None:
        time_min = pytima_dataset.series_data['Time'].min()
    if time_max==None:
        time_max = pytima_dataset.series_data['Time'].max()
    
    time_bucket = pytima_dataset.series_data['TimeBucket'].tolist()[0]

    if time_bucket == 'Week':
        forecast_time_list = pd.date_range(start=time_min, end=time_max,
                                         freq='W-MON').strftime('%Y-%m-%d').tolist()
    elif time_bucket == 'Month':
        forecast_time_list = pd.date_range(start=time_min, end=time_max,
                                         freq='MS').strftime('%Y-%m-%d').tolist()
    elif time_bucket == 'Day':
        forecast_time_list = pd.date_range(start=time_min, end=time_max,
                                         freq='D').strftime('%Y-%m-%d').tolist()
        
    horizen_time_list = []
    fp_list = []
    step_list = []
    for plan_time in forecast_time_list:
        for step in fixed_steps:
            forecast_point = get_changed_time(plan_time, -step, time_bucket)
            horizen_time_list.append(plan_time)
            fp_list.append(forecast_point)
            step_list.append(step)
    plan_horizon_df = pd.DataFrame()
    plan_horizon_df['Time'] = horizen_time_list
    plan_horizon_df['forecast_point'] = fp_list
    plan_horizon_df['step'] = step_list
    
    
    fcst_horizon_df_with_target = pd.DataFrame()
    

    for fcst_time, fcst_time_horizon in plan_horizon_df.groupby('Time'):
        series_data_subset = pytima_dataset.series_data[pytima_dataset.series_data.Time == fcst_time].copy()
        for horizon_ind in range(len(fcst_time_horizon)):
            fcst_df = series_data_subset.copy()
            fcst_df['forecast_point'] = fcst_time_horizon.iloc[horizon_ind].forecast_point
            fcst_df['step'] = fcst_time_horizon.iloc[horizon_ind].step
            fcst_horizon_df_with_target = fcst_horizon_df_with_target.append(fcst_df)
            
    pytima_backtest_datasets = {}
    for fp, horizen_data_fp in fcst_horizon_df_with_target.groupby('forecast_point'):
        pytima_backtest_datasets[fp] = TimaDataset()
        pytima_backtest_datasets[fp].series_data = pytima_dataset.series_data[pytima_dataset.series_data.Time < fp]
        pytima_backtest_datasets[fp].horizen_data = horizen_data_fp

    
    return pytima_backtest_datasets


def wmape(y_pred, y_true, include_zero_flag):
    """WMAPE Error"""
    sum_error = 0.0
    sum_true  =0.0
    sum_pred  =0.0
    for i in range(len(y_pred)):
        if np.isnan(y_true[i]): continue
        if not include_zero_flag:
            if y_true[i]==0.0: continue
        sum_true+=y_true[i]
        sum_pred+=y_pred[i]
        sum_error+=abs(float(y_pred[i]) - float(y_true[i]))
    sum_true = max([1.0, sum_true])
    return sum_error/sum_true


def bias(y_pred, y_true, include_zero_flag):
    """Bias Error"""
    sum_error = 0.0
    sum_true  =0.0
    sum_pred  =0.0
    for i in range(len(y_pred)):
        if np.isnan(y_true[i]): continue
        if not include_zero_flag:
            if y_true[i]==0.0: continue
        sum_true+=y_true[i]
        sum_pred+=y_pred[i]
        sum_error+=abs(float(y_pred[i]) - float(y_true[i]))
    sum_true = max([1.0, sum_true])
    return (sum_pred - sum_true)/sum_true


def mape(y_pred, y_true, include_zero_flag):
    """MAPE Error"""
    sum_ratio = 0.0
    for i in range(len(y_pred)):
        if np.isnan(y_true[i]): continue
        if not include_zero_flag:
            if y_true[i]==0.0: continue
        sum_ratio += abs(float(y_pred[i]) - float(y_true[i])) / max([1.0, y_true[i]])
    return sum_ratio / max(1.0, len(y_pred))

def evaluate_acc_bias(res_all, true_col, fcst_col, eval_dims=['DS'], error_metric=wmape, bias_metric=bias,
                      include_zero_flag=True, include_nan_flag=True, return_flag=False, true_thres=None, verbose=1):
    """Evaluation"""
    if not include_zero_flag:
        res_all_ = res_all[res_all[true_col]!=0.0].copy()

    if not include_nan_flag:
        res_all_ = res_all[~(np.isnan(res_all[fcst_col]))].copy()
    else:
        res_all_ = res_all.copy()
        res_all_.loc[(np.isnan(res_all[fcst_col])), fcst_col] = 0.0

    if true_thres is not None:
        res_all_ = res_all_[res_all_[true_col] > true_thres]

    acc_list = []
    bias_list = []
    group_list = []
    if verbose>0:
        print('GROUP', '\t' * (len(eval_dims)*2), '#UNIT', '\t', 'ACC', '\t\t', 'BIAS')

    if len(eval_dims)>0:
        res_groups = res_all_.groupby(eval_dims)
    else:
        res_groups = [('ALL', res_all_)]

    for group_k, res in res_groups:
        error = error_metric(res[fcst_col].tolist(), res[true_col].tolist(), include_zero_flag=True)
        bias = bias_metric(res[fcst_col].tolist(), res[true_col].tolist(), include_zero_flag=True)
        if verbose > 0:
            print(group_k, '\t', len(res), '\t', round(1.0 - error, 5), '\t', round(bias, 5))
        group_list.append(group_k)
        acc_list.append(round(1.0 - error, 5))
        bias_list.append(round(bias, 5))

    if return_flag:
        res = pd.DataFrame()
        res['group'] = group_list
        res['acc'] = acc_list
        res['bias'] = bias_list
        return res



