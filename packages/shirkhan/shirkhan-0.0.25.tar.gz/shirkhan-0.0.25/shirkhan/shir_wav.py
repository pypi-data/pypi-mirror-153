import wave
from pydub import AudioSegment

'''
分析音频常用linux工具库:
sox
soxi 查看音频详情 metadata

开源pyton 库
pydub
'''


def open(wav_path):
    with wave.open(wav_path) as w:  # type:wave.Wave_read
        return w


def get_duration(wav_path):
    f = open(wav_path)
    frames = f.getnframes()
    rate = f.getframerate()
    duration = float(frames) / float(rate)
    return duration


def get_channels(wav_path):
    f = open(wav_path)
    return f.getnchannels()


def get_framerate(wav_path):
    f = open(wav_path)
    return f.getframerate()


def get_sampwidth(wav_path):
    f = open(wav_path)
    return f.getsampwidth()


def cut(wav_path, start_time, end_time, out_path):
    """
    给定的wav按照 start_time 和 end_time 切割并存放在out_path中
    :param wav_path: 音频路径
    :param start_time: 起始点
    :param end_time:结束点
    :param out_path: 保存的文件路径 xx.wav
    :return:
    """
    song = AudioSegment.from_wav(wav_path)
    t1 = start_time * 1000
    t2 = end_time * 1000
    newAudio = song[t1:t2]
    newAudio.export(out_path, format="wav")
    return True


if __name__ == '__main__':
    pass
