from pydub import AudioSegment

'''
分析音频常用linux工具库:
sox
soxi 查看音频详情 metadata

开源pyton 库
pydub
'''


def duration(mp3_path):
    mp3 = AudioSegment.from_mp3(mp3_path)
    return mp3.duration_seconds


def cut_mp3(mp3_path, start_time, end_time, out_path):
    """
    给定的wav按照 start_time 和 end_time 切割并存放在out_path中
    :param mp3_path: 音频路径
    :param start_time: 起始点
    :param end_time:结束点
    :param out_path: 保存的文件路径 xx.wav
    :return:
    """
    song = AudioSegment.from_mp3(mp3_path)
    t1 = start_time * 1000
    t2 = end_time * 1000
    newAudio = song[t1:t2]
    newAudio.export(out_path, format="mp3")
    return True


if __name__ == '__main__':
    pass
