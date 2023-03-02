# #######################
# 媒体分析类 2023.01.19 拆分
# 作者：meyu
# #######################
import subprocess
import re
import os
import functools
from plugins.remux.logger import Logger
from plugins.remux.setting import Setting


class MediaAnalysis:

    def __int__(self):
        a = 'x'

    @staticmethod
    def trackinfo(file):
        res = subprocess.run(
            [Setting.mkvbin, '-i', file],
            shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        info = {'video': [], 'audio': [], 'subtitles': [], 'chapters': 0}
        for row in str(res.stdout).split(r"\n"):
            field = row.split()
            if field[0] == 'Track':
                info[field[3]].append({'trackid': field[2].replace(':', '')})
            elif field[0] == 'Chapters:':
                info['chapters'] = int(field[1])
        return info

    def mediainfo(self, file):
        res = subprocess.run(
            [Setting.mediainfobin, file],
            shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        info = {'general': {},
                'video': [],
                'audio': [],
                'subtitles': [],
                'chapters': 0}
        _tmpk = ''
        videoindex = -1
        audioindex = -1
        subindex = -1
        chaptersnum = 0
        for row in str(res.stdout).split(r"\n"):
            field = row.split(":", 1)
            # 节点名称,节点开始位置
            if len(field) == 1:
                # 开始记录新节点数据
                # 获取节点名称
                _name = field[0].split(" #")
                if 'General' in _name[0]:
                    _tmpk = 'general'
                elif _name[0] == "Video":
                    _tmpk = 'video'
                    videoindex += 1
                    info['video'].append({})
                elif _name[0] == "Audio":
                    _tmpk = 'audio'
                    audioindex += 1
                    info[_tmpk].append({})
                elif _name[0] == "Text":
                    _tmpk = 'subtitles'
                    subindex += 1
                    info[_tmpk].append({})
                elif _name[0] == "Menu":
                    _tmpk = 'chapters'
                else:
                    _tmpk = ''
            elif _tmpk != '':
                _fkey = field[0].strip()
                _fval = field[1].strip()
                if _fkey == 'Language' or _fkey == 'Source':
                    _fval = re.sub(r'([.\w]+).*', r'\1', _fval)
                if _fkey == 'Duration':
                    _fval = self.formattime(_fval)
                # 填充节点数据
                if _tmpk == 'video':
                    info[_tmpk][videoindex][_fkey] = _fval
                elif _tmpk == 'audio':
                    info[_tmpk][audioindex][_fkey] = _fval
                elif _tmpk == 'subtitles':
                    info[_tmpk][subindex][_fkey] = _fval
                elif _tmpk == 'chapters':
                    chaptersnum += 1
                else:
                    info[_tmpk][_fkey] = _fval
        info['chapters'] = chaptersnum
        info['video'].sort(key=functools.cmp_to_key(self.video_cmp))
        # 剔除不会被使用的重复数据
        if videoindex != -1:
            tmps = None
            if info['video'][0].__contains__('Source'):
                tmps = info['video'][0]['Source']
            audiol = []
            audioidl = []
            for sori in info['audio']:
                if sori.__contains__('Source'):
                    if sori['Source'] == tmps:
                        audiol.append(sori)
                elif sori['ID'] not in audioidl:
                    audiol.append(sori)
                    audioidl.append(sori['ID'])
            info['audio'] = audiol
            subl = []
            subidl = []
            for sori in info['subtitles']:
                if sori.__contains__('Source'):
                    if sori['Source'] == tmps:
                        subl.append(sori)
                elif sori['ID'] not in subidl:
                    subl.append(sori)
                    subidl.append(sori['ID'])
            info['subtitles'] = subl
        return info


    # 获取蓝光盘内的所有列表信息
    @staticmethod
    def mainmpls(bluray):
        res = subprocess.run(
            [Setting.blurayinfobin, '-m', bluray],
            shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        info = {}
        inmath = re.search(
                        r'Title:\s*(\d+), Playlist:\s*(\d+), Length: (\d{2}):(\d{2}):(\d{2})([.\d]*), Chapters:\s*(\d+)'
                        r', Video streams:\s*(\d+), Audio streams:\s*(\d+), Subtitles:\s*(\d+),',
                        str(res.stdout))
        if inmath:
            info = {'mpls': inmath.group(2).zfill(5) + '.mpls',
                    'duration': int(inmath.group(3)) * 3600 + int(inmath.group(4)) * 60 + int(inmath.group(5)),
                    'chapters': int(inmath.group(7)),
                    'video': int(inmath.group(8)),
                    'audio': int(inmath.group(9)),
                    'subtitles': int(inmath.group(10))}
        return info

    # 获取tsMuxeR下的轨道信息
    @staticmethod
    def tsinfo(file, trackid=None):
        res = subprocess.run(
            [Setting.tsmuxerbin, file],
            shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        info = []
        tridx = -1
        trretun = None
        for row in str(res.stdout).split(r"\n"):
            field = row.split(':')
            tkey = field[0].lower().strip().replace(' ', "_")
            tval = field[1].strip() if len(field) > 1 else ''
            if tkey == 'track_id':
                tridx += 1
                info.append({'track_id': tval})
                if trackid and tridx == int(trackid):
                    trretun = info[tridx]
            elif 'stream' in tkey:
                info[tridx][tkey] = tval
        if trackid:
            return trretun
        return info

    # 获取列表中的视频名称
    @staticmethod
    def vedioextinfo(file):
        res = subprocess.run(
            [Setting.eac3tobin, file],
            shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        vtmatch = re.findall(r'(\d+\.m2ts)', str(res.stdout))
        if vtmatch:
            return vtmatch
        else:
            vtmatch = re.search(r'\[(\d+(\+\d+)*)]\.m2ts', str(res.stdout))
            vtfiles = []
            if vtmatch:
                for vi in vtmatch.group(1).split('+'):
                    vtfiles.append(vi.zfill(5) + '.m2ts')
            return vtfiles

    # 格式化媒体时长
    @staticmethod
    def formattime(timestr):
        timem = re.match(r'((\d+) h)?\s?((\d+) min)?\s?((\d+) s)?', timestr)
        sec = 0
        if timem.group(2):
            sec = sec + int(timem.group(2)) * 3600
        if timem.group(4):
            sec = sec + int(timem.group(4)) * 60
        if timem.group(6):
            sec = sec + int(timem.group(6))
        return sec

    # 格式化码率，输出kb/s数值
    @staticmethod
    def formatrate(ratestr):
        ratem = re.match(r'([.\d]+) ([kM])b/s', ratestr)
        rate = 0
        if ratem:
            rate = float(ratem.group(1))
            if ratem.group(2) == 'M':
                rate *= 1024
        return rate

    # 音频排序
    @staticmethod
    def audio_cmp(x, y):
        # 通道数大优先
        xres = re.search(r'(\d+) channel', x['Channel(s)'])
        yres = re.search(r'(\d+) channel', y['Channel(s)'])
        xch = int(xres.group(1))
        ych = int(yres.group(1))
        if xch > ych:
            return -1
        if xch < ych:
            return 1
        # 同通道数，DTS优先
        if x['Format'] != y['Format'] and y['Format'] == 'DTS':
            return 1
        return 0

    # 视频排序 按时长，分辨率排序
    @staticmethod
    def video_cmp(x, y):
        # 时长大优先
        xch = x['Duration']
        ych = y['Duration']
        if xch > ych:
            return -1
        if xch < ych:
            return 1
        # 同时长，分辨率大的优先
        xsize = int(re.sub(r'\D', '', x['Width']))
        ysize = int(re.sub(r'\D', '', y['Width']))
        if xsize > ysize:
            return -1
        if xsize < ysize:
            return 1
        return 0

    # 视频排序2  按文件名排序
    @staticmethod
    def video_cmp2(x, y):
        if x['mpls'] < y['mpls']:
            return -1
        if x['mpls'] > y['mpls']:
            return 1
        return 0

    # 转换音频
    @staticmethod
    def changeaudio(mpls, trackid, file, arg):
        if os.path.exists(file):
            return True
        mplsmatch = re.search(r'\.(\w+)$', mpls)
        if mplsmatch:
            filetype = mplsmatch.group(1).lower()
            if filetype == 'mpls':
                # eac3to 的章节在前,且序号从1开始，对应的trackid序号加2
                args = [Setting.eac3tobin, mpls, '1)', str(int(trackid) + 2) + ":"+file]
            elif filetype == 'mkv':
                # mkv 等文件没有章节信息
                args = [Setting.eac3tobin, mpls, str(int(trackid) + 1) + ":" + file]
            else:
                # 音频文件直接转
                args = [Setting.eac3tobin, mpls, file]
            if arg:
                for ai in arg:
                    args.append(ai)
            Logger.info(args)
            res2 = subprocess.run(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res2.stderr:
                Logger.error(res2.stderr)
            else:
                ssmatch = re.search(r'eac3to processing took [^.]+\.', str(res2.stdout))
                if ssmatch:
                    Logger.info('output:' + file + ' : ' + ssmatch.group(0))
                    return True
        return False

    # 获取章节文件
    @staticmethod
    def getchapter(bluray, file):
        args = [Setting.blurayinfobin, '-m', '-c', bluray]
        Logger.info(args)
        res2 = subprocess.run(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res2.stderr:
            Logger.error(res2.stderr)
        else:
            chapstr = ''
            for row in str(res2.stdout).split(r"\n"):
                ssmatch = re.search(r'Chapter:\s*(\d+), Start: ([.:\d]+),', row)
                if ssmatch:
                    chapstr += 'CHAPTER%s=%s\nCHAPTER%sNAME=\n' % (ssmatch.group(1).zfill(2),
                                                                   ssmatch.group(2),
                                                                   ssmatch.group(1).zfill(2))
            if chapstr:
                f = open(file, 'w', encoding='utf-8')
                f.write(chapstr)
                f.close()
                return True
        return False

    @staticmethod
    def change2simp(lang):
        langs = {'Afrikaans': 'af',
                 'Arabic': 'ar',
                 'Asturian': 'ast',
                 'Azerbaijani': 'az',
                 'Bulgarian': 'bg',
                 'Belarusian': 'be',
                 'Bengali': 'bn',
                 'Breton': 'br',
                 'Bosnian': 'bs',
                 'Catalan': 'ca',
                 'Chinese': 'zh',
                 'Czech': 'cs',
                 'Welsh': 'cy',
                 'Danish': 'da',
                 'German': 'de',
                 'Greek': 'el',
                 'English': 'en',
                 'Esperanto': 'eo',
                 'Spanish': 'es',
                 'Estonian': 'et',
                 'Basque': 'eu',
                 'Persian': 'fa',
                 'Finnish': 'fi',
                 'French': 'fr',
                 'Frisian': 'fy',
                 'Irish': 'ga',
                 'Galician': 'gl',
                 'Hebrew': 'he',
                 'Hindi': 'hi',
                 'Croatian': 'hr',
                 'Hungarian': 'hu',
                 'Armenian': 'hy',
                 'Interlingua': 'ia',
                 'Indonesian': 'id',
                 'Igbo': 'ig',
                 'Ido': 'io',
                 'Icelandic': 'is',
                 'Italian': 'it',
                 'Japanese': 'ja',
                 'Georgian': 'ka',
                 'Kabyle': 'kab',
                 'Kazakh': 'kk',
                 'Khmer': 'km',
                 'Kannada': 'kn',
                 'Korean': 'ko',
                 'Kyrgyz': 'ky',
                 'Luxembourgish': 'lb',
                 'Lithuanian': 'lt',
                 'Latvian': 'lv',
                 'Macedonian': 'mk',
                 'Malayalam': 'ml',
                 'Mongolian': 'mn',
                 'Marathi': 'mr',
                 'Malay': 'ms',
                 'Burmese': 'my',
                 'Nepali': 'ne',
                 'Norwegian': 'no',
                 'Dutch': 'nl',
                 'Ossetic': 'os',
                 'Punjabi': 'pa',
                 'Polish': 'pl',
                 'Portuguese': 'pt',
                 'Romanian': 'ro',
                 'Russian': 'ru',
                 'Slovak': 'sk',
                 'Slovenian': 'sl',
                 'Albanian': 'sq',
                 'Serbian': 'sr',
                 'Swedish': 'sv',
                 'Swahili': 'sw',
                 'Tamil': 'ta',
                 'Telugu': 'te',
                 'Tajik': 'tg',
                 'Thai': 'th',
                 'Turkmen': 'tk',
                 'Turkish': 'tr',
                 'Tatar': 'tt',
                 'Udmurt': 'udm',
                 'Ukrainian': 'uk',
                 'Urdu': 'ur',
                 'Uzbek': 'uz',
                 'Vietnamese': 'vi'}

        if langs.__contains__(lang):
            return langs[lang]
        return 'und'

    @staticmethod
    def change2subsimp(lang):
        langs = {'English': 'eng', 'Japanese': 'jpn'}
        if langs.__contains__(lang):
            return langs[lang]
        return lang

    # ts导出，暂时只需求码音频
    def tsdemux(self, infile, trackid, outfile, otherarg=''):
        outroot = os.path.dirname(outfile)
        outname = os.path.basename(outfile)
        outpath = r'%s\tmp-%s' % (outroot, outname)
        metafile = r'%s\ts.meta' % outroot

        # ts的序列号从1开始
        # trackid = str(int(trackid) + 1)

        trackinfo = self.tsinfo(infile, trackid)
        if trackinfo:
            if not os.path.exists(outroot):
                os.mkdir(outroot)

            f = open(metafile, 'w', encoding='utf-8')
            f.write('%s, "%s", track=%s, lang=eng' % (trackinfo['stream_id'], infile, trackinfo['track_id']))
            f.close()

            args = [Setting.tsmuxerbin, metafile, outpath]
            Logger.info(args)
            res = subprocess.run(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if res.stderr:
                Logger.error(res.stderr)
            else:
                ssmatch = re.search(r'Demux complete.*(Demuxing time: .*)\\r', str(res.stdout))
                if ssmatch:
                    Logger.info('output:' + outpath + ' : ' + ssmatch.group(1))

            tmpfile = os.listdir(outpath)
            if len(tmpfile) == 1:
                tmpfile = r'%s\%s' % (outpath, tmpfile[0])
                return self.changeaudio(tmpfile, trackid, outfile, otherarg)
        return False

    # ts合并m2ts
    def tsmerge(self, infiles, outfile, ntraks=None, ntype=None):
        trackinfo = self.tsinfo(infiles[0])
        if trackinfo:
            outroot = os.path.dirname(outfile)
            metafile = r'%s\ts.meta' % outroot

            if not os.path.exists(outroot):
                os.mkdir(outroot)

            fstr = 'MUXOPT --no-pcr-on-video-pid --new-audio-pes --vbr  --vbv-len=500\n'
            for track in trackinfo:
                if ntraks and track['track_id'] not in ntraks:
                    continue
                if ntype and track['stream_type'] != ntype:
                    continue
                fstr += '%s, "%s", track=%s\n' % (track['stream_id'], '"+"'.join(infiles), track['track_id'])

            f = open(metafile, 'w', encoding='utf-8')
            f.write(fstr.strip('\n'))
            f.close()

            args = [Setting.tsmuxerbin, metafile, outfile]
            Logger.info(args)
            res = subprocess.run(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if res.stderr:
                Logger.error(res.stderr)
            else:
                ssmatch = re.search(r'(.*)', str(res.stdout))
                if ssmatch:
                    Logger.info('output:' + outfile + ' : ' + ssmatch.group(1))
                    return True
        return False

    # 文件取名
    def getname(self, file, oname, otype='', muti=False):
        mname = {'pre': '', 'version': '', 'resolution': '', 'source': 'BluRay', 'type': otype,
                 'bit': '', 'format': '', 'effect': '', 'audio': ''}
        namematch = re.match(r'(.*[12]\d{3})\.(.*)-', oname)
        if namematch:
            mname['pre'] = namematch.group(1)
            # 多盘必须带季标识，避免文件被覆盖
            if muti:
                tvmatch = re.search(r'\.S\d+\.', mname['pre'])
                if not tvmatch:
                    mname['pre'] = re.sub(r'(\.[12]\d{3})$', r'.S01\1', mname['pre'])
            info = self.mediainfo(file)
            if info.__contains__('video'):
                tvedio = info['video'][0]

                # Remux不做识别
                if not mname['type'] and tvedio.__contains__('Writing library'):
                    mname['type'] = tvedio['Writing library'].split(' ').pop(0).replace('pro', '')
                    # 位深
                    if tvedio.__contains__('Bit depth') and tvedio['Bit depth'] != '8 bits':
                        mname['bit'] = re.sub(r'(\d+) bits', r'\1bit', tvedio['Bit depth'])

                if mname['type'] == 'Remux':
                    mname['format'] = tvedio['Format']
                _rlt1 = '1080'
                if int(re.sub(r'\D', '', tvedio['Height'])) > 1080 or int(
                        re.sub(r'\D', '', tvedio['Width'])) > 1920:
                    _rlt1 = '2160'
                _rlt2 = 'p'
                if mname['type'] == 'Remux' \
                        and tvedio.__contains__('Scan type') and tvedio['Scan type'] != 'Progressive':
                    _rlt2 = 'i'
                if _rlt1 == '1080':
                    mname['resolution'] = '%s%s' % (_rlt1, _rlt2)
                else:
                    mname['resolution'] = '%s%s.UHD' % (_rlt1, _rlt2)
                    if tvedio.__contains__('Color primaries') and tvedio['Color primaries'] != 'BT.709':
                        mname['effect'] = 'HDR'
                        if 'Dolby Vision' in tvedio['HDR format']:
                            mname['effect'] = 'DV'

                if tvedio.__contains__('Original source medium'):
                    if tvedio['Original source medium'] != 'Blu-ray':
                        mname['source'] = re.sub(r'\W', '', tvedio['Original source medium'])

                audiol = []
                if info.__contains__('audio'):
                    taudio = {}
                    tch = 0
                    audionum = 0
                    for ai in info['audio']:
                        audionum += 1
                        if ai.__contains__('Channel(s)'):
                            xres = re.search(r'(\d+) channel', ai['Channel(s)'])
                            xch = int(xres.group(1))
                        else:
                            xch = 1
                        if (not taudio) or xch > tch:
                            taudio = ai
                            tch = xch

                    # 音频格式
                    audioname = re.sub(r'(\w+).*', r'\1', taudio['Format'])
                    audioname2 = ''
                    if taudio.__contains__('Commercial name'):
                        audioname2 = taudio['Commercial name']
                    audioext = ''
                    if audioname == 'DTS':
                        # DTS-HD
                        if audioname2 == 'DTS-HD Master Audio':
                            audioname = audioname + '-HD.MA'
                    elif audioname == 'MLP':
                        if 'TrueHD' in audioname2:
                            audioname = 'TrueHD'
                        if 'Atmos' in audioname2:
                            audioext = 'Atmos'
                    # AC-3格式改名
                    if audioname == 'AC-3':
                        audioname = 'DD'
                    elif audioname == 'PCM':
                        audioname = 'LPCM'
                    audiol.append(audioname)

                    # 通道数
                    #     "Front: C",
                    #     "Front: L R",
                    #     "Front: L C R",
                    #     "Front: L C R, Side: C",
                    #     "Front: L C R, Side: L R",
                    #     "Front: L C R, Side: L R, LFE",
                    #     "Front: L C R, Side: L R, Back: L R, LFE"
                    if tch in (1, 2, 5):
                        audioch = str(tch) + '.0'
                    else:
                        audioch = str(tch - 1) + '.1'
                    if audioname != 'DTS' or audioch != '5.1':
                        audiol.append(audioch)

                    # 音频拓展格式
                    if audioext:
                        audiol.append(audioext)

                    # 音频数量
                    if audionum > 1:
                        audiol.append('%sAudio' % str(audionum))

                mname['audio'] = '.'.join(audiol)

                # 版本标识
                versionl = []
                _nameext = namematch.group(2)
                versions = [['Director', 'cut', 'DC'], 'Extended', 'Theatrical', 'Unrated',
                            'Limited', 'Uncut', ['Criterion', 'Collection', 'CC'], 'CC', 'DC']
                for pattern in versions:
                    isin = True
                    sn = ''
                    if isinstance(pattern, list):
                        sn = pattern.pop()
                        for pi in pattern:
                            if not re.search(pi, _nameext, re.IGNORECASE):
                                isin = False
                                break
                    else:
                        if not re.search(pattern, _nameext, re.IGNORECASE):
                            isin = False
                    if isin:
                        if sn:
                            versionl.append(sn)
                        else:
                            versionl.append(pattern)
                mname['version'] = '.'.join(versionl)

        namestr = ''
        for nv in mname.values():
            if nv:
                namestr = '%s.%s' % (namestr, nv)
        return "%s-MeYu" % namestr.strip('.')


