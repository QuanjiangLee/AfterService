import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class analysis: #解析数据库配置文件数据   输入:文件名 路径 解析模块  运行函数:get_result
    def __init__(self, file_name, file_path, sql_module="pymysql", sql = 'all'):
        self.file_path = os.path.join(BASE_DIR, file_path, file_name)
        self.sql_module = sql_module
        self.sql = sql


    def _get_file(self):
        if not os.path.exists(self.file_path):
            return False

        fp = open(self.file_path, 'rb')
        info = fp.read().decode("utf-8")
        return info


    def get_result(self):
        info = self._get_file()

        if info == False:
            return info

        result_db = {}
        enter_position = info.find("\r\n\r\n")
        if enter_position >= 0:
            module_list = info.split('\r\n\r\n')
        else:
            module_list = info.split('\n\n')
        for index in module_list[1: ]:
            enter_position = index.find("\r\n")
            if enter_position >= 0:
                module_index = index.split('\r\n')
            else:
                module_index = index.split('\n')
            module = module_index[0].strip()
            module = module.strip("[")
            module = module.strip("]")
            sql_module = module.split(":")[0].strip()
            sql = module.split(":")[1].strip()

            if sql_module == self.sql_module and sql == self.sql and len(module_index) > 1:
                for i in module_index[1: ]:
                    if i.strip() == "":
                        continue
                    result_db[i.split("=")[0].strip()] = str(i.split("=")[1].strip()).encode("utf-8")
                return result_db
        return False

