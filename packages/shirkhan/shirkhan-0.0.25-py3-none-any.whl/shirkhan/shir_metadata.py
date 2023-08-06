import collections


class Metadata:
    def __init__(self, metadata_file):
        self.__metadata_dict = collections.OrderedDict()
        self.__init_metadata_dict()
        self.__metadata_dict = self.get_metadata(metadata_file)
        self.metadata = self.__metadata_dict

    def __init_metadata_dict(self):
        self.__metadata_dict["LHD"] = ""
        self.__metadata_dict["DBN"] = ""
        self.__metadata_dict["SES"] = ""
        self.__metadata_dict["BLANK1"] = ""
        self.__metadata_dict["SRC"] = ""
        self.__metadata_dict["DIR"] = ""
        self.__metadata_dict["LBN"] = ""
        self.__metadata_dict["CCD"] = ""
        self.__metadata_dict["BEG"] = ""
        self.__metadata_dict["END"] = ""
        self.__metadata_dict["REP"] = ""
        self.__metadata_dict["RED"] = ""
        self.__metadata_dict["RET"] = ""
        self.__metadata_dict["BLANK2"] = ""
        self.__metadata_dict["SAM"] = ""
        self.__metadata_dict["SNB"] = ""
        self.__metadata_dict["SBF"] = ""
        self.__metadata_dict["SSB"] = ""
        self.__metadata_dict["QNT"] = ""
        self.__metadata_dict["NCH"] = ""
        self.__metadata_dict["BLANK3"] = ""
        self.__metadata_dict["SCD"] = ""
        self.__metadata_dict["SEX"] = ""
        self.__metadata_dict["AGE"] = ""
        self.__metadata_dict["ACC"] = ""
        self.__metadata_dict["ACT"] = ""
        self.__metadata_dict["BIR"] = ""
        self.__metadata_dict["BLANK4"] = ""
        self.__metadata_dict["MIP"] = ""
        self.__metadata_dict["MIT"] = ""
        self.__metadata_dict["SPP"] = ""
        self.__metadata_dict["SCC"] = ""
        self.__metadata_dict["BLANK5"] = ""
        self.__metadata_dict["LBR"] = ""
        self.__metadata_dict["BLANK6"] = ""

    def add_item(self, key, value):
        try:
            self.__metadata_dict[key] = value
        except Exception as e:
            raise ValueError(e)
        return True

    def get_item(self, key):
        if key in self.__metadata_dict:
            return self.__metadata_dict[key]
        else:
            return None

    def write_metadata(self, output):
        assert output.endswith(".metadata"), "输出文件扩展名不是.metadata"
        write_list = []
        try:
            for key, value in self.__metadata_dict.items():
                if "BLANK" in key:
                    write_list.append("")
                    continue
                write_list.append(key + " " + value)
            self.__write_lines(output, write_list)
        except Exception as e:
            raise ValueError(e)
        return True

    @staticmethod
    def get_metadata(filepath):
        lines = Metadata.__get_file_lines(filepath)
        __metadata_dict = collections.OrderedDict()
        count = 0
        try:
            for line in lines:
                if line.strip() == "":
                    count += 1
                    key, value = "BLANK" + str(count), ""
                elif " " not in line.strip():
                    key, value = line, ""
                else:
                    key, value = line.split(" ", 1)
                if key not in __metadata_dict.keys():
                    __metadata_dict[key] = value
                else:
                    __metadata_dict.clear()
                    raise TypeError(f"{filepath}中有重复的key:{key}")
        except Exception as e:
            raise ValueError(f"{e}:{filepath}模板内容有问题，无法区分key-value")

        return __metadata_dict

    @staticmethod
    def __get_file_lines(file_path):
        new_lines = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                new_lines.append(line.strip())
        return new_lines

    @staticmethod
    def __write_lines(file_path, write_list, mode="w"):
        write_str = "\n".join(write_list)
        with open(file_path, mode, encoding="utf-8") as f:
            f.write(write_str + "\n")

    def __repr__(self):
        dd = ["{%s:%s}" % (item[0], item[1] if item[1] else "''") for item in self.__metadata_dict.items()]
        return "\n".join(dd)

    def __str__(self):
        dd = ["%s %s" % (item[0], item[1] if item[1] else " ") for item in self.__metadata_dict.items()]
        return "\n".join(dd)
