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
from sc_utilities import Singleton


class BranchUtils(metaclass=Singleton):
    """
    机构相关工具类
    """
    _branch_name_mapping_loaded = False
    _branch_name_mapping = dict()
    _sales_performance_attribution_mapping_loaded = False
    _sales_performance_attribution_mapping = dict()
    # 公共户名关键字列表
    _common_account_keyword_list = list()
    # 所有会发生业务的机构列表
    _all_business_branch_list = list()
    _all_business_branch_list_loaded = False
    _config = None
    
    @classmethod
    def set_config(cls, config):
        cls._config = config

    @classmethod
    def load_common_account_keyword_list(cls):
        """
        加载公共户关键字列表
        :return:
        """
        # 公共户名关键字
        common_account_keyword = cls._config.get("branch.common_account_keyword")
        cls._common_account_keyword_list.clear()
        cls._common_account_keyword_list.extend(common_account_keyword)

    @classmethod
    def is_common_account(cls, name):
        """
        判断账户名称是否为公共户
        :param name: 账户名称
        :return: 账户名称是否为公共户
        """
        for common_account_keyword in cls._common_account_keyword_list:
            if common_account_keyword in name:
                return True
        return False

    @classmethod
    def get_branch_name_mapping(cls) -> dict:
        """
        机构对应关系表
        :return: 机构对应关系表
        """
        return cls._branch_name_mapping

    @classmethod
    def load_branch_name_mapping(cls):
        """
        加载机构对应关系表
        :return:
        """
        if cls._branch_name_mapping_loaded:
            return
        mapping = cls._config.get("branch.name_mapping")
        cls._branch_name_mapping.update(mapping)
        cls._branch_name_mapping_loaded = True

    @classmethod
    def get_sales_performance_attribution_mapping(cls) -> dict:
        """
        业绩归属机构配置
        :return: 业绩归属机构配置
        """
        return cls._sales_performance_attribution_mapping

    @classmethod
    def load_sales_performance_attribution_mapping(cls):
        """
        加载业绩归属机构配置
        :return:
        """
        if cls._sales_performance_attribution_mapping_loaded:
            return
        mapping = cls._config.get("branch.sales_performance_attribution_mapping")
        cls._sales_performance_attribution_mapping.update(mapping)
        cls._sales_performance_attribution_mapping_loaded = True

    @classmethod
    def load_all_business_branch_list(cls):
        """
        加载业绩归属机构配置
        :return:
        """
        if cls._all_business_branch_list_loaded:
            return
        cls.load_branch_name_mapping()
        cls.load_sales_performance_attribution_mapping()
        name_mapping = cls.get_branch_name_mapping()
        attribution_mapping = cls.get_sales_performance_attribution_mapping()
        cls._all_business_branch_list.clear()
        branch_list = set()
        for branch_name in set(name_mapping.values()):
            if branch_name in attribution_mapping:
                branch_name = attribution_mapping.get(branch_name)
            branch_list.add(branch_name)
        cls._all_business_branch_list.extend(branch_list)
        cls._all_business_branch_list_loaded = True

    @classmethod
    def get_all_business_branch_list(cls):
        return cls._all_business_branch_list

    @classmethod
    def replace_branch_name(cls, *, branch_name: str) -> str:
        """
        替换机构名称为通用机构名称
        :param branch_name: 原机构名称
        :return: 通用机构名称
        """
        if branch_name in cls.get_branch_name_mapping():
            return cls.get_branch_name_mapping().get(branch_name)
        return branch_name
