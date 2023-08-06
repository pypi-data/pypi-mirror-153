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

import logging
import os

import numpy as np
import pandas as pd
from config42 import ConfigManager

from .common_summary_diff_analyzer import CommonSummaryDiffAnalyzer


class CustomerSummaryDiffAnalyzer(CommonSummaryDiffAnalyzer):
    """
    贷款明细汇总差异分析类
    """

    def __init__(self, *, config: ConfigManager, diff_sheet_name: str, is_first_analyzer=False):
        super().__init__(config=config, diff_sheet_name=diff_sheet_name, is_first_analyzer=is_first_analyzer)

    def _pivot_result(self, *, group_key: str, group_name: str, result: pd.DataFrame) -> pd.DataFrame:
        logging.getLogger(__name__).info("数据透视 {}...".format(group_name))
        # 按待分析差异、按比较类型归类
        result = pd.pivot_table(
            result,
            values=self._diff_column_dict.keys(),
            columns=[self._target_compare_type_column_name],
            index=group_key,
            aggfunc=np.sum,
            fill_value=0,
        )
        # 添加合计行
        result.loc["合计"] = result.apply(lambda x: x.sum())
        # 调整比较项目（待分析差异列）的排序
        result.sort_index(
            axis=1,
            level=[0, 1],
            key=self._sort_compare_item_and_type,
            inplace=True,
        )
        return result

    def _after_calculated_difference(self, result: pd.DataFrame) -> pd.DataFrame:
        logging.getLogger(__name__).info("差异后分析...")
        # 没有的数据填充"-"
        result.fillna(0, inplace=True)
        # 处理比较类型的排序
        result[self._target_compare_type_column_name] = pd.Categorical(
            result[self._target_compare_type_column_name],
            self._compare_type_order
        )
        # 分组列名
        group_key = '分组'
        group_key = group_key + "(" + "/".join(self._index_column_names) + ")"
        first = True
        # 将分组列合并成一列
        for column_name in self._index_column_names:
            if first:
                result[group_key] = result[column_name]
            else:
                result[group_key] = result[group_key].astype(str).str.cat(result[column_name].astype(str), sep='/')
            first = False

        # 按机构分组
        file_appearance_count: dict = dict()
        column_name = self._branch_column_name
        grouped_df = result.groupby(column_name, dropna=False)
        for data in grouped_df[column_name]:
            group_name = data[0]
            output_filename = "{}-按{}拆分-{}.xlsx".format(self._sheet_name, column_name, group_name)
            # 如果文件已经存在，第一次出现的时候删除原来的文件
            if os.path.exists(output_filename) and output_filename not in file_appearance_count:
                os.remove(output_filename)
            # 如果文件已经存在，则采用追加的模式
            mode = 'a' if os.path.exists(output_filename) else 'w'
            # 如果Sheet已经存在则替换原有的Sheet
            replace_strategy = 'replace' if mode == 'a' else None
            with pd.ExcelWriter(output_filename, mode=mode, if_sheet_exists=replace_strategy) as writer:
                sub_group = grouped_df.get_group(group_name)
                sub_result = self._pivot_result(group_key=group_key, group_name=group_name, result=sub_group)
                sub_result.to_excel(
                    writer,
                    sheet_name=self._target_sheet_name,
                )
                file_appearance_count[output_filename] = 1

        result = self._pivot_result(group_key=group_key, group_name='ALL', result=result)
        return result
