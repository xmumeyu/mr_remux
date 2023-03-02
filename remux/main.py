########################################
# 全自动压制 电影电视剧 脚本
# 暂不支持的盘： 国粤双语
# 暂时仅对 Scan type：Interlaced使用反交错，不变帧
# 作者：meyu
########################################

import os
import re
import functools
import shutil
from plugins.remux.media import MediaAnalysis
from plugins.remux.mediapro import MediaProcessing
import plugins.remux.yusesope as yus
from plugins.remux.logger import Logger
from plugins.remux.setting import Setting


class Remux:

    def __init__(self, event_var):
        self.event_var = event_var

    # 文件夹位置
    def getpath(self, oname):
        return '%s/%s' % (self.event_var.outpath, oname)


    # 单集文件命名
    def getepname(self, oname):
        return r"%s/%s.mkv" % (self.getpath(oname), oname)


    def makeremux(self, bluraypath: str):

        codevision = 'meyuremux.1.1.0'

        # 压制文件生成位置
        filepath = self.event_var.outpath

        if not filepath:
            Logger.error("The file name does not contain the year info, Unable to initialize.")
            exit(0)

        # 媒体语言，默认选取第一条音轨语言，设置为''
        # 指定语言 'English' 多语言： 'Japanese,Chinese'（不支持TrueHD多语）
        medialanguage = ''

        # 相关文件及文件夹
        videopath = "%s/video" % filepath

        myMedia = MediaAnalysis()

        myMediaPro = MediaProcessing()

        if not os.path.exists(filepath):
            os.mkdir(filepath)

        # 默认文件放在根目录
        blurayname = os.path.basename(bluraypath)
        Logger.info("blurayname: 【%s】" % blurayname)

        fname = 'remux'

        # 获取主mpls
        mpls = myMedia.mainmpls(bluraypath)
        if not mpls:
            Logger.error("no mpls")
            exit(0)

        mpls['fullmpls'] = r"%s/BDMV/PLAYLIST/%s" % (bluraypath, mpls['mpls'])
        mpls['tracks'] = myMedia.trackinfo(mpls['fullmpls'])
        mpls['medias'] = myMedia.mediainfo(mpls['fullmpls'])

        Logger.info(mpls['tracks'])
        Logger.info(mpls['medias'])

        # 字幕轨道数不符，mpls信息错误，以主视频数据为准
        # 该项调整会造成mkv混流失败，激活再次混流（此流程合理性待测试）
        if len(mpls['medias']['subtitles']) > len(mpls['tracks']['subtitles']):
            if mpls['medias']['video'][0].__contains__('Source'):
                tmpm2ts = mpls['medias']['video'][0]['Source']
                Logger.error("mpls tracks info error, use videos 【%s】 tracks" % tmpm2ts)
                tmpchapter = mpls['tracks']['chapters']
                mpls['tracks'] = myMedia.trackinfo(r"%s/BDMV/STREAM/%s" % (bluraypath, tmpm2ts))
                mpls['tracks']['chapters'] = tmpchapter

        # 为了处理异常数据，视频数据提前定义
        thism2ts = None
        dvsource = None

        # 资源数据
        thissource = {'source': mpls['fullmpls'],
                      'video': {'trackid': mpls['tracks']['video'][0]['trackid'],
                                'trackname': codevision}}

        # 音频查询
        audiodict = {}
        audioidx = 0
        for sori in mpls['medias']['audio']:
            # 并入轨道信息
            if len(mpls['tracks']['audio']) < audioidx + 1:
                break
            sori['trackid'] = mpls['tracks']['audio'][audioidx]['trackid']
            # 跳过TrueHD自带ac3核
            if 'AC-3' in sori['Format'] and 'MLP' in sori['Format']:
                audioidx += 2
            else:
                audioidx += 1
            if not sori.__contains__('Language'):
                continue
            # 保留一个媒体语言及中文音轨
            if medialanguage == '' and not audiodict:
                medialanguage = sori['Language'] + ',Chinese'
            if sori['Language'] in medialanguage:
                if not audiodict.__contains__(sori['Language']):
                    audiodict[sori['Language']] = []
                audiodict[sori['Language']].append(sori)
        # 过滤无效音频
        if not audiodict:
            Logger.error("check mpls:%s audio tracks does not match" % mpls['mpls'])
            exit(0)

        # 音频入库
        thisaudiotracks = []
        for value in audiodict.values():
            value.sort(key=functools.cmp_to_key(myMedia.audio_cmp))
            audioinfo = value.pop(0)
            thisaudiotracks.append({'simpLang': myMedia.change2simp(audioinfo['Language']),
                                    'trackid': audioinfo['trackid']})
        thissource['audio'] = thisaudiotracks

        # 字幕处理，最多保留4中文字幕，
        chinesetracks = []
        othertracks = []
        thissubtracks = []
        subidx = 0
        for sori in mpls['medias']['subtitles']:
            # 并入轨道信息
            if len(mpls['tracks']['subtitles']) < subidx + 1:
                break
            sori['trackid'] = mpls['tracks']['subtitles'][subidx]['trackid']
            subidx += 1
            if sori['Language'] == 'Chinese':
                chinesetracks.append(sori)
                if len(chinesetracks) > 4:
                    chinesetracks.pop(0)
            # 保留一个媒体语言及英语字幕
            elif sori['Language'] in medialanguage + ',English':
                haslang = False
                for tm in othertracks:
                    if tm['Language'] == sori['Language']:
                        haslang = True
                        break
                if not haslang:
                    othertracks.append(sori)

        chineselen = len(chinesetracks)
        # 有效中文字幕数量不符
        if chineselen in (0, 1, 3):
            Logger.error("subtitles")
            exit(0)
        if chineselen == 2:
            chineselist = [['zh-Hans', 'chs'], ['zh-Hant', 'cht']]
        else:
            chineselist = [['zh-Hans', r'chs^&eng'], ['zh-Hant', r'cht^&eng'], ['zh-Hans', 'chs'],
                           ['zh-Hant', 'cht']]
        for i in range(0, chineselen):
            thissubtracks.append({'simpLang': chineselist[i][0],
                                  'trackname': chinesetracks[i]['trackid'] + ':' + chineselist[i][1],
                                  'trackid': chinesetracks[i]['trackid']})
        # 格式化
        for tmpsub in othertracks:
            thissubtracks.append(
                {'simpLang': myMedia.change2simp(tmpsub['Language']),
                 'trackname': tmpsub['trackid'] + ':' + myMedia.change2subsimp(tmpsub['Language']),
                 'trackid': tmpsub['trackid']})
        thissource['subtitles'] = thissubtracks

        # 视频处理
        videos = mpls['medias']['video']
        if mpls['medias']['video'][0].__contains__('Source'):
            mpls['m2ts'] = []
            for vds in videos:
                if vds['Source'] not in mpls['m2ts']:
                    mpls['m2ts'].append(vds['Source'])

            thism2ts = videos[0]['Source']
            # 分辨率
            resolution = re.sub(r'\D', '', videos[0]['Height'])
            # 判断DV视频
            if resolution == '2160' and len(videos) > 1 and videos[1]['Source'] == thism2ts \
                    and re.sub(r'\D', '', videos[1]['Height']) == '1080':
                dvtmpa = r"%s/BDMV/STREAM/%s" % (bluraypath, thism2ts)
                dvtmpb = r'%s/01.hevc' % videopath
                if os.path.exists(dvtmpb):
                    dvsource = {'source': dvtmpb, 'video': {'trackid': '0', 'trackname': codevision}}
                    thissource.pop('video')
                else:
                    if not os.path.exists(videopath):
                        os.mkdir(videopath)
                    # 判断是否肉酱，需要合并
                    if len(mpls['m2ts']) > 1:
                        m2tss = []
                        for m2 in mpls['m2ts']:
                            m2tss.append(r"%s/BDMV/STREAM/%s" % (bluraypath, m2))
                        # dv临时文件
                        dvtmpa = r'%s/01.m2ts' % videopath
                        # 合并M2TS
                        myMedia.tsmerge(m2tss, dvtmpa, (videos[0]['trackid'], videos[1]['trackid']))

                    yus.mux_exp(dvtmpa, dvtmpb)
                    # 转换完成
                    if os.path.exists(dvtmpb):
                        dvsource = {'source': dvtmpb, 'video': {'trackid': '0', 'trackname': codevision}}
                        thissource.pop('video')
                    else:
                        Logger.error("tsmerge Failed %s" % ','.join(mpls['m2ts']))
                        exit(0)

        # remux名
        remuxepfile = self.getepname(fname)

        Logger.info(mpls['fullmpls'])
        Logger.info(remuxepfile)
        # 封装
        mkvsource = [dvsource, thissource] if dvsource else thissource
        mkvreturn = myMediaPro.makemkv(mkvsource, remuxepfile, False)

        # 封装异常，做一次容错处理
        # 不同故障添加不同代码修复
        if (mkvreturn != True) and thism2ts:
            # 故障1： mpls异常，两个m2ts文件中，有一个m2ts文件格式错误，空片头或片尾
            rerul = re.search(r"'(.+\.m2ts)'.+(no track can|cannot) be appended to", mkvreturn)
            if rerul:
                # 使用列表中时长最长的M2TS文件,尝试修复
                # 修复规则：从mpls中获取章节，添加到m2ts中混流
                tmpm2ts = r"%s/%s" % (os.path.dirname(rerul.group(1)), thism2ts)
                Logger.info("MPLS error, use M2TS:'%s' instead." % tmpm2ts)
                thissource['source'] = tmpm2ts
                if not thissource.__contains__('chaptersfile'):
                    chapterfile = "%s/chapter.txt" % filepath
                    if myMedia.getchapter(bluraypath, chapterfile):
                        thissource['chaptersfile'] = chapterfile
                        myMediaPro.makemkv(mkvsource, remuxepfile, False)
                else:
                    myMediaPro.makemkv(mkvsource, remuxepfile, False)

        # 没有找到有效文件
        if not os.path.exists(remuxepfile):
            # 混流失败，程序退出
            Logger.error("Failed to make remux file, please check this mpls %s" % mpls['fullmpls'])
            exit(0)
        else:
            fname = myMedia.getname(remuxepfile, blurayname, 'Remux')
            Logger.info("remuxname: 【%s】" % fname)
            # 新建文件夹
            if not os.path.exists(self.getpath(fname)):
                os.mkdir(self.getpath(fname))
            # 文件移位
            shutil.move(remuxepfile, self.getepname(fname))

        Logger.info("%s the end." % filepath)
