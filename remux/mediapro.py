# #######################
# 媒体处理类 2023.01.25 拆分
# 作者：meyu
# #######################
import subprocess
from plugins.remux.logger import Logger
from plugins.remux.setting import Setting


class MediaProcessing:

    def __init__(self):

        # mkv不同版本参数修正
        self.mkvtrackflag = ''

    # 当前仅修正 default-track
    def checkmkv(self):
        self.mkvtrackflag = '--default-track-flag'
        args = [Setting.mkvbin]
        res = subprocess.run(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.stderr:
            Logger.error(res.stderr)
        else:
            if 'default-track-flag' not in str(res.stdout):
                self.mkvtrackflag = '--default-track'
        return True

    # 混流
    def makemkv(self, source, file, reducecore=True):
        # 修正参数
        if not self.mkvtrackflag:
            self.checkmkv()

        # 打包mkv
        args = [Setting.mkvbin, "--priority", "lower", "--output", file]

        if isinstance(source, dict):
            tlist = [source]
            source = tlist

        _videos = []
        _audios = []
        _subtitles = []
        _splitchapters = ''
        _chapters = ''
        defultaudio = False
        for sid in range(0, len(source)):
            sori = source[sid]
            # 视频
            if sori.__contains__('video'):
                if sori['video'] != "all":
                    args.append("--video-tracks")
                    args.append(sori['video']['trackid'])
                    args.append("--language")
                    args.append(sori['video']['trackid'] + ":und")
                    args.append("--track-name")
                    args.append('%s:%s' % (sori['video']['trackid'], sori['video']['trackname']))
                    _videos.append(str(sid) + ':' + sori['video']['trackid'])
            else:
                args.append("--no-video")
            # 音频
            if sori.__contains__('audio'):
                if reducecore:
                    args.append("--reduce-to-core")
                    args.append("1")
                if sori['audio'] != "all":
                    args.append("--audio-tracks")
                    tracks = []
                    for audioi in sori['audio']:
                        tracks.append(audioi['trackid'])
                    args.append(','.join(tracks))
                    for audioi in sori['audio']:
                        args.append("--language")
                        args.append(audioi['trackid'] + ":" + audioi['simpLang'])
                        if defultaudio:
                            args.append(self.mkvtrackflag)
                            args.append("%s:no" % audioi['trackid'])
                        else:
                            defultaudio = True
                        _audios.append(str(sid) + ':' + audioi['trackid'])
            else:
                args.append("--no-audio")
            # 字幕
            if sori.__contains__('subtitles'):
                if sori['subtitles'] != "all":
                    args.append("--subtitle-tracks")
                    tracks = []
                    for subi in sori['subtitles']:
                        tracks.append(subi['trackid'])
                    args.append(','.join(tracks))
                    defultsub = False
                    for subi in sori['subtitles']:
                        args.append("--language")
                        args.append(subi['trackid'] + ":" + subi['simpLang'])
                        args.append("--track-name")
                        args.append(subi['trackname'])
                        if defultsub:
                            args.append(self.mkvtrackflag)
                            args.append("%s:no" % subi['trackid'])
                        else:
                            defultsub = True
                        _subtitles.append(str(sid) + ':' + subi['trackid'])
            else:
                args.append("--no-subtitles")

            # 章节文件
            if sori.__contains__('chaptersfile'):
                _chapters = sori['chaptersfile']

            # 切割分集
            if sori.__contains__('chapters'):
                _splitchapters = sori['chapters']

            if _chapters:
                args.append("--no-chapters")

            # 源
            args.append(sori['source'])

        if _chapters:
            args.append("--chapters")
            args.append(_chapters)

        if _splitchapters:
            args.append("--split")
            args.append("chapters:" + _splitchapters)

        # 所有轨道信息
        args.append("--track-order")
        args.append(','.join(_videos + _audios + _subtitles))

        Logger.info(args)
        res = subprocess.run(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.stderr:
            Logger.error(res.stderr)
        else:
            reslist = str(res.stdout).split(r"\n")
            if len(reslist) > 2:
                if 'Multiplexing' in reslist[-2]:
                    Logger.info('output:' + file + ' : ' + reslist[-2])
                else:
                    # 异常错误
                    Logger.error(reslist[-2])
                    return reslist[-2]
        return True
