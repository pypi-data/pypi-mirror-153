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
from pandas import ExcelWriter

from .common_summary_diff_analyzer import CommonSummaryDiffAnalyzer


class XinkaSummaryDiffAnalyzer(CommonSummaryDiffAnalyzer):
    """
    心卡汇总差异分析类
    """

    def __init__(self, *, config: ConfigManager, diff_sheet_name: str, is_first_analyzer=False):
        self._branch_result_data = pd.DataFrame()
        self._branch_order = dict()
        super().__init__(config=config, diff_sheet_name=diff_sheet_name, is_first_analyzer=is_first_analyzer)

    def _read_config(self, *, config: ConfigManager):
        super()._read_config(config=config)
        # 选中需要处理的机构清单
        self._branch_selected_list = config.get("branch.selected_list")
        self._init_branch_orders()
        self._positive_column_name = config.get(
            "diff.customized_summary." + self._diff_sheet_name + ".positive_column_name")
        self._negative_column_name = config.get(
            "diff.customized_summary." + self._diff_sheet_name + ".negative_column_name")
        self._branch_column_name = config.get(
            "diff.customized_summary." + self._diff_sheet_name + ".branch_column_name")
        new_orders = self._compare_type_order.copy()
        for order in self._compare_type_order:
            if "较" in order:
                order_index = new_orders.index(order)
                # 添加投放与还款比较类型
                new_orders.insert(order_index + 1, order + self._positive_column_name)
                new_orders.insert(order_index + 2, order + self._negative_column_name)
        self._compare_type_order = new_orders.copy()

    def _init_branch_orders(self):
        index = 1
        for branch in self._branch_selected_list:
            self._branch_order[branch] = index
            index = index + 1

    def _sort_branch_rows(self, branches):
        return branches.map(self._branch_order)

    def _init_compare_types(self):
        logging.getLogger(__name__).info("初始化比较类型...")
        index = 1
        for compare_type in self._compare_type_order:
            self._compare_type_order_dict[compare_type] = index
            index = index + 1

        self._compare_types = list()
        # 比较类型的排序
        if self._contains_current_day_data:
            self._compare_types.append(self._target_current_day_column_name)
        else:
            self._compare_type_order.remove(self._target_current_day_column_name)
            self._compare_type_order.remove(self._target_current_day_column_name + self._positive_column_name)
            self._compare_type_order.remove(self._target_current_day_column_name + self._negative_column_name)
            self._compare_type_order_dict.pop(self._target_current_day_column_name)
            self._compare_type_order_dict.pop(self._target_current_day_column_name + self._positive_column_name)
            self._compare_type_order_dict.pop(self._target_current_day_column_name + self._negative_column_name)
        if self._contains_yearly_base_data:
            self._compare_types.append(self._target_yearly_base_compare_column_name)
            self._compare_types.append(self._target_yearly_base_compare_column_name + self._positive_column_name)
            self._compare_types.append(self._target_yearly_base_compare_column_name + self._negative_column_name)
        else:
            self._compare_type_order.remove(self._target_yearly_base_compare_column_name)
            self._compare_type_order.remove(self._target_yearly_base_compare_column_name + self._positive_column_name)
            self._compare_type_order.remove(self._target_yearly_base_compare_column_name + self._negative_column_name)
            self._compare_type_order_dict.pop(self._target_yearly_base_compare_column_name)
            self._compare_type_order_dict.pop(self._target_yearly_base_compare_column_name + self._positive_column_name)
            self._compare_type_order_dict.pop(self._target_yearly_base_compare_column_name + self._negative_column_name)
        if self._contains_seasonal_base_data:
            self._compare_types.append(self._target_seasonal_base_compare_column_name)
            self._compare_types.append(self._target_seasonal_base_compare_column_name + self._positive_column_name)
            self._compare_types.append(self._target_seasonal_base_compare_column_name + self._negative_column_name)
        else:
            self._compare_type_order.remove(self._target_seasonal_base_compare_column_name)
            self._compare_type_order.remove(self._target_seasonal_base_compare_column_name + self._positive_column_name)
            self._compare_type_order.remove(self._target_seasonal_base_compare_column_name + self._negative_column_name)
            self._compare_type_order_dict.pop(self._target_seasonal_base_compare_column_name)
            self._compare_type_order_dict.pop(
                self._target_seasonal_base_compare_column_name + self._positive_column_name)
            self._compare_type_order_dict.pop(
                self._target_seasonal_base_compare_column_name + self._negative_column_name)
        if self._contains_monthly_base_data:
            self._compare_types.append(self._target_monthly_base_compare_column_name)
            self._compare_types.append(self._target_monthly_base_compare_column_name + self._positive_column_name)
            self._compare_types.append(self._target_monthly_base_compare_column_name + self._negative_column_name)
        else:
            self._compare_type_order.remove(self._target_monthly_base_compare_column_name)
            self._compare_type_order.remove(self._target_monthly_base_compare_column_name + self._positive_column_name)
            self._compare_type_order.remove(self._target_monthly_base_compare_column_name + self._negative_column_name)
            self._compare_type_order_dict.pop(self._target_monthly_base_compare_column_name)
            self._compare_type_order_dict.pop(
                self._target_monthly_base_compare_column_name + self._positive_column_name)
            self._compare_type_order_dict.pop(
                self._target_monthly_base_compare_column_name + self._negative_column_name)
        if self._contains_last_week_data:
            self._compare_types.append(self._target_last_week_compare_column_name)
            self._compare_types.append(self._target_last_week_compare_column_name + self._positive_column_name)
            self._compare_types.append(self._target_last_week_compare_column_name + self._negative_column_name)
        else:
            self._compare_type_order.remove(self._target_last_week_compare_column_name)
            self._compare_type_order.remove(self._target_last_week_compare_column_name + self._positive_column_name)
            self._compare_type_order.remove(self._target_last_week_compare_column_name + self._negative_column_name)
            self._compare_type_order_dict.pop(self._target_last_week_compare_column_name)
            self._compare_type_order_dict.pop(self._target_last_week_compare_column_name + self._positive_column_name)
            self._compare_type_order_dict.pop(self._target_last_week_compare_column_name + self._negative_column_name)
        if self._contains_yesterday_data:
            self._compare_types.append(self._target_yesterday_compare_column_name)
            self._compare_types.append(self._target_yesterday_compare_column_name + self._positive_column_name)
            self._compare_types.append(self._target_yesterday_compare_column_name + self._negative_column_name)
        else:
            self._compare_type_order.remove(self._target_yesterday_compare_column_name)
            self._compare_type_order.remove(self._target_yesterday_compare_column_name + self._positive_column_name)
            self._compare_type_order.remove(self._target_yesterday_compare_column_name + self._negative_column_name)
            self._compare_type_order_dict.pop(self._target_yesterday_compare_column_name)
            self._compare_type_order_dict.pop(self._target_yesterday_compare_column_name + self._positive_column_name)
            self._compare_type_order_dict.pop(self._target_yesterday_compare_column_name + self._negative_column_name)
        if self._contains_base_data:
            self._compare_types.append(self._target_base_compare_column_name)
            self._compare_types.append(self._target_base_compare_column_name + self._positive_column_name)
            self._compare_types.append(self._target_base_compare_column_name + self._negative_column_name)
        else:
            self._compare_type_order.remove(self._target_base_compare_column_name)
            self._compare_type_order.remove(self._target_base_compare_column_name + self._positive_column_name)
            self._compare_type_order.remove(self._target_base_compare_column_name + self._negative_column_name)
            self._compare_type_order_dict.pop(self._target_base_compare_column_name)
            self._compare_type_order_dict.pop(self._target_base_compare_column_name + self._positive_column_name)
            self._compare_type_order_dict.pop(self._target_base_compare_column_name + self._negative_column_name)
        if self._contains_target_data:
            self._compare_types.append(self._target_target_compare_column_name)
            self._compare_types.append(self._target_target_compare_column_name + self._positive_column_name)
            self._compare_types.append(self._target_target_compare_column_name + self._negative_column_name)
        else:
            self._compare_type_order.remove(self._target_target_compare_column_name)
            self._compare_type_order.remove(self._target_target_compare_column_name + self._positive_column_name)
            self._compare_type_order.remove(self._target_target_compare_column_name + self._negative_column_name)
            self._compare_type_order_dict.pop(self._target_target_compare_column_name)
            self._compare_type_order_dict.pop(self._target_target_compare_column_name + self._positive_column_name)
            self._compare_type_order_dict.pop(self._target_target_compare_column_name + self._negative_column_name)
        logging.getLogger(__name__).info(f"比较类型:{self._compare_types}")

    def _calculate_value_based_on_compare_type(self, value, compare_type):
        if self._positive_column_name in compare_type:
            return value if value > 0 else 0
        elif self._negative_column_name in compare_type:
            return -value if value < 0 else 0
        return value

    def _deal_with_compare_result(
            self, *,
            result: pd.DataFrame,
            compare_result: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        处理比较结果
        根据比较结果去设置最终结果集
        :param result: 最终结果集
        :param compare_result: 比较结果
        :return:
        """
        result = super()._deal_with_compare_result(result=result, compare_result=compare_result)
        logging.getLogger(__name__).info("处理投放还款比较结果...")
        # 检查配置的比较项目中哪些是存在的
        existed_columns = self._find_existed_columns(result)

        result2 = result.copy()
        result_merge = result.merge(
            result2,
            on=self._index_column_names,
        )
        # 删除比较类型x包含投放或者还款的行
        result_merge.drop(
            index=result_merge.loc[
                (result_merge[self._target_compare_type_column_name + '_x'].str.contains(self._positive_column_name))
                | (result_merge[self._target_compare_type_column_name + '_x'].str.contains(self._negative_column_name))
                ].index,
            inplace=True,
        )
        # 只保留比较类型Y包含比较类型X的行
        result_merge = result_merge[
            result_merge.apply(
                lambda x: x[self._target_compare_type_column_name + '_x'] in x[
                    self._target_compare_type_column_name + '_y'],
                axis=1,
            )
        ]
        for column in existed_columns:
            result_merge[column + '_y'] = result_merge.apply(
                lambda x: self._calculate_value_based_on_compare_type(
                    x[column + '_x'],
                    x[self._target_compare_type_column_name + '_y']
                ),
                axis=1
            )
            result_merge.drop(
                columns=[column + "_x"], inplace=True
            )
            result_merge.rename(
                columns={
                    column + '_y': column,
                }, inplace=True
            )
        result_merge.drop(
            columns=[self._target_compare_type_column_name + '_x'], inplace=True
        )
        result_merge.rename(
            columns={
                self._target_compare_type_column_name + '_y': self._target_compare_type_column_name,
            }, inplace=True
        )
        logging.getLogger(__name__).info("处理投放还款比较结果结束")
        return result_merge

    def _after_calculated_difference(self, result: pd.DataFrame) -> pd.DataFrame:
        logging.getLogger(__name__).info("差异后分析...")
        # 没有的数据填充"-"
        result.fillna(0, inplace=True)
        # 按客户统计维度，不需要投放与还款比较类型
        compare_type_order_result = self._compare_type_order.copy()
        if self._contains_yearly_base_data:
            compare_type_order_result.remove(self._target_yearly_base_compare_column_name + self._positive_column_name)
            compare_type_order_result.remove(self._target_yearly_base_compare_column_name + self._negative_column_name)
        if self._contains_seasonal_base_data:
            compare_type_order_result.remove(
                self._target_seasonal_base_compare_column_name + self._positive_column_name)
            compare_type_order_result.remove(
                self._target_seasonal_base_compare_column_name + self._negative_column_name)
        if self._contains_monthly_base_data:
            compare_type_order_result.remove(self._target_monthly_base_compare_column_name + self._positive_column_name)
            compare_type_order_result.remove(self._target_monthly_base_compare_column_name + self._negative_column_name)
        if self._contains_last_week_data:
            compare_type_order_result.remove(self._target_last_week_compare_column_name + self._positive_column_name)
            compare_type_order_result.remove(self._target_last_week_compare_column_name + self._negative_column_name)
        if self._contains_yesterday_data:
            compare_type_order_result.remove(self._target_yesterday_compare_column_name + self._positive_column_name)
            compare_type_order_result.remove(self._target_yesterday_compare_column_name + self._negative_column_name)
        if self._contains_base_data:
            compare_type_order_result.remove(self._target_base_compare_column_name + self._positive_column_name)
            compare_type_order_result.remove(self._target_base_compare_column_name + self._negative_column_name)
        if self._contains_target_data:
            compare_type_order_result.remove(self._target_target_compare_column_name + self._positive_column_name)
            compare_type_order_result.remove(self._target_target_compare_column_name + self._negative_column_name)
        # 按机构汇总投放与还款
        if self._branch_column_name in result.columns:
            data = result.copy()
            criterion = data[self._branch_column_name].map(lambda x: x != 0)
            data = data[criterion]
            compare_type_order_branch = self._compare_type_order.copy()
            # 按机构统计维度，不需要时点与较昨日、较上周等比较类型比较类型
            if self._contains_current_day_data:
                compare_type_order_branch.remove(
                    self._target_current_day_column_name)
            if self._contains_yearly_base_data:
                compare_type_order_branch.remove(
                    self._target_yearly_base_compare_column_name)
            if self._contains_seasonal_base_data:
                compare_type_order_branch.remove(
                    self._target_seasonal_base_compare_column_name)
            if self._contains_monthly_base_data:
                compare_type_order_branch.remove(
                    self._target_monthly_base_compare_column_name)
            if self._contains_last_week_data:
                compare_type_order_branch.remove(
                    self._target_last_week_compare_column_name)
            if self._contains_yesterday_data:
                compare_type_order_branch.remove(
                    self._target_yesterday_compare_column_name)
            if self._contains_base_data:
                compare_type_order_branch.remove(self._target_base_compare_column_name)
            if self._contains_target_data:
                compare_type_order_branch.remove(self._target_target_compare_column_name)

            # 处理比较类型的排序
            data[self._target_compare_type_column_name] = pd.Categorical(
                data[self._target_compare_type_column_name],
                compare_type_order_branch
            )
            self._branch_result_data = pd.pivot_table(
                data,
                values=self._diff_column_dict.keys(),
                columns=[self._target_compare_type_column_name],
                index=self._branch_column_name,
                aggfunc=np.sum,
                fill_value=0,
            )
            # 按指定顺序排序机构名称
            self._branch_result_data.sort_index(
                axis=0,
                inplace=True,
                key=self._sort_branch_rows,
            )
            # 添加合计行
            self._branch_result_data.loc["合计"] = self._branch_result_data.apply(lambda x: x.sum())
        # 处理比较类型的排序
        result[self._target_compare_type_column_name] = pd.Categorical(
            result[self._target_compare_type_column_name],
            compare_type_order_result
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

        logging.getLogger(__name__).info("数据透视...")
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

    def _write_diff_result(self, *, diff: pd.DataFrame) -> int:
        result = super()._write_diff_result(diff=diff)
        # 添加按机构投放还款汇总的输出
        if self._branch_result_data is not None and not self._branch_result_data.empty:
            target_filename_full_path = os.path.join(self._target_directory, self._target_filename)
            # 如果文件已经存在，则采用追加的模式
            mode = 'a' if os.path.exists(target_filename_full_path) else 'w'
            # 如果Sheet已经存在则替换原有的Sheet
            replace_strategy = 'replace' if mode == 'a' else None
            with ExcelWriter(target_filename_full_path, mode=mode, if_sheet_exists=replace_strategy) as excel_writer:
                sheet_name = self._sheet_name + "-" + "按机构汇总"
                self._branch_result_data.to_excel(
                    excel_writer=excel_writer,
                    sheet_name=sheet_name,
                )
        return result
