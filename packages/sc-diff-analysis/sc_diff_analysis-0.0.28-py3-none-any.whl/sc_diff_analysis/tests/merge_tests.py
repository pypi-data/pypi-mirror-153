#  The MIT License (MIT)
#
#  Copyright (c) 2022. Scott Lau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import pandas as pd


def func(x, y):
    if '投放' in y:
        return x if x > 0 else 0
    elif '还款' in y:
        return -x if x < 0 else 0
    return x


result = pd.DataFrame(
    [
        ["张三", '分营', '较昨日', 1, 1, -2, 3],
        ["张三", '分营', '较昨日投放', 0, 0, 0, 0],
        ["张三", '分营', '较昨日还款', 0, 0, 0, 0],
        ["张三", '分营', '较上周', 2, 2, -2, 3],
        ["张三", '分营', '较上周投放', 0, 0, 0, 0],
        ["张三", '分营', '较上周还款', 0, 0, 0, 0],
        ["张三", '分营', '较上月', 3, 1, -3, 4],
        ["张三", '分营', '较上月投放', 0, 0, 0, 0],
        ["张三", '分营', '较上月还款', 0, 0, 0, 0],
        ["李四", '南沙', '较昨日', -4, -2, -2, 4],
        ["李四", '南沙', '较昨日投放', 0, 0, 0, 0],
        ["李四", '南沙', '较昨日还款', 0, 0, 0, 0],
        ["李四", '南沙', '较上周', -5, 2, -2, 3],
        ["李四", '南沙', '较上周投放', 0, 0, 0, 0],
        ["李四", '南沙', '较上周还款', 0, 0, 0, 0],
        ["李四", '南沙', '较上月', 6, 1, -3, 4],
        ["李四", '南沙', '较上月投放', 0, 0, 0, 0],
        ["李四", '南沙', '较上月还款', 0, 0, 0, 0],
        ["王五", '江湾', '较昨日', -7, 5, -3, 2],
        ["王五", '江湾', '较昨日投放', 0, 0, 0, 0],
        ["王五", '江湾', '较昨日还款', 0, 0, 0, 0],
        ["王五", '江湾', '较上周', 8, 9, -7, 3],
        ["王五", '江湾', '较上周投放', 0, 0, 0, 0],
        ["王五", '江湾', '较上周还款', 0, 0, 0, 0],
        ["王五", '江湾', '较上月', 9, 6, -2, 4],
        ["王五", '江湾', '较上月投放', 0, 0, 0, 0],
        ["王五", '江湾', '较上月还款', 0, 0, 0, 0],
    ],
    columns=['姓名', '机构', '比较类型', '按揭', '消费', '秒贷', '经营'],
)
print("result", result)
result2 = result.copy()
# result2.drop(index=result2.loc[(result2['比较类型'].str.contains('投放')) | (result2['比较类型'].str.contains('还款'))].index, inplace=True)
print("result2", result2)
result_merge = result.merge(
    result2,
    on=['姓名', '机构']
)
df4 = result_merge.copy()
# print(result_merge)

# print('投放', result_merge)

result_merge.drop(
    index=result_merge.loc[
        (result_merge['比较类型_x'].str.contains('投放'))
        | (result_merge['比较类型_x'].str.contains('还款'))
        ].index,
    inplace=True
)

df5 = result_merge.copy()
result_merge = result_merge[
    result_merge.apply(
        lambda x: x['比较类型_x'] in x['比较类型_y'],
        axis=1,
    )
]
# result_merge.drop(
#     index=result_merge.loc[
#         result_merge['比较类型_y'].str.startswith(result_merge['比较类型_x'].str)].index,
#     inplace=True
# )

# result_merge.drop(index=result_merge.loc[result_merge['比较类型_y'].isin(['昨日'])].index, inplace=True)
# print(result_merge)


result_merge['按揭_y'] = result_merge.apply(lambda x: func(x['按揭_x'], x['比较类型_y']), axis=1)
result_merge['消费_y'] = result_merge.apply(lambda x: func(x['消费_x'], x['比较类型_y']), axis=1)
result_merge['秒贷_y'] = result_merge.apply(lambda x: func(x['秒贷_x'], x['比较类型_y']), axis=1)
result_merge['经营_y'] = result_merge.apply(lambda x: func(x['经营_x'], x['比较类型_y']), axis=1)

result_merge.drop(
    columns=['比较类型_x', '按揭_x', '消费_x', '秒贷_x', '经营_x'], inplace=True
)
result_merge.rename(
    columns={
        '比较类型_y': '比较类型',
        '按揭_y': '按揭',
        '消费_y': '消费',
        '秒贷_y': '秒贷',
        '经营_y': '经营',
    }, inplace=True
)
print("result_merge", result_merge)
