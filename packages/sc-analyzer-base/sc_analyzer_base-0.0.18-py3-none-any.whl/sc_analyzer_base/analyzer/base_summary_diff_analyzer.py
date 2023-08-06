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
from sc_analyzer_base import MoneyUtils, PROJECT_NAME, __version__


class BaseSummaryDiffAnalyzer:
    """
    汇总差异分析基础类
    """

    def __init__(self, *, config: ConfigManager, is_first_analyzer: bool = False):
        self._config = config
        self._key_enabled = None
        self._key_split_branches_enabled = None
        # 是否是第一个分析报表，如果是第一个，先把输出文件删除
        self._is_first_analyzer = is_first_analyzer
        # 是否包含基数数据
        self._contains_base_data = False
        self._base_data = pd.DataFrame()
        # 是否包含目标数据
        self._contains_target_data = False
        self._target_data = pd.DataFrame()
        # 是否包含年初数据
        self._contains_yearly_base_data = False
        self._yearly_base_data = pd.DataFrame()
        # 年初分析结果文件路径
        self._yearly_base_file_path: str = ''
        # 是否包含季度初数据
        self._contains_seasonal_base_data = False
        self._seasonal_base_data = pd.DataFrame()
        # 季度初分析结果文件路径
        self._seasonal_base_file_path: str = ''
        # 是否包含月初数据
        self._contains_monthly_base_data = False
        self._monthly_base_data = pd.DataFrame()
        # 月初分析结果文件路径
        self._monthly_base_file_path: str = ''
        # 是否包含上周数据
        self._contains_last_week_data = False
        self._last_week_data = pd.DataFrame()
        # 上周分析结果文件路径
        self._last_week_file_path: str = ''
        # 是否包含昨日数据
        self._contains_yesterday_data = False
        self._yesterday_data = pd.DataFrame()
        # 昨日分析结果文件路径
        self._yesterday_file_path: str = ''
        # 是否包含当日数据
        self._contains_current_day_data = False
        self._current_day_data = pd.DataFrame()
        # 当日分析结果文件路径
        self._current_day_file_path: str = ''

        # 生成的目标Excel文件存放路径
        self._target_directory: str = ''
        # 目标文件名称
        self._target_filename: str = ''
        # 比较类型列名称
        self._target_compare_type_column_name: str = ''
        # 较基数分析结果列名称
        self._target_base_compare_column_name: str = ''
        # 较目标差距分析结果列名称
        self._target_target_compare_column_name: str = ''
        # 较年初分析结果列名称
        self._target_yearly_base_compare_column_name: str = ''
        # 较季初分析结果列名称
        self._target_seasonal_base_compare_column_name: str = ''
        # 较月初分析结果列名称
        self._target_monthly_base_compare_column_name: str = ''
        # 较上周分析结果列名称
        self._target_last_week_compare_column_name: str = ''
        # 较昨日分析结果列名称
        self._target_yesterday_compare_column_name: str = ''
        # 当前日期分析结果列名称
        self._target_current_day_column_name: str = ''
        # 生成的Excel中Sheet的名称
        self._target_sheet_name: str = ''
        # Sheet名称
        self._sheet_name: str = ''
        # 表头行索引
        self._header_row: int = 0
        # 索引列名称（Excel中列名必须唯一）
        self._index_column_names: list = list()
        # 待分析差异列名称列表（Excel中列名必须唯一）
        self._diff_column_dict: dict = dict()
        # 比较项目的排序规则，按配置文件配置的先后顺序进行排序
        self._diff_column_order = dict()

        self._compare_types = list()
        self._compare_type_order = list()
        self._compare_type_order_dict = dict()

        self._read_config(config=config)
        self._init_diff_column_orders()

    def _enabled(self):
        """
        是否启用分析
        :return: 是否启用分析
        """
        # 配置不存在默认不启用分析
        if self._key_enabled is None:
            return False
        enabled_config = self._config.get(self._key_enabled)
        return False if enabled_config is None else enabled_config

    def _split_branches_enabled(self):
        """
        是否启用按机构拆分
        :return: 是否启用按机构拆分
        """
        # 配置不存在默认不启用按机构拆分
        if self._key_split_branches_enabled is None:
            return False
        enabled_config = self._config.get(self._key_split_branches_enabled)
        return False if enabled_config is None else enabled_config

    def _read_config(self, *, config: ConfigManager):
        """
        读取配置，初始化相关变量
        """
        logging.getLogger(__name__).info("读取配置文件...")
        # 基数分析结果文件路径
        self._base_file_path = config.get("diff.base_file_path")
        # 目标分析结果文件路径
        self._target_file_path = config.get("diff.target_file_path")
        # 年初分析结果文件路径
        self._yearly_base_file_path = config.get("diff.yearly_base_file_path")
        # 季度初分析结果文件路径
        self._seasonal_base_file_path = config.get("diff.seasonal_base_file_path")
        # 月初分析结果文件路径
        self._monthly_base_file_path = config.get("diff.monthly_base_file_path")
        # 上周分析结果文件路径
        self._last_week_file_path = config.get("diff.last_week_file_path")
        # 昨日分析结果文件路径
        self._yesterday_file_path = config.get("diff.yesterday_file_path")
        # 当日分析结果文件路径
        self._current_day_file_path = config.get("diff.current_day_file_path")

        # 生成的目标Excel文件存放路径
        self._target_directory = config.get("diff.target_directory")
        # 目标文件名称
        self._target_filename = config.get("diff.target_filename")

        # 比较类型列名称
        self._target_compare_type_column_name = config.get("diff.target_compare_type_column_name")
        # 较基数分析结果列名称
        self._target_base_compare_column_name = config.get("diff.target_base_compare_column_name")
        # 较目标分析结果列名称
        self._target_target_compare_column_name = config.get("diff.target_target_compare_column_name")
        # 较年初分析结果列名称
        self._target_yearly_base_compare_column_name = config.get("diff.target_yearly_base_compare_column_name")
        # 较季初分析结果列名称
        self._target_seasonal_base_compare_column_name = config.get("diff.target_seasonal_base_compare_column_name")
        # 较月初分析结果列名称
        self._target_monthly_base_compare_column_name = config.get("diff.target_monthly_base_compare_column_name")
        # 较上周分析结果列名称
        self._target_last_week_compare_column_name = config.get("diff.target_last_week_compare_column_name")
        # 较昨日分析结果列名称
        self._target_yesterday_compare_column_name = config.get("diff.target_yesterday_compare_column_name")
        # 当前日期分析结果列名称
        self._target_current_day_column_name = config.get("diff.target_current_day_column_name")
        # 比较类型排序规则
        compare_type_orders = config.get("diff.compare_type_orders")
        if compare_type_orders is not None and type(compare_type_orders) is list:
            self._compare_type_order.extend(compare_type_orders)

    def _init_diff_column_orders(self):
        index = 1
        for column in self._diff_column_dict.keys():
            self._diff_column_order[column] = index
            index = index + 1

    def _find_existed_columns(self, data: pd.DataFrame) -> list:
        """
        检查配置的比较项目中哪些是存在的
        """
        # 检查配置的比较项目中哪些是存在的
        existed_columns = list()
        for column in self._diff_column_dict.keys():
            if column in data.columns.values:
                existed_columns.append(column)
        return existed_columns

    def analysis(self):
        """
        分析入口
        """
        logging.getLogger(__name__).info("开始进行汇总差异分析...")
        logging.getLogger(__name__).info("program {} version {}".format(PROJECT_NAME, __version__))
        if self._is_first_analyzer:
            target_filename_full_path = os.path.join(self._target_directory, self._target_filename)
            # 如果文件已经存在，则删除
            if os.path.exists(target_filename_full_path):
                logging.getLogger(__name__).info("删除输出文件：{} ".format(target_filename_full_path))
                os.remove(target_filename_full_path)

        # 如果未启用，则直接返回上一次的分析数据
        if not self._enabled():
            logging.getLogger(__name__).info("差异分析未启用")
            return 0

        self._contains_current_day_data, self._current_day_data = self._read_src_file(
            self._current_day_file_path,
            self._target_current_day_column_name,
        )
        if not self._contains_current_day_data:
            logging.getLogger(__name__).error("未找到当日数据，程序退出。")
            return 1
        self._contains_yesterday_data, self._yesterday_data = self._read_src_file(
            self._yesterday_file_path,
            self._target_yesterday_compare_column_name,
        )
        self._contains_last_week_data, self._last_week_data = self._read_src_file(
            self._last_week_file_path,
            self._target_last_week_compare_column_name,
        )
        self._contains_monthly_base_data, self._monthly_base_data = self._read_src_file(
            self._monthly_base_file_path,
            self._target_monthly_base_compare_column_name,
        )
        self._contains_seasonal_base_data, self._seasonal_base_data = self._read_src_file(
            self._seasonal_base_file_path,
            self._target_seasonal_base_compare_column_name,
        )
        self._contains_yearly_base_data, self._yearly_base_data = self._read_src_file(
            self._yearly_base_file_path,
            self._target_yearly_base_compare_column_name,
        )
        self._contains_base_data, self._base_data = self._read_src_file(
            self._base_file_path,
            self._target_base_compare_column_name,
        )
        self._contains_target_data, self._target_data = self._read_src_file(
            self._target_file_path,
            self._target_target_compare_column_name,
        )
        if (not self._contains_yesterday_data) \
                and (not self._contains_last_week_data) \
                and (not self._contains_monthly_base_data) \
                and (not self._contains_seasonal_base_data) \
                and (not self._contains_yearly_base_data) \
                and (not self._contains_base_data) \
                and (not self._contains_target_data):
            logging.getLogger(__name__).error("未找到可对比数据，程序退出。")
            return 2
        # 初始化比较类型
        self._init_compare_types()

        diff = self._calculate_difference(
            current_day_data=self._current_day_data,
            yesterday_data=self._yesterday_data,
            last_week_data=self._last_week_data,
            monthly_base_data=self._monthly_base_data,
            seasonal_base_data=self._seasonal_base_data,
            yearly_base_data=self._yearly_base_data,
            base_data=self._base_data,
            target_data=self._target_data,
        )
        result = self._write_diff_result(diff=diff)
        logging.getLogger(__name__).info("结束汇总差异分析，结果：{}".format(result))
        return result

    def _read_src_file(
            self,
            source_file_path: str,
            compare_type: str,
    ) -> (bool, pd.DataFrame):
        """
        读取原始数据，获取DataFrame

        :param source_file_path: 源文件路径
        :param compare_type: 比较类型
        :return: (bool, pd.DataFrame), 1、是否包含数据，2、读取的数据
        """
        name = compare_type.replace("较", "")
        if source_file_path is None or (not os.path.exists(source_file_path)):
            logging.getLogger(__name__).warning("{}源文件不存在或者未配置".format(name))
            return False, pd.DataFrame()
        logging.getLogger(__name__).info("读取{}源文件：{}".format(name, source_file_path))
        try:
            data = pd.read_excel(source_file_path, sheet_name=self._sheet_name, header=self._header_row)
            data = self._filter_origin_data(data=data)
            return True, data
        except Exception as e:
            logging.getLogger(__name__).error("读取{}文件失败：{}".format(name, e))
            return False, pd.DataFrame()

    def _filter_origin_data(self, *, data):
        """
        过滤原始数据
        :param data: 原始数据
        :return: 过滤后的数据
        """
        return data

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
            self._compare_type_order_dict.pop(self._target_current_day_column_name)
        if self._contains_yearly_base_data:
            self._compare_types.append(self._target_yearly_base_compare_column_name)
        else:
            self._compare_type_order.remove(self._target_yearly_base_compare_column_name)
            self._compare_type_order_dict.pop(self._target_yearly_base_compare_column_name)
        if self._contains_seasonal_base_data:
            self._compare_types.append(self._target_seasonal_base_compare_column_name)
        else:
            self._compare_type_order.remove(self._target_seasonal_base_compare_column_name)
            self._compare_type_order_dict.pop(self._target_seasonal_base_compare_column_name)
        if self._contains_monthly_base_data:
            self._compare_types.append(self._target_monthly_base_compare_column_name)
        else:
            self._compare_type_order.remove(self._target_monthly_base_compare_column_name)
            self._compare_type_order_dict.pop(self._target_monthly_base_compare_column_name)
        if self._contains_last_week_data:
            self._compare_types.append(self._target_last_week_compare_column_name)
        else:
            self._compare_type_order.remove(self._target_last_week_compare_column_name)
            self._compare_type_order_dict.pop(self._target_last_week_compare_column_name)
        if self._contains_yesterday_data:
            self._compare_types.append(self._target_yesterday_compare_column_name)
        else:
            self._compare_type_order.remove(self._target_yesterday_compare_column_name)
            self._compare_type_order_dict.pop(self._target_yesterday_compare_column_name)
        if self._contains_base_data:
            self._compare_types.append(self._target_base_compare_column_name)
        else:
            self._compare_type_order.remove(self._target_base_compare_column_name)
            self._compare_type_order_dict.pop(self._target_base_compare_column_name)
        if self._contains_target_data:
            self._compare_types.append(self._target_target_compare_column_name)
        else:
            self._compare_type_order.remove(self._target_target_compare_column_name)
            self._compare_type_order_dict.pop(self._target_target_compare_column_name)
        logging.getLogger(__name__).info(f"比较类型:{self._compare_types}")

    def _init_result_data_frame(
            self, *,
            current_day_data: pd.DataFrame,
            yesterday_data: pd.DataFrame,
            last_week_data: pd.DataFrame,
            monthly_base_data: pd.DataFrame,
            seasonal_base_data: pd.DataFrame,
            yearly_base_data: pd.DataFrame,
            base_data: pd.DataFrame,
            target_data: pd.DataFrame,
    ) -> pd.DataFrame:
        logging.getLogger(__name__).info("初始化结果数据...")
        # 将所有数据中的索引放在一起，求并集，作为初始结果的数据
        data_list = list()
        data_list.append(current_day_data)
        data_list.append(yesterday_data)
        data_list.append(last_week_data)
        data_list.append(monthly_base_data)
        data_list.append(seasonal_base_data)
        data_list.append(yearly_base_data)
        data_list.append(base_data)
        data_list.append(target_data)

        union_result = pd.DataFrame(columns=self._index_column_names)

        # 将所有数据中的索引放在一起，求并集，作为初始结果的数据
        for df in data_list:
            if df is None or df.empty:
                continue
            union_result = pd.merge(
                union_result[self._index_column_names].drop_duplicates(),
                df[self._index_column_names].drop_duplicates(),
                on=self._index_column_names,
                how="outer"
            )

        df_compare_types = pd.DataFrame(self._compare_types, columns=[self._target_compare_type_column_name])
        # 计算两者的笛卡尔积，以快速初始化result对象
        result = pd.merge(union_result, df_compare_types, how="cross")
        # 添加数据列
        for column in self._diff_column_dict:
            result[column] = 0

        return result

    def _calculate_difference(
            self, *,
            current_day_data: pd.DataFrame,
            yesterday_data: pd.DataFrame,
            last_week_data: pd.DataFrame,
            monthly_base_data: pd.DataFrame,
            seasonal_base_data: pd.DataFrame,
            yearly_base_data: pd.DataFrame,
            base_data: pd.DataFrame,
            target_data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        差异分析
        :rtype: pd.DataFrame
        :param current_day_data: 当日数据
        :param yesterday_data: 昨日数据
        :param last_week_data: 上周数据
        :param monthly_base_data: 月初数据
        :param seasonal_base_data: 季度初数据
        :param yearly_base_data: 年初数据
        :param base_data: 基数数据
        :param target_data: 目标数据
        :return: 差异分析结果
        """

        logging.getLogger(__name__).info("计算差异...")
        # 所有索引值
        result = self._init_result_data_frame(
            current_day_data=current_day_data,
            yesterday_data=yesterday_data,
            last_week_data=last_week_data,
            monthly_base_data=monthly_base_data,
            seasonal_base_data=seasonal_base_data,
            yearly_base_data=yearly_base_data,
            base_data=base_data,
            target_data=target_data,
        )

        result = self._calculate_all_compare_types(
            result=result,
            current_day_data=current_day_data,
            yesterday_data=yesterday_data,
            last_week_data=last_week_data,
            monthly_base_data=monthly_base_data,
            seasonal_base_data=seasonal_base_data,
            yearly_base_data=yearly_base_data,
            base_data=base_data,
            target_data=target_data,
        )
        # 当前时点数
        result = self._deal_with_current_data(result=result, current_day_data=current_day_data)

        result = self._after_calculated_difference(result)
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

    def _calculate_all_compare_types(
            self, *,
            result: pd.DataFrame,
            current_day_data: pd.DataFrame,
            yesterday_data: pd.DataFrame,
            last_week_data: pd.DataFrame,
            monthly_base_data: pd.DataFrame,
            seasonal_base_data: pd.DataFrame,
            yearly_base_data: pd.DataFrame,
            base_data: pd.DataFrame,
            target_data: pd.DataFrame,
    ):
        # 分析较年初
        result = self._calculate_diff_according_to_type(
            result=result,
            contains_data=self._contains_yearly_base_data,
            current_day_data=current_day_data,
            compare_type=self._target_yearly_base_compare_column_name,
            compare_data=yearly_base_data,
        )
        # 分析较季度初
        result = self._calculate_diff_according_to_type(
            result=result,
            contains_data=self._contains_seasonal_base_data,
            current_day_data=current_day_data,
            compare_type=self._target_seasonal_base_compare_column_name,
            compare_data=seasonal_base_data,
        )
        # 分析较月初
        result = self._calculate_diff_according_to_type(
            result=result,
            contains_data=self._contains_monthly_base_data,
            current_day_data=current_day_data,
            compare_type=self._target_monthly_base_compare_column_name,
            compare_data=monthly_base_data,
        )
        # 分析较上周
        result = self._calculate_diff_according_to_type(
            result=result,
            contains_data=self._contains_last_week_data,
            current_day_data=current_day_data,
            compare_type=self._target_last_week_compare_column_name,
            compare_data=last_week_data,
        )
        # 分析较昨日
        result = self._calculate_diff_according_to_type(
            result=result,
            contains_data=self._contains_yesterday_data,
            current_day_data=current_day_data,
            compare_type=self._target_yesterday_compare_column_name,
            compare_data=yesterday_data,
        )
        # 分析较基数
        result = self._calculate_diff_according_to_type(
            result=result,
            contains_data=self._contains_base_data,
            current_day_data=current_day_data,
            compare_type=self._target_base_compare_column_name,
            compare_data=base_data,
        )
        # 分析较目标差距
        result = self._calculate_diff_according_to_type(
            result=result,
            contains_data=self._contains_target_data,
            current_day_data=target_data,
            compare_type=self._target_target_compare_column_name,
            compare_data=current_day_data,
        )
        return result

    def _sort_compare_item_and_type(self, columns):
        # 如果是待分析差异项排序，则使用自定义的排序规则
        if self._diff_column_order.get(columns[0]) is not None:
            return columns.map(self._diff_column_order)
        else:
            # 如果是比较类型的排序，使用原有的Categorical进行排序
            return columns

    def _deal_with_current_data(
            self, *,
            result: pd.DataFrame,
            current_day_data: pd.DataFrame,
    ):
        logging.getLogger(__name__).info("处理时点数据...")
        current_day_data_copy = current_day_data.copy()
        current_day_data_copy[self._target_compare_type_column_name] = self._target_current_day_column_name
        result = self._deal_with_compare_result(result=result, compare_result=current_day_data_copy)
        return result

    def _calculate_diff_according_to_type(
            self,
            result: pd.DataFrame,
            contains_data: bool,
            current_day_data: pd.DataFrame,
            compare_type: str,
            compare_data: pd.DataFrame,
    ):
        """
        根据比较类型计算差异
        :param result: 差异分析结果
        :param contains_data: 是否包含待比较数据，如果没有，则直接返回
        :param current_day_data: 当前时点数
        :param compare_type: 比数类型：较年初、季初、月初、上周、昨日
        :param compare_data: 待比较分析
        :return:
        """
        if not contains_data:
            return result
        logging.getLogger(__name__).info(f"开始计算差异:{compare_type}")
        compare_result = current_day_data.merge(
            compare_data,
            how="outer",  # 与时点数据求并集
            on=self._index_column_names,
            suffixes=("_1", "_2"),
        )
        compare_result.fillna(0, inplace=True)
        compare_result[self._target_compare_type_column_name] = compare_type
        # 计算两次数据的差异
        # existed_columns_plus_index_column = list([self._index_column_names, self._target_compare_type_column_name])
        existed_columns_plus_index_column = list()
        existed_columns_plus_index_column.extend(self._index_column_names)
        existed_columns_plus_index_column.append(self._target_compare_type_column_name)
        for column in self._diff_column_dict.keys():
            # 当天与比较日期都有该列，可以进行比较
            if column in current_day_data.columns.values and column in compare_data.columns.values:
                compare_result[column] = compare_result[column + "_1"] - compare_result[column + "_2"]
            # 当天有该列，比较日期无此列，保持现状不变
            elif column in current_day_data.columns.values:
                pass
            # 当天无该列，比较日期有此列，比较结果取负数
            elif column in compare_data.columns.values:
                compare_result[column] = 0 - compare_result[column]
            # 当天与比较日期均无此列，比较结果置0
            else:
                compare_result[column] = 0
            existed_columns_plus_index_column.append(column)
        compare_result = compare_result[existed_columns_plus_index_column]
        result = self._deal_with_compare_result(result=result, compare_result=compare_result)
        return result

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
        logging.getLogger(__name__).info("处理比较结果...")
        # 检查配置的比较项目中哪些是存在的
        existed_columns = self._find_existed_columns(compare_result)
        on_columns = self._index_column_names.copy()
        on_columns.append(self._target_compare_type_column_name)
        result = result.merge(
            compare_result,
            how="left",
            on=on_columns
        )
        result.fillna(0, inplace=True)
        for column in existed_columns:
            amount_unit = self._diff_column_dict.get(column)
            divider = MoneyUtils.get_money_unit_divider(amount_unit)
            if divider != 1:
                result[column] = result[column + "_x"] + result[column + "_y"] / divider
            else:
                result[column] = result[column + "_x"] + result[column + "_y"]
            result.drop(columns=[column + "_x", column + "_y"], inplace=True)

        logging.getLogger(__name__).info("比较结果处理完毕")
        return result

    def _write_diff_result(self, *, diff: pd.DataFrame) -> int:
        target_filename_full_path = os.path.join(self._target_directory, self._target_filename)
        logging.getLogger(__name__).info("输出文件：{} ".format(target_filename_full_path))
        # 如果文件已经存在，则采用追加的模式
        mode = 'a' if os.path.exists(target_filename_full_path) else 'w'
        # 如果Sheet已经存在则替换原有的Sheet
        replace_strategy = 'replace' if mode == 'a' else None
        with pd.ExcelWriter(target_filename_full_path, mode=mode, if_sheet_exists=replace_strategy) as excel_writer:
            for name, data in dict({
                self._target_current_day_column_name: self._current_day_data,
                self._target_yearly_base_compare_column_name: self._yearly_base_data,
                self._target_seasonal_base_compare_column_name: self._seasonal_base_data,
                self._target_monthly_base_compare_column_name: self._monthly_base_data,
                self._target_last_week_compare_column_name: self._last_week_data,
                self._target_yesterday_compare_column_name: self._yesterday_data,
                self._target_base_compare_column_name: self._base_data,
                self._target_target_compare_column_name: self._target_data,
            }).items():
                if data.empty:
                    continue
                sheet_name = name.replace("较", "")
                sheet_name = self._sheet_name + "-" + sheet_name
                data.to_excel(
                    excel_writer=excel_writer,
                    index=False,
                    sheet_name=sheet_name,
                )

            diff.to_excel(
                excel_writer=excel_writer,
                sheet_name=self._target_sheet_name,
            )
        return 0
