import abc
from pyocs.pyocs_interface import UniteInterface


class Msd3663Common(UniteInterface):

    independent_tuner = ['CDT-9NT372-RF01（IEC头）,EDS-11980FNPRD（F螺纹头）',
                         'XF-3SET-HP（IEC头）,EDS-11980FNPRD（F螺纹头）',
                         'EDU-12908INPRB（IEC头）,EDS-11980FNPRD（F螺纹头）',
                         ]

    def get_board_macro(self):
        # 主板宏：CVT_DEF_BOARD_TYPE
        product_split_list = self.request_dict[self.ocs_demand.product_name].split('.')
        if 'MS3663' == product_split_list[1]:
            main_project = 'MSD3663'
        elif 'MS3663T' == product_split_list[1]:
            main_project = 'MSD3663T'
        else:
            main_project = 'MSD3663S'
        board_type = product_split_list[2]
        sub_board_split_list = self.request_dict[self.ocs_demand.port_name].split('_')
        sub_board_type = sub_board_split_list[1]
        board_macro = "ID_BD_" + main_project + "_" + board_type + "_SUB_CH_" + sub_board_type
        ret = self.get_macro_line('CVT_DEF_BOARD_TYPE',board_macro)
        return ret

    def get_chip_macro(self):
        chip_type_list = self.request_dict[self.ocs_demand.chip_name].split('(')
        chip_type = chip_type_list[0]
        if ('MSD3663LSA-Z1' in chip_type) or ('MSD3663LUHA-Z1' in chip_type):
            hashkey_type = 'CVT_HASH_KEY_MSD3663LSA_Z1_GAAC'
        elif ('MSD3663LSA-SW' in chip_type) or ('MSD3663LUHA-SW' in chip_type) or ('MSD3663LSAT-SW' in chip_type):
            hashkey_type = 'CVT_HASH_KEY_MSD3663LSA_SW_GAAC'
        else:
            raise RuntimeError('此芯片型号没有录入，请补充')
        ret = self.get_macro_line('CVT_DEF_HASH_KEY',hashkey_type)
        return ret

    def get_pwm_macro(self):
        # Pwm占空比宏：[占空比：60]
        pwm_macro = self.request_dict[self.ocs_demand.pwm_name]
        if pwm_macro == '100':
            ret = self.get_macro_line('CVT_DEF_CURRENT_REF_DUTY', '0')
        else:
            ret = self.get_macro_line('CVT_DEF_CURRENT_REF_DUTY', pwm_macro)
        return ret

    def get_ci_macro(self):
        # CI PLUS
        ret = ''
        if (not self.request_dict[self.ocs_demand.ci_type]) and (not self.request_dict[self.ocs_demand.ciplus_name]):
            ret = self.get_macro_line('CVT_EN_CI_PLUS', '0')
        elif 'CI_Plus' in self.request_dict[self.ocs_demand.ciplus_name]:
            ret = self.get_macro_line('CVT_EN_CI_PLUS', '1')
        else:
            ret = self.get_macro_line('CVT_EN_CI_PLUS', '0')
        return ret

    def get_dvd_macro(self):
        ret = ''
        dvd_macro = self.request_dict[self.ocs_demand.option_func]
        if 'DVD' in dvd_macro:
            ret = self.get_macro_line('CVT_EN_SOURCE_DVD', '1')
        return ret

    def get_tuner_macro(self):
        ret = ''
        tuner_type_str = self.request_dict[self.ocs_demand.tuner_name]
        for tuner_name in self.independent_tuner:
            if tuner_name in tuner_type_str:
                ret = self.get_macro_line('CVT_EN_R842_RT710_TUNER_MODULE_SUPPORT', '1')
                return ret
        return ret

    def get_flash_size_macro(self):
        flash_size = self.request_dict[self.ocs_demand.flash_size_name]
        if '8M' in flash_size:
            ret = self.get_macro_line('FLASH_SIZE', "FLASH_SIZE_8MB")
        elif '4M' in flash_size:
            ret = self.get_macro_line('FLASH_SIZE', "FLASH_SIZE_4MB")
        else:
            raise RuntimeError('此flash没有录入，请补充')
        return ret

    def get_code_branch(self):
        return self._code_branch

    @abc.abstractmethod
    def get_ocs_modelid(self):
        pass

    @abc.abstractmethod
    def get_ocs_require(self):
        pass

