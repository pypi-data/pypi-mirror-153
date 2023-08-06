import praatio.tgio as tgio
from praatio.tgio import IntervalTier, Textgrid, Interval
from decimal import Decimal
from typing import List


class SIntervalHandler:
    """
    textgrid中 item 里的intervals
    """

    def __init__(self, interval: Interval, index=0, item_index=0):
        """
        :param  interval:
        """
        self.item_index = item_index  # item 下表
        self.index = index
        self.interval = interval

        self.start = interval.start
        self.end = interval.end
        self.label = interval.label

    def get_time(self, decimal_type=True):
        """
        Decimal(f"{tg_text.start:.06f}")
        :param decimal_type:
        :param decimal_leng:
        :return:
        """
        if decimal_type:
            return [Decimal(f"{self.start:.06f}"), Decimal(f"{self.end:.06f}")]

        return [self.start, self.end]

    def get_diff_time(self, other_interval):
        """
        返回两个 intervals的起始和结尾点的误差
        :param SIntervalHandler other_interval:
        :return:
        """
        text_start, text_end = self.get_time()
        spkr_start, spkr_end = other_interval.get_time()

        return [abs(text_start - spkr_start), abs(text_end - spkr_end)]

    def is_time_equal(self, other_interval):
        """
        比较两个interval 的起始和结尾点是否一致
        :param SIntervalHandler other_interval:
        :return:
        """
        diff = list(set(self.get_diff_time(other_interval)))

        if len(diff) > 1:
            return False
        if Decimal(diff[0]) > 0:
            return False

        return True

    def to_tg_entry(self):
        """
        返回 text grid 需要保存数据的格式
        :return:
        """
        return self.start, self.end, self.label

    def __repr__(self):
        return f"item[{self.item_index}],intervals[{self.index}], min:{self.start}, max:{self.end},text:{self.label}"

    def __str__(self):
        return f"item[{self.item_index}],intervals[{self.index}], min:{self.start}, max:{self.end},text:{self.label}"


class IntervalErrorBean:
    def __init__(self, text_interval: SIntervalHandler, speaker_interval: SIntervalHandler, error_message: List[str]):
        self.text_interval = text_interval
        self.speaker_interval = speaker_interval
        self.error_message = error_message
        self.time_diff = [str(item) for item in self.text_interval.get_diff_time(self.speaker_interval)]

    def __repr__(self):
        return "\n".join([" ".join(self.error_message),
                          str(self.text_interval), str(self.speaker_interval),
                          "起始对，结尾对误差", " ".join(self.time_diff), "---" * 5])

    def __str__(self):
        return "\n".join([" ".join(self.error_message),
                          str(self.text_interval), str(self.speaker_interval),
                          "起始对，结尾对误差", " ".join(self.time_diff), "---" * 5])


class STierHandler:
    """
    textgrid 中的item
    """

    def __init__(self, tier: List[SIntervalHandler]):
        self.tier = tier

    def entrylist(self):
        return [item.to_tg_entry() for item in self.tier]

    def get_tier_diffs(self, other_tier):
        """
        返回所有text item和speaker item不一致的条和他们的错误信息
        :param STierHandler other_tier:
        :return:
        """
        assert len(self.tier) > 0 and len(other_tier.tier), "tier数量不等于2或者存在空tier,比较条件不成立"

        tier_diffs = []
        pre_end = 0
        for tg_text, tg_speaker in zip(self.tier, other_tier.tier):

            text_begin, text_end = tg_text.get_time()
            spkr_begin, spkr_end = tg_speaker.get_time()

            err_message = []
            # 判断时间是否对应
            if not tg_text.is_time_equal(tg_speaker):
                err_message.append("时间不对应")
            # 判断时间是否连续
            if spkr_begin != pre_end:
                err_message.append("时间不连续")

            pre_end = text_end

            if len(err_message) > 0:
                tier_diffs.append(IntervalErrorBean(tg_text, tg_speaker, err_message))
        return tier_diffs

    def align_time(self, need_aligned_tier):
        """
        按照自身的每个 entry 的起始和结束时间来对齐传递进来的tier的起始和结束时间
        :param STierHandler other_tier:
        :return:
        """
        assert len(self.tier) > 0 and len(need_aligned_tier.tier), "tier数量不等于2或者存在空tier,无法对齐时间"
        newEntrylist = []
        for selfz, target in zip(self.tier, need_aligned_tier.tier):  # type:SIntervalHandler
            newEntrylist.append((selfz.start, selfz.end, target.label))
        return newEntrylist


class STextGridHandler:
    """
    textgrid文件句柄
    """

    def __init__(self, path):
        self.path = path
        # type:Textgrid
        try:
            self.tg = tgio.openTextgrid(self.path, readRaw=True)
        except AssertionError as e:
            assert len(e.args) != 0, "两个tier的名字相同导致程序无法正确获取段列表"
        # assert tgio.openTextgrid(self.path, readRaw=True), "分析库报错，两段tier名字相同导致的问题"

    def tierNameList(self):
        """
        返回两个tier的名字列表
        :return:
        """
        return self.tg.tierNameList

    def entryList(self):
        """
        返回转换SIntervalHandler后的[item0,item1]集合
        :return:
        """
        entryLists = []
        for item_index, item in enumerate(self.tg.tierDict):
            iter = self.tg.tierDict.get(item)  # type:IntervalTier
            slist = []
            for index in range(len(iter.entryList)):
                slist.append(SIntervalHandler(iter.entryList[index], index + 1, item_index + 1))  # interval 从 1 开始
            entryLists.append(slist)

        return entryLists

    def tier(self, tier_name):
        assert tier_name in self.tg.tierDict, "tier name 不存在"

        return self.tg.tierDict[tier_name].entryList

    def tier_diffs(self):
        assert len(self.entryList()) >= 2, "只有一个tier，少于2的tier无法产出比较值"

        enlist = self.entryList()
        one, two = enlist[0], enlist[1]
        # assert len(one) == len(two), "两个声道段数不一致"

        return STierHandler(one).get_tier_diffs(STierHandler(two))

    def time_diffs(self):
        """
        返回错误误差集
        :return:
        """
        diffs = []
        res = self.tier_diffs()
        if res:
            for item in res:
                diffs.extend(item.time_diff)

        return sorted(diffs)

    def align_text_speaker_time(self):
        """
        item1 和item2的每个item起始点和结束点自动对齐,参考item1的时间对齐item2
        :return:
        """
        tg = self
        one, two = tg.entryList()[:2]
        oneTier = STierHandler(one)
        twoTier = STierHandler(two)
        newEntrylist = oneTier.align_time(twoTier)
        tg.tg.tierDict[tg.tg.tierNameList[0]].entryList = oneTier.entrylist()
        tg.tg.tierDict[tg.tg.tierNameList[1]].entryList = newEntrylist
        # out_path = os.path.join(os.path.dirname(file), "time_aligned", os.path.basename(file))
        # if os.path.exists(os.path.dirname(out_path)) is not True:
        #     os.makedirs(os.path.dirname(out_path), exist_ok=True)
        # tg.tg.save(out_path)

    def save(self, save_path):
        self.tg.save(save_path, useShortForm=False)

    def __str__(self):
        return self.path


#
# def get_error_details(allTextGrids, out_path="所有问题textgrid详情"):
#     """
#     生成所有文件的异常详情记录
#     :param allTextGrids:
#     :return:
#     """
#     if not os.path.exists(out_path):
#         os.makedirs(out_path, exist_ok=True)
#     ff = ""
#     try:
#         for file in allTextGrids:
#             error_msg = [file]
#             ff = file
#
#             tg = STextGridHandler(file)
#             diffs = tg.time_diffs()
#             if len(diffs) > 0:
#                 error_msg.extend([str(item) for item in tg.tier_diffs()])
#             if len(error_msg) == 1:  # 只有文件名时不计为有问题
#                 continue
#             write_lines(os.path.join(out_path, os.path.basename(file) + ".txt"), error_msg)
#     except AssertionError as e:
#         pass
#         print("异常", ff, e)
#
#
# def get_diff_tierlen_files(allTextGrids):
#     """
#     两段数量不相等
#     :return:
#     """
#     files = []
#     try:
#         for file in allTextGrids:
#
#             [one, two] = (STextGridHandler(file).entryList())[:2]
#             if len(one) != len(two):
#                 print(len(one), len(two))
#                 print(file, "两段数量不相等")
#                 files.append(file)
#
#     except AssertionError as e:
#         pass
#     return set(files)
#
#
# def get_diff_times_gt_1(allTextGrids, out_path=False):
#     """
#     误差大于1秒
#     :return:
#     """
#     files = []
#     try:
#         for file in allTextGrids:
#             diffs = STextGridHandler(file).tier_diffs()
#             if diffs:
#                 for item in diffs:
#                     gt_1 = list(filter(lambda x: Decimal(x) > 1, item.time_diff))
#                     if len(gt_1) > 0:
#                         print(file, "误差大于1秒")
#                         files.append(file)
#                         if out_path:
#                             os.makedirs(out_path, exist_ok=True)
#                             shutil.copy(file, out_path)
#                         break
#
#
#     except AssertionError as e:
#         pass
#     return set(files)
#
#
# def get_breaking_points(one, two):
#     break_pointes_list = []
#     for index, target_interval in enumerate(one):  # type:int,SIntervalHandler
#         if index > len(two) - 1:  # 索引不匹配的情况
#             break
#         other_interval = two[index]  # type:SIntervalHandler
#         # 起始点不相等，结束点相同情况
#         if target_interval.is_time_equal(other_interval) is False:
#             start_diff, end_diff = target_interval.get_diff_time(other_interval)
#             if (start_diff == 0) and (end_diff != 0):
#                 one_ends = [item.end for item in one]
#                 two_ends = [item.end for item in two]
#
#                 res1 = other_interval.end in one_ends  #
#                 res2 = target_interval.end in two_ends
#                 if res1:
#                     # print(f"item2 的 interval {other_interval.index} 在 item1 上变成了多段")
#                     break_pointes_list.append(f"item2 的 interval {other_interval.index} 在 item1 上变成了多段")
#                 if res2:
#                     # print(f"item1 的 interval {other_interval.index} 在 item2 上变成了多段")
#                     break_pointes_list.append(f"item1 的 interval {other_interval.index} 在 item2 上变成了多段")
#     return break_pointes_list
#
#
# def find_2text_1speaker(allTextGrids, out_path=False):
#     """
#     找item1的 一段编程了两段的情况
#     :param allTextGrids:
#     :return:
#     """
#     try:
#         for file in allTextGrids:
#             tg = STextGridHandler(file)
#             all_entry_list = tg.entryList()
#             if len(all_entry_list) < 2:
#                 print("这文件没有 >=2个item，无法做比较")
#                 continue
#             [one, two] = all_entry_list[:2]  # type:list[list[SIntervalHandler]]
#             res = get_breaking_points(one, two)
#             if len(res) > 0:
#                 print(f"文件{os.path.basename(file)} 中出现以下问题:")
#                 print("\n".join(res))
#                 if out_path:
#                     os.makedirs(out_path, exist_ok=True)
#                     shutil.copy(file, out_path)
#     except Exception as e:
#         pass
#         print("异常", e)
#
#
# def get_all_diff_times(allTextGrids, out_path):
#     try:
#         diffs = []
#
#         for file in allTextGrids:
#             tg = STextGridHandler(file)
#             res = tg.time_diffs()
#             for item in res:
#                 if Decimal(item) > 0.06:
#                     print(os.path.basename(file), item)
#                     if out_path:
#                         os.makedirs(out_path, exist_ok=True)
#                         shutil.copy(file, out_path)
#                         break
#                 diffs.extend(res)
#
#         result = sorted(list(Counter(diffs).items()), key=lambda x: x[0], reverse=True)
#         write_lines("difftime-list.txt", ["  ".join([item[0], str(item[1])]) for item in result])
#     except AssertionError as e:
#         print("AssertionError", e)
#     except Exception as e:
#         pass
#         print("异常", e)
#
#
# def align_time(allTextGrids, out_path):
#     """
#     按照item1 对齐item2的起始和结束时间
#     :param allTextGrids:
#     :return:
#     """
#     try:
#         result_output_path = out_path
#         for file in allTextGrids:
#
#             tg = STextGridHandler(file)
#             tg.align_text_speaker_time()
#
#             out_path = os.path.join(result_output_path, *(file.split("/")[-2:-1]))
#             if os.path.exists(out_path) is not True:
#                 os.makedirs(out_path, exist_ok=True)
#
#             tg.save(os.path.join(out_path, os.path.basename(file)))
#
#
#     except AssertionError as e:
#         print("AssertionError", e)
#     except Exception as e:
#         pass
#         print("异常", e)
#
#
# def makeup_path(allTextGrids):
#     for file in allTextGrids:
#         path = os.path.splitext(os.path.basename(file))[0]
#         real_path = os.path.join(os.path.dirname(file), str(int(path)))
#         os.makedirs(real_path)
#         shutil.move(file, real_path)
#         # print(path,int(path))
#
#
# if __name__ == '__main__':
#     pass
#
#     """
#     pip install praatio
#     pip install shirkhan
#     """
#     # allTextGrids = [""]
#     # allTextGrids = glob.glob("/Users/babbage/Desktop/中文客服联想返工/data_2000小时/29761_data/**/*.TextGrid")
#     # allTextGrids = glob.glob("/Users/babbage/Desktop/中文客服联想返工/data_2000小时/所有问题修正后的textgrids/**/*.TextGrid")
#     # allTextGrids = glob.glob("/Users/babbage/Desktop/中文客服联想返工/返工200小时详情/中文客服200小时数据/**/*.TextGrid")
#     # allTextGrids = glob.glob("/Users/babbage/Desktop/中文客服联想返工/返工200小时详情/200小时修复后的textgrids/**/*.TextGrid")
#
#     # print("分析的textgrid总数量", len(allTextGrids))
#
#     # 生成目录下所有文件的错误详情到给定目录下
#     # 1.
#     # get_error_details(allTextGrids, "all_2380_error_detail_final")
#     # 2.获取段数不一致的textgrid文件列表
#     # files = get_diff_tierlen_files(allTextGrids)
#     # 3. 获取 误差大于1的文件列表
#     # files = get_diff_times_gt_1(allTextGrids,"时间误差超过1秒textgrids")
#     # 4. 找出item1分割成2个的段位,如果outpath 给了数字，程序将问题textgrdi复制到这个目录下
#     # find_2text_1speaker(allTextGrids, out_path="中文客服200小时段被分割的textgrids/")
#     # 5. 拿出所有误差,写入 difftime_list.txt文件中
#     # get_all_diff_times(allTextGrids, "存在误差大于0.06的textgrids/")
#     # 6. 时间对齐
#     # align_time(allTextGrids, "/Users/babbage/Desktop/中文客服联想返工/返工200小时详情/200小时修复后的textgrids/")
#     # 7. 恢复路径
#     # files=glob.glob("/Users/babbage/Desktop/中文客服联想返工/返工200小时详情/问题和过程/修改完-存在误差大于0.06的textgrids/*.TextGrid")
#     # makeup_path(files)
if __name__ == '__main__':
    for i in STextGridHandler("/Users/babbage/Desktop/000919.TextGrid").entryList():
        print(i)
