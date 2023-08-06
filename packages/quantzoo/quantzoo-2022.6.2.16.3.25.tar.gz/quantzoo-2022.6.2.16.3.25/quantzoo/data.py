#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : quantzoo.
# @File         : ak
# @Time         : 2022/6/2 下午3:09
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import akshare

# ME
from meutils.pipe import *
from meutils.cache_utils import *

cache_func = eval(os.environ.get("cache_func", 'lru_cache'))

# 设置缓存
for attr in dir(akshare):
    func = getattr(akshare, attr)
    if isinstance(func, Callable):
        setattr(akshare, attr, cache_func()(func))

if __name__ == '__main__':
    print(akshare.bond_cash_summary_sse())
