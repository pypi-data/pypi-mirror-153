#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : quantzoo.
# @File         : viz
# @Time         : 2022/4/20 下午3:18
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://www.freesion.com/article/7211668549/
"""
http://www.javashuo.com/article/p-qbanlcme-ng.html
"""

from meutils.pipe import *

import cufflinks as cf
import tushare as ts

cf.set_config_file(theme='polar', offline=True, world_readable=True)


pro = ts.pro_api('c9e5aa127c4a416e2bb116d00234f5326ad018967c3a887c881a1c1f')


df_hs300 = pro.index_daily(ts_code='000300.SH')

df_hs300.iplot(x='trade_date', y=['open', 'close'])
