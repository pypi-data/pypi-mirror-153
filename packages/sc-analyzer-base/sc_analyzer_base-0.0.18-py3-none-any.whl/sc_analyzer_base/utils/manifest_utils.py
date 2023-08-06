#  The MIT License (MIT)
#
#  Copyright (c) 2021. Scott Lau
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

import pandas as pd
from sc_utilities import Singleton

from .branch_utils import BranchUtils


class ManifestUtils(metaclass=Singleton):
    """
    花名册相关工具类
    """
    # 名单DataFrame
    _df: pd.DataFrame = None
    # 花名册姓名与所在部门对应关系DataFrame
    _name_branch_df: pd.DataFrame = None
    _id_column_name: str = ""
    _name_column_name: str = ""
    _branch_column_name: str = ""
    _sales_performance_attribution_column_name: str = ""
    # 离职人员调整表
    _leave_employee_mapping = dict()
    # （非息）离职人员归属机构表
    _non_interest_leave_employee_branch_mapping = dict()
    _config = None

    @classmethod
    def set_config(cls, config):
        cls._config = config

    @classmethod
    def get_manifest_branch_column_name(cls):
        return "花名册" + cls.get_branch_column_name()

    @classmethod
    def get_name_branch_data_frame(cls) -> pd.DataFrame:
        """
        花名册姓名与所在部门对应关系
        :return:
        """
        return cls._name_branch_df

    @classmethod
    def get_id_column_name(cls) -> str:
        """
        工号列名
        :return: 工号列名
        """
        return cls._id_column_name

    @classmethod
    def get_name_column_name(cls) -> str:
        """
        姓名列名
        :return: 姓名列名
        """
        return cls._name_column_name

    @classmethod
    def get_branch_column_name(cls) -> str:
        """
        所属机构列名
        :return: 所属机构列名
        """
        return cls._branch_column_name

    @classmethod
    def get_sales_performance_attribution_column_name(cls) -> str:
        """
        业绩归属机构列名
        :return: 业绩归属机构列名
        """
        return cls._sales_performance_attribution_column_name

    @classmethod
    def get_leave_employee_mapping(cls) -> dict:
        """
        机构对应关系表
        :return: 机构对应关系表
        """
        return cls._leave_employee_mapping

    @classmethod
    def load_leave_employee_mapping(cls):
        """
        加载离职人员调整表
        :return:
        """
        mapping = cls._config.get("manifest.leave_employee_mapping")
        cls._leave_employee_mapping.update(mapping)

    @classmethod
    def get_non_interest_leave_employee_branch_mapping(cls) -> dict:
        """
        （非息）离职人员归属机构表
        :return: （非息）离职人员归属机构表
        """
        return cls._non_interest_leave_employee_branch_mapping

    @classmethod
    def load_non_interest_leave_employee_branch_mapping(cls):
        """
        加载（非息）离职人员归属机构表
        :return:
        """
        mapping = cls._config.get("manifest.non_interest_leave_employee_branch_mapping")
        cls._non_interest_leave_employee_branch_mapping.update(mapping)

    @classmethod
    def load_manifest(cls):
        """
        加载花名册
        :return:
        """
        config = cls._config
        src_file_path = config.get("manifest.source_file_path")
        # 业绩归属机构列名
        cls._sales_performance_attribution_column_name = config.get("branch.sales_performance_attribution_column_name")
        sheet_name = config.get("manifest.sheet_name")
        header_row = config.get("manifest.sheet_config.header_row")
        # 工号列索引
        id_column = config.get("manifest.sheet_config.id_column")
        # 姓名列索引
        name_column = config.get("manifest.sheet_config.name_column")
        # 所属机构列索引
        branch_column = config.get("manifest.sheet_config.branch_column")
        logging.getLogger(__name__).info("加载花名册：{}".format(src_file_path))
        df = pd.read_excel(src_file_path, sheet_name=sheet_name, header=header_row)
        df = df.iloc[:, [id_column, name_column, branch_column]]
        cls._id_column_name = df.columns[0]
        cls._name_column_name = df.columns[1]
        cls._branch_column_name = df.columns[2]
        # 添加公共户相关行
        for branch in set(BranchUtils.get_branch_name_mapping().values()):
            # df = df.append({
            #     cls._id_column_name: 0,
            #     cls._name_column_name: branch,
            #     cls._branch_column_name: branch,
            # }, ignore_index=True)
            df = pd.concat(
                [df, pd.DataFrame(
                    {
                        cls._id_column_name: 0,
                        cls._name_column_name: branch,
                        cls._branch_column_name: branch,
                    },
                    index=[1])  # 必须添加此index参数，否则会报错
                 ],
                ignore_index=True,  # 忽略上一步添加的index，使用系统生成的index
            )

        mapping = BranchUtils.get_branch_name_mapping()
        # 替换机构名称
        df = df.replace({cls._branch_column_name: mapping})
        # 添加业绩归属列
        df[cls._sales_performance_attribution_column_name] = df[cls._branch_column_name]
        # 业绩归属机构配置
        mapping = BranchUtils.get_sales_performance_attribution_mapping()
        # 处理业绩归属机构
        result = df.replace({cls._sales_performance_attribution_column_name: mapping})
        # 花名册姓名与所在部门对应关系
        cls._name_branch_df = result[[cls._name_column_name, cls._branch_column_name]].copy()
        cls._name_branch_df.set_index(cls._name_column_name, inplace=True)
        cls._name_branch_df.rename(columns={
            cls._branch_column_name: ManifestUtils.get_manifest_branch_column_name(),
        }, inplace=True)
        cls._df = result

    @classmethod
    def fix_name_error(cls, data: pd.DataFrame, id_column_name: str, name_column_name: str) -> pd.DataFrame:
        """
        解决姓名与工号不匹配的问题

        :param data: 原始数据
        :param id_column_name: 工号列名称
        :param name_column_name: 姓名列名称
        :return: 解决姓名与工号不匹配的问题后的数据
        """
        for row_i, row in data.iterrows():
            id_value = row[id_column_name]
            if id_value == 0:
                continue
            name_in_manifest = cls._df.loc[cls._df[cls._id_column_name] == id_value][cls._name_column_name]
            if name_in_manifest.empty:
                continue
            name = row[name_column_name]
            if name != name_in_manifest.values[0]:
                data.at[row_i, name_column_name] = name_in_manifest.values[0]
        return data

    @classmethod
    def merge_with_manifest(cls, *,
                            manifest_data: pd.DataFrame,
                            data: pd.DataFrame,
                            id_column_name: str = None,
                            how: str = "left",
                            name_column_name: str = None) -> pd.DataFrame:
        """
        与花名册合并

        :param manifest_data: 花名册数据，左边表
        :param data: 待合并DataFrame，右边表
        :param how: 如何合并，即连接方式，默认使用left连接，即左连接，保证花名册的数据完整
        :param id_column_name: 工号列名称
        :param name_column_name: 姓名列名称
        :return: 花名册与目标DataFrame合并后的DataFrame
        """
        if id_column_name is None and name_column_name is None:
            # ID与名称列全为空，则返回原结果
            return data
        if id_column_name is None and name_column_name is not None:
            # 如果没有工号列，则按姓名列Join
            return manifest_data.merge(data, how=how, left_on=[cls._df.columns[1]], right_on=[name_column_name])
        if name_column_name is None and id_column_name is not None:
            # 如果没有姓名列，则按工号列Join
            return manifest_data.merge(data, how=how, left_on=[cls._df.columns[0]], right_on=[id_column_name])
        # ID与姓名都不为空，则按ID和姓名两列Join
        return manifest_data.merge(data, how=how, left_on=[cls._df.columns[0], cls._df.columns[1]],
                                   right_on=[id_column_name, name_column_name])

    @classmethod
    def get_manifest_df(cls) -> pd.DataFrame:
        return cls._df

    @classmethod
    def get_all_names_in_manifest(cls) -> list:
        return list(cls._df[cls._name_column_name].values)
