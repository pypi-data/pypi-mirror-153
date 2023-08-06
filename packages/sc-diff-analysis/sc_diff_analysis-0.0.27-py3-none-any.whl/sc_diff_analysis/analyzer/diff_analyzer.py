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

import sys

sys.path.append(...)

from config42 import ConfigManager

from . import BranchSummaryGroupByBranchDiffAnalyzer
from . import BranchSummaryGroupByItemTypeDiffAnalyzer
from . import CommonSummaryDiffAnalyzer


def create_instance(module_name, class_name, *args, **kwargs):
    """
    动态实例化类
    :param module_name: 模块名称
    :param class_name: 类名
    :param args: 参数
    :param kwargs: 有名参数
    :return: 实例化后的对象
    """
    module_meta = __import__(module_name, globals(), locals(), [class_name])
    class_meta = getattr(module_meta, class_name)
    obj = class_meta(*args, **kwargs)
    return obj


class DiffAnalyzer:
    """
    差异分析类
    """

    def __init__(self, config: ConfigManager):
        self._config = config
        self._customized_summary_dict: dict = dict()

        # 待分析Sheet列表
        customized_summary_dict: dict = config.get("diff.customized_summary")
        if customized_summary_dict is not None and type(customized_summary_dict) is dict:
            self._customized_summary_dict.update(customized_summary_dict)

    def analysis(self):
        is_first = True
        # 自定义汇总-差异分析
        for sheet_name, summary_dict in self._customized_summary_dict.items():
            if "module_name" in summary_dict.keys() and "class_name" in summary_dict.keys():
                diff_analyzer = create_instance(
                    module_name=summary_dict.get("module_name"),
                    class_name=summary_dict.get("class_name"),
                    config=self._config,
                    is_first_analyzer=is_first,
                    diff_sheet_name=sheet_name,
                )
            else:
                diff_analyzer = CommonSummaryDiffAnalyzer(
                    config=self._config,
                    is_first_analyzer=is_first,
                    diff_sheet_name=sheet_name,
                )
            logging.getLogger(__name__).info(f"开始分析：{sheet_name} ")
            result = diff_analyzer.analysis()
            if result != 0:
                return result
            is_first = False

        # 机构汇总差异分析
        diff_analyzer = BranchSummaryGroupByBranchDiffAnalyzer(config=self._config, is_first_analyzer=is_first)
        logging.getLogger(__name__).info(f"开始分析：BranchSummaryGroupByBranchDiffAnalyzer ")
        result = diff_analyzer.analysis()
        if result != 0:
            return result

        is_first = False
        # 按差异类型分组进行差异分析
        diff_analyzer = BranchSummaryGroupByItemTypeDiffAnalyzer(config=self._config, is_first_analyzer=is_first)
        logging.getLogger(__name__).info(f"开始分析：BranchSummaryGroupByItemTypeDiffAnalyzer ")
        result = diff_analyzer.analysis()
        if result != 0:
            return result
        return result
