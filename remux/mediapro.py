import subprocess #line:5
from plugins .remux .logger import Logger #line:6
from plugins .remux .setting import Setting #line:7
class MediaProcessing :#line:10
    def __init__ (O000O00000O00OO0O ):#line:12
        O000O00000O00OO0O .mkvtrackflag =''#line:15
    def checkmkv (O0OO0000O00O00OO0 ):#line:18
        O0OO0000O00O00OO0 .mkvtrackflag ='--default-track-flag'#line:19
        O00O0000OOOO0OO0O =[Setting .mkvbin ]#line:20
        OO00O0OOOO0O0OOOO =subprocess .run (O00O0000OOOO0OO0O ,shell =False ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE )#line:21
        if OO00O0OOOO0O0OOOO .stderr :#line:22
            Logger .error (OO00O0OOOO0O0OOOO .stderr )#line:23
        else :#line:24
            if 'default-track-flag'not in str (OO00O0OOOO0O0OOOO .stdout ):#line:25
                O0OO0000O00O00OO0 .mkvtrackflag ='--default-track'#line:26
        return True #line:27
    def makemkv (OO000O0OO00OOOO0O ,O000OOOOOOOO0000O ,OOOOO00O000O0OOOO ,reducecore =True ):#line:30
        if not OO000O0OO00OOOO0O .mkvtrackflag :#line:32
            OO000O0OO00OOOO0O .checkmkv ()#line:33
        OO00O0O0OOOOOOO0O =[Setting .mkvbin ,"--priority","lower","--output",OOOOO00O000O0OOOO ]#line:36
        if isinstance (O000OOOOOOOO0000O ,dict ):#line:38
            O00O00OOO00O0O0OO =[O000OOOOOOOO0000O ]#line:39
            O000OOOOOOOO0000O =O00O00OOO00O0O0OO #line:40
        _O0O0O0O0O0O0O000O =[]#line:42
        _O00O000O0OO0000O0 =[]#line:43
        _OOO0O00O0OOO000OO =[]#line:44
        _O0000OO00O000O00O =''#line:45
        _O0OO0O0O0000O00O0 =''#line:46
        OOO0O000000O0OOO0 =False #line:47
        for OOO0000O0OO0O0OOO in range (0 ,len (O000OOOOOOOO0000O )):#line:48
            O0000O00OOOOOO00O =O000OOOOOOOO0000O [OOO0000O0OO0O0OOO ]#line:49
            if O0000O00OOOOOO00O .__contains__ ('video'):#line:51
                if O0000O00OOOOOO00O ['video']!="all":#line:52
                    OO00O0O0OOOOOOO0O .append ("--video-tracks")#line:53
                    OO00O0O0OOOOOOO0O .append (O0000O00OOOOOO00O ['video']['trackid'])#line:54
                    OO00O0O0OOOOOOO0O .append ("--language")#line:55
                    OO00O0O0OOOOOOO0O .append (O0000O00OOOOOO00O ['video']['trackid']+":und")#line:56
                    OO00O0O0OOOOOOO0O .append ("--track-name")#line:57
                    OO00O0O0OOOOOOO0O .append ('%s:%s'%(O0000O00OOOOOO00O ['video']['trackid'],O0000O00OOOOOO00O ['video']['trackname']))#line:58
                    _O0O0O0O0O0O0O000O .append (str (OOO0000O0OO0O0OOO )+':'+O0000O00OOOOOO00O ['video']['trackid'])#line:59
            else :#line:60
                OO00O0O0OOOOOOO0O .append ("--no-video")#line:61
            if O0000O00OOOOOO00O .__contains__ ('audio'):#line:63
                if reducecore :#line:64
                    OO00O0O0OOOOOOO0O .append ("--reduce-to-core")#line:65
                    OO00O0O0OOOOOOO0O .append ("1")#line:66
                if O0000O00OOOOOO00O ['audio']!="all":#line:67
                    OO00O0O0OOOOOOO0O .append ("--audio-tracks")#line:68
                    O00OOOO0000000O00 =[]#line:69
                    for O0000O000O0O0OOO0 in O0000O00OOOOOO00O ['audio']:#line:70
                        O00OOOO0000000O00 .append (O0000O000O0O0OOO0 ['trackid'])#line:71
                    OO00O0O0OOOOOOO0O .append (','.join (O00OOOO0000000O00 ))#line:72
                    for O0000O000O0O0OOO0 in O0000O00OOOOOO00O ['audio']:#line:73
                        OO00O0O0OOOOOOO0O .append ("--language")#line:74
                        OO00O0O0OOOOOOO0O .append (O0000O000O0O0OOO0 ['trackid']+":"+O0000O000O0O0OOO0 ['simpLang'])#line:75
                        if OOO0O000000O0OOO0 :#line:76
                            OO00O0O0OOOOOOO0O .append (OO000O0OO00OOOO0O .mkvtrackflag )#line:77
                            OO00O0O0OOOOOOO0O .append ("%s:no"%O0000O000O0O0OOO0 ['trackid'])#line:78
                        else :#line:79
                            OOO0O000000O0OOO0 =True #line:80
                        _O00O000O0OO0000O0 .append (str (OOO0000O0OO0O0OOO )+':'+O0000O000O0O0OOO0 ['trackid'])#line:81
            else :#line:82
                OO00O0O0OOOOOOO0O .append ("--no-audio")#line:83
            if O0000O00OOOOOO00O .__contains__ ('subtitles'):#line:85
                if O0000O00OOOOOO00O ['subtitles']!="all":#line:86
                    OO00O0O0OOOOOOO0O .append ("--subtitle-tracks")#line:87
                    O00OOOO0000000O00 =[]#line:88
                    for O0O0O0O000000000O in O0000O00OOOOOO00O ['subtitles']:#line:89
                        O00OOOO0000000O00 .append (O0O0O0O000000000O ['trackid'])#line:90
                    OO00O0O0OOOOOOO0O .append (','.join (O00OOOO0000000O00 ))#line:91
                    OO00OOOOO00OOOOO0 =False #line:92
                    for O0O0O0O000000000O in O0000O00OOOOOO00O ['subtitles']:#line:93
                        OO00O0O0OOOOOOO0O .append ("--language")#line:94
                        OO00O0O0OOOOOOO0O .append (O0O0O0O000000000O ['trackid']+":"+O0O0O0O000000000O ['simpLang'])#line:95
                        OO00O0O0OOOOOOO0O .append ("--track-name")#line:96
                        OO00O0O0OOOOOOO0O .append (O0O0O0O000000000O ['trackname'])#line:97
                        if OO00OOOOO00OOOOO0 :#line:98
                            OO00O0O0OOOOOOO0O .append (OO000O0OO00OOOO0O .mkvtrackflag )#line:99
                            OO00O0O0OOOOOOO0O .append ("%s:no"%O0O0O0O000000000O ['trackid'])#line:100
                        else :#line:101
                            OO00OOOOO00OOOOO0 =True #line:102
                        _OOO0O00O0OOO000OO .append (str (OOO0000O0OO0O0OOO )+':'+O0O0O0O000000000O ['trackid'])#line:103
            else :#line:104
                OO00O0O0OOOOOOO0O .append ("--no-subtitles")#line:105
            if O0000O00OOOOOO00O .__contains__ ('chaptersfile'):#line:108
                _O0OO0O0O0000O00O0 =O0000O00OOOOOO00O ['chaptersfile']#line:109
            if O0000O00OOOOOO00O .__contains__ ('chapters'):#line:112
                _O0000OO00O000O00O =O0000O00OOOOOO00O ['chapters']#line:113
            if _O0OO0O0O0000O00O0 :#line:115
                OO00O0O0OOOOOOO0O .append ("--no-chapters")#line:116
            OO00O0O0OOOOOOO0O .append (O0000O00OOOOOO00O ['source'])#line:119
        if _O0OO0O0O0000O00O0 :#line:121
            OO00O0O0OOOOOOO0O .append ("--chapters")#line:122
            OO00O0O0OOOOOOO0O .append (_O0OO0O0O0000O00O0 )#line:123
        if _O0000OO00O000O00O :#line:125
            OO00O0O0OOOOOOO0O .append ("--split")#line:126
            OO00O0O0OOOOOOO0O .append ("chapters:"+_O0000OO00O000O00O )#line:127
        OO00O0O0OOOOOOO0O .append ("--track-order")#line:130
        OO00O0O0OOOOOOO0O .append (','.join (_O0O0O0O0O0O0O000O +_O00O000O0OO0000O0 +_OOO0O00O0OOO000OO ))#line:131
        Logger .info (OO00O0O0OOOOOOO0O )#line:133
        OOO000OOO0O0000O0 =subprocess .run (OO00O0O0OOOOOOO0O ,shell =False ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE )#line:134
        if OOO000OOO0O0000O0 .stderr :#line:135
            Logger .error (OOO000OOO0O0000O0 .stderr )#line:136
        else :#line:137
            OOO000O00O000OO00 =str (OOO000OOO0O0000O0 .stdout ).split (r"\n")#line:138
            if len (OOO000O00O000OO00 )>2 :#line:139
                if 'Multiplexing'in OOO000O00O000OO00 [-2 ]:#line:140
                    Logger .info ('output:'+OOOOO00O000O0OOOO +' : '+OOO000O00O000OO00 [-2 ])#line:141
                else :#line:142
                    Logger .error (OOO000O00O000OO00 [-2 ])#line:144
                    return OOO000O00O000OO00 [-2 ]#line:145
        return True #line:146
