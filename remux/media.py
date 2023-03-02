import subprocess #line:5
import re #line:6
import os #line:7
import functools #line:8
from plugins .remux .logger import Logger #line:9
from plugins .remux .setting import Setting #line:10
class MediaAnalysis :#line:13
    def __int__ (OO0O0O0O00O0O0OOO ):#line:15
        OOOO0OOOOO00000O0 ='x'#line:16
    @staticmethod #line:18
    def trackinfo (O0OO0000OOOO0O0OO ):#line:19
        OOOOO0OOOOO0O0000 =subprocess .run ([Setting .mkvbin ,'-i',O0OO0000OOOO0O0OO ],shell =False ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE )#line:22
        OOO0OO000O0O000OO ={'video':[],'audio':[],'subtitles':[],'chapters':0 }#line:23
        for OOOOO0O00OOO00O00 in str (OOOOO0OOOOO0O0000 .stdout ).split (r"\n"):#line:24
            O00O0000OO0OO00O0 =OOOOO0O00OOO00O00 .split ()#line:25
            if O00O0000OO0OO00O0 [0 ]=='Track':#line:26
                OOO0OO000O0O000OO [O00O0000OO0OO00O0 [3 ]].append ({'trackid':O00O0000OO0OO00O0 [2 ].replace (':','')})#line:27
            elif O00O0000OO0OO00O0 [0 ]=='Chapters:':#line:28
                OOO0OO000O0O000OO ['chapters']=int (O00O0000OO0OO00O0 [1 ])#line:29
        return OOO0OO000O0O000OO #line:30
    def mediainfo (OOO0000O00O0O0O0O ,O000OOO0OOO000O0O ):#line:32
        O0OO0O0O000OOO00O =subprocess .run ([Setting .mediainfobin ,O000OOO0OOO000O0O ],shell =False ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE )#line:35
        O0O00O00OOO000OO0 ={'general':{},'video':[],'audio':[],'subtitles':[],'chapters':0 }#line:40
        _OO0000O000O0O0OOO =''#line:41
        OO0OOOOOOOO00OOOO =-1 #line:42
        O00OO000O00O000O0 =-1 #line:43
        OO0O00O00OOO00O00 =-1 #line:44
        OO0OOOOO0O00O00O0 =0 #line:45
        for OO00OO0O00O0OOOO0 in str (O0OO0O0O000OOO00O .stdout ).split (r"\n"):#line:46
            OO00O0O00O00O00OO =OO00OO0O00O0OOOO0 .split (":",1 )#line:47
            if len (OO00O0O00O00O00OO )==1 :#line:49
                _OOO000O00OO000OO0 =OO00O0O00O00O00OO [0 ].split (" #")#line:52
                if 'General'in _OOO000O00OO000OO0 [0 ]:#line:53
                    _OO0000O000O0O0OOO ='general'#line:54
                elif _OOO000O00OO000OO0 [0 ]=="Video":#line:55
                    _OO0000O000O0O0OOO ='video'#line:56
                    OO0OOOOOOOO00OOOO +=1 #line:57
                    O0O00O00OOO000OO0 ['video'].append ({})#line:58
                elif _OOO000O00OO000OO0 [0 ]=="Audio":#line:59
                    _OO0000O000O0O0OOO ='audio'#line:60
                    O00OO000O00O000O0 +=1 #line:61
                    O0O00O00OOO000OO0 [_OO0000O000O0O0OOO ].append ({})#line:62
                elif _OOO000O00OO000OO0 [0 ]=="Text":#line:63
                    _OO0000O000O0O0OOO ='subtitles'#line:64
                    OO0O00O00OOO00O00 +=1 #line:65
                    O0O00O00OOO000OO0 [_OO0000O000O0O0OOO ].append ({})#line:66
                elif _OOO000O00OO000OO0 [0 ]=="Menu":#line:67
                    _OO0000O000O0O0OOO ='chapters'#line:68
                else :#line:69
                    _OO0000O000O0O0OOO =''#line:70
            elif _OO0000O000O0O0OOO !='':#line:71
                _O00O0OO00OO0O0OO0 =OO00O0O00O00O00OO [0 ].strip ()#line:72
                _OO00O0O00O0OOO0OO =OO00O0O00O00O00OO [1 ].strip ()#line:73
                if _O00O0OO00OO0O0OO0 =='Language'or _O00O0OO00OO0O0OO0 =='Source':#line:74
                    _OO00O0O00O0OOO0OO =re .sub (r'([.\w]+).*',r'\1',_OO00O0O00O0OOO0OO )#line:75
                if _O00O0OO00OO0O0OO0 =='Duration':#line:76
                    _OO00O0O00O0OOO0OO =OOO0000O00O0O0O0O .formattime (_OO00O0O00O0OOO0OO )#line:77
                if _OO0000O000O0O0OOO =='video':#line:79
                    O0O00O00OOO000OO0 [_OO0000O000O0O0OOO ][OO0OOOOOOOO00OOOO ][_O00O0OO00OO0O0OO0 ]=_OO00O0O00O0OOO0OO #line:80
                elif _OO0000O000O0O0OOO =='audio':#line:81
                    O0O00O00OOO000OO0 [_OO0000O000O0O0OOO ][O00OO000O00O000O0 ][_O00O0OO00OO0O0OO0 ]=_OO00O0O00O0OOO0OO #line:82
                elif _OO0000O000O0O0OOO =='subtitles':#line:83
                    O0O00O00OOO000OO0 [_OO0000O000O0O0OOO ][OO0O00O00OOO00O00 ][_O00O0OO00OO0O0OO0 ]=_OO00O0O00O0OOO0OO #line:84
                elif _OO0000O000O0O0OOO =='chapters':#line:85
                    OO0OOOOO0O00O00O0 +=1 #line:86
                else :#line:87
                    O0O00O00OOO000OO0 [_OO0000O000O0O0OOO ][_O00O0OO00OO0O0OO0 ]=_OO00O0O00O0OOO0OO #line:88
        O0O00O00OOO000OO0 ['chapters']=OO0OOOOO0O00O00O0 #line:89
        O0O00O00OOO000OO0 ['video'].sort (key =functools .cmp_to_key (OOO0000O00O0O0O0O .video_cmp ))#line:90
        if OO0OOOOOOOO00OOOO !=-1 :#line:92
            OO0OO00000OO0O0OO =None #line:93
            if O0O00O00OOO000OO0 ['video'][0 ].__contains__ ('Source'):#line:94
                OO0OO00000OO0O0OO =O0O00O00OOO000OO0 ['video'][0 ]['Source']#line:95
            O0OOO00O000OO0OO0 =[]#line:96
            OOO0OO00OOOO0O00O =[]#line:97
            for O0000000OOOO0OO00 in O0O00O00OOO000OO0 ['audio']:#line:98
                if O0000000OOOO0OO00 .__contains__ ('Source'):#line:99
                    if O0000000OOOO0OO00 ['Source']==OO0OO00000OO0O0OO :#line:100
                        O0OOO00O000OO0OO0 .append (O0000000OOOO0OO00 )#line:101
                elif O0000000OOOO0OO00 ['ID']not in OOO0OO00OOOO0O00O :#line:102
                    O0OOO00O000OO0OO0 .append (O0000000OOOO0OO00 )#line:103
                    OOO0OO00OOOO0O00O .append (O0000000OOOO0OO00 ['ID'])#line:104
            O0O00O00OOO000OO0 ['audio']=O0OOO00O000OO0OO0 #line:105
            OO0O000OO000O0000 =[]#line:106
            OO0O00OOOO00OOO00 =[]#line:107
            for O0000000OOOO0OO00 in O0O00O00OOO000OO0 ['subtitles']:#line:108
                if O0000000OOOO0OO00 .__contains__ ('Source'):#line:109
                    if O0000000OOOO0OO00 ['Source']==OO0OO00000OO0O0OO :#line:110
                        OO0O000OO000O0000 .append (O0000000OOOO0OO00 )#line:111
                elif O0000000OOOO0OO00 ['ID']not in OO0O00OOOO00OOO00 :#line:112
                    OO0O000OO000O0000 .append (O0000000OOOO0OO00 )#line:113
                    OO0O00OOOO00OOO00 .append (O0000000OOOO0OO00 ['ID'])#line:114
            O0O00O00OOO000OO0 ['subtitles']=OO0O000OO000O0000 #line:115
        return O0O00O00OOO000OO0 #line:116
    @staticmethod #line:120
    def mainmpls (OO0OOO0OO0O0OOO0O ):#line:121
        OOO0OO0OOOO00000O =subprocess .run ([Setting .blurayinfobin ,'-m',OO0OOO0OO0O0OOO0O ],shell =False ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE )#line:124
        O0O0OO0O00OOOOOOO ={}#line:125
        O0O0O0000O0OOOOOO =re .search (r'Title:\s*(\d+), Playlist:\s*(\d+), Length: (\d{2}):(\d{2}):(\d{2})([.\d]*), Chapters:\s*(\d+)' r', Video streams:\s*(\d+), Audio streams:\s*(\d+), Subtitles:\s*(\d+),',str (OOO0OO0OOOO00000O .stdout ))#line:129
        if O0O0O0000O0OOOOOO :#line:130
            O0O0OO0O00OOOOOOO ={'mpls':O0O0O0000O0OOOOOO .group (2 ).zfill (5 )+'.mpls','duration':int (O0O0O0000O0OOOOOO .group (3 ))*3600 +int (O0O0O0000O0OOOOOO .group (4 ))*60 +int (O0O0O0000O0OOOOOO .group (5 )),'chapters':int (O0O0O0000O0OOOOOO .group (7 )),'video':int (O0O0O0000O0OOOOOO .group (8 )),'audio':int (O0O0O0000O0OOOOOO .group (9 )),'subtitles':int (O0O0O0000O0OOOOOO .group (10 ))}#line:136
        return O0O0OO0O00OOOOOOO #line:137
    @staticmethod #line:140
    def tsinfo (O0O0OOOO0OO0OOOOO ,trackid =None ):#line:141
        OOOO0O0O00OOOO00O =subprocess .run ([Setting .tsmuxerbin ,O0O0OOOO0OO0OOOOO ],shell =False ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE )#line:144
        OOOO0O000OOO0O000 =[]#line:145
        O0OOO0O0O0OO00O0O =-1 #line:146
        OO0OO0000OO0OO000 =None #line:147
        for OOO00O00OO000OO0O in str (OOOO0O0O00OOOO00O .stdout ).split (r"\n"):#line:148
            O00OOO0OOOOOO00OO =OOO00O00OO000OO0O .split (':')#line:149
            OO0OOOOOOOO0OO00O =O00OOO0OOOOOO00OO [0 ].lower ().strip ().replace (' ',"_")#line:150
            O0O0OO00OOO00OO00 =O00OOO0OOOOOO00OO [1 ].strip ()if len (O00OOO0OOOOOO00OO )>1 else ''#line:151
            if OO0OOOOOOOO0OO00O =='track_id':#line:152
                O0OOO0O0O0OO00O0O +=1 #line:153
                OOOO0O000OOO0O000 .append ({'track_id':O0O0OO00OOO00OO00 })#line:154
                if trackid and O0OOO0O0O0OO00O0O ==int (trackid ):#line:155
                    OO0OO0000OO0OO000 =OOOO0O000OOO0O000 [O0OOO0O0O0OO00O0O ]#line:156
            elif 'stream'in OO0OOOOOOOO0OO00O :#line:157
                OOOO0O000OOO0O000 [O0OOO0O0O0OO00O0O ][OO0OOOOOOOO0OO00O ]=O0O0OO00OOO00OO00 #line:158
        if trackid :#line:159
            return OO0OO0000OO0OO000 #line:160
        return OOOO0O000OOO0O000 #line:161
    @staticmethod #line:164
    def vedioextinfo (O000O00000O00O00O ):#line:165
        O00000OOOOO0O0OOO =subprocess .run ([Setting .eac3tobin ,O000O00000O00O00O ],shell =False ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE )#line:168
        O0O0OO000OO00OOOO =re .findall (r'(\d+\.m2ts)',str (O00000OOOOO0O0OOO .stdout ))#line:169
        if O0O0OO000OO00OOOO :#line:170
            return O0O0OO000OO00OOOO #line:171
        else :#line:172
            O0O0OO000OO00OOOO =re .search (r'\[(\d+(\+\d+)*)]\.m2ts',str (O00000OOOOO0O0OOO .stdout ))#line:173
            O000000OOOOO00OOO =[]#line:174
            if O0O0OO000OO00OOOO :#line:175
                for OO000O00O000O0O00 in O0O0OO000OO00OOOO .group (1 ).split ('+'):#line:176
                    O000000OOOOO00OOO .append (OO000O00O000O0O00 .zfill (5 )+'.m2ts')#line:177
            return O000000OOOOO00OOO #line:178
    @staticmethod #line:181
    def formattime (O0O0000OO0O000000 ):#line:182
        OO0OO0OOO0O00O00O =re .match (r'((\d+) h)?\s?((\d+) min)?\s?((\d+) s)?',O0O0000OO0O000000 )#line:183
        OO0O000OOOO0O0O00 =0 #line:184
        if OO0OO0OOO0O00O00O .group (2 ):#line:185
            OO0O000OOOO0O0O00 =OO0O000OOOO0O0O00 +int (OO0OO0OOO0O00O00O .group (2 ))*3600 #line:186
        if OO0OO0OOO0O00O00O .group (4 ):#line:187
            OO0O000OOOO0O0O00 =OO0O000OOOO0O0O00 +int (OO0OO0OOO0O00O00O .group (4 ))*60 #line:188
        if OO0OO0OOO0O00O00O .group (6 ):#line:189
            OO0O000OOOO0O0O00 =OO0O000OOOO0O0O00 +int (OO0OO0OOO0O00O00O .group (6 ))#line:190
        return OO0O000OOOO0O0O00 #line:191
    @staticmethod #line:194
    def formatrate (OO0000OO000OOO000 ):#line:195
        OOO0O0O0O00O0OO00 =re .match (r'([.\d]+) ([kM])b/s',OO0000OO000OOO000 )#line:196
        O0OO0000O0OOOOO00 =0 #line:197
        if OOO0O0O0O00O0OO00 :#line:198
            O0OO0000O0OOOOO00 =float (OOO0O0O0O00O0OO00 .group (1 ))#line:199
            if OOO0O0O0O00O0OO00 .group (2 )=='M':#line:200
                O0OO0000O0OOOOO00 *=1024 #line:201
        return O0OO0000O0OOOOO00 #line:202
    @staticmethod #line:205
    def audio_cmp (O0OO000OOO0OOOO0O ,O000O00OO0OOO0OOO ):#line:206
        OOO00OO00000OO0OO =re .search (r'(\d+) channel',O0OO000OOO0OOOO0O ['Channel(s)'])#line:208
        OOOO00O000OOO0O00 =re .search (r'(\d+) channel',O000O00OO0OOO0OOO ['Channel(s)'])#line:209
        O00O0000OO00OOOOO =int (OOO00OO00000OO0OO .group (1 ))#line:210
        OO00O0O0O0O0OOO00 =int (OOOO00O000OOO0O00 .group (1 ))#line:211
        if O00O0000OO00OOOOO >OO00O0O0O0O0OOO00 :#line:212
            return -1 #line:213
        if O00O0000OO00OOOOO <OO00O0O0O0O0OOO00 :#line:214
            return 1 #line:215
        if O0OO000OOO0OOOO0O ['Format']!=O000O00OO0OOO0OOO ['Format']and O000O00OO0OOO0OOO ['Format']=='DTS':#line:217
            return 1 #line:218
        return 0 #line:219
    @staticmethod #line:222
    def video_cmp (O0O0OOO0OOOO00OOO ,O0OO0OO0OO0000O0O ):#line:223
        O00OO00OOO0O0OOO0 =O0O0OOO0OOOO00OOO ['Duration']#line:225
        O0O0O00OOOOOO0000 =O0OO0OO0OO0000O0O ['Duration']#line:226
        if O00OO00OOO0O0OOO0 >O0O0O00OOOOOO0000 :#line:227
            return -1 #line:228
        if O00OO00OOO0O0OOO0 <O0O0O00OOOOOO0000 :#line:229
            return 1 #line:230
        OO0OO0OOO0O00O0OO =int (re .sub (r'\D','',O0O0OOO0OOOO00OOO ['Width']))#line:232
        OOO0O00O0O00000O0 =int (re .sub (r'\D','',O0OO0OO0OO0000O0O ['Width']))#line:233
        if OO0OO0OOO0O00O0OO >OOO0O00O0O00000O0 :#line:234
            return -1 #line:235
        if OO0OO0OOO0O00O0OO <OOO0O00O0O00000O0 :#line:236
            return 1 #line:237
        return 0 #line:238
    @staticmethod #line:241
    def video_cmp2 (OO0O0OO0OOO0OO00O ,OO000000OOO0O00O0 ):#line:242
        if OO0O0OO0OOO0OO00O ['mpls']<OO000000OOO0O00O0 ['mpls']:#line:243
            return -1 #line:244
        if OO0O0OO0OOO0OO00O ['mpls']>OO000000OOO0O00O0 ['mpls']:#line:245
            return 1 #line:246
        return 0 #line:247
    @staticmethod #line:250
    def changeaudio (O0O000O0OOOOOOO0O ,OO00O0OOO0OO0O0OO ,O0O00OOOO00000O0O ,OO000O000OO0O0OO0 ):#line:251
        if os .path .exists (O0O00OOOO00000O0O ):#line:252
            return True #line:253
        OOO0OO0O00O0O00O0 =re .search (r'\.(\w+)$',O0O000O0OOOOOOO0O )#line:254
        if OOO0OO0O00O0O00O0 :#line:255
            O00OOO0OOO00OOOOO =OOO0OO0O00O0O00O0 .group (1 ).lower ()#line:256
            if O00OOO0OOO00OOOOO =='mpls':#line:257
                O0000O0OO0O00O0OO =[Setting .eac3tobin ,O0O000O0OOOOOOO0O ,'1)',str (int (OO00O0OOO0OO0O0OO )+2 )+":"+O0O00OOOO00000O0O ]#line:259
            elif O00OOO0OOO00OOOOO =='mkv':#line:260
                O0000O0OO0O00O0OO =[Setting .eac3tobin ,O0O000O0OOOOOOO0O ,str (int (OO00O0OOO0OO0O0OO )+1 )+":"+O0O00OOOO00000O0O ]#line:262
            else :#line:263
                O0000O0OO0O00O0OO =[Setting .eac3tobin ,O0O000O0OOOOOOO0O ,O0O00OOOO00000O0O ]#line:265
            if OO000O000OO0O0OO0 :#line:266
                for OOOOO00O00O000000 in OO000O000OO0O0OO0 :#line:267
                    O0000O0OO0O00O0OO .append (OOOOO00O00O000000 )#line:268
            Logger .info (O0000O0OO0O00O0OO )#line:269
            O00OOO00OOOOO0OO0 =subprocess .run (O0000O0OO0O00O0OO ,shell =False ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE )#line:270
            if O00OOO00OOOOO0OO0 .stderr :#line:271
                Logger .error (O00OOO00OOOOO0OO0 .stderr )#line:272
            else :#line:273
                OOOOO00OOOO00O000 =re .search (r'eac3to processing took [^.]+\.',str (O00OOO00OOOOO0OO0 .stdout ))#line:274
                if OOOOO00OOOO00O000 :#line:275
                    Logger .info ('output:'+O0O00OOOO00000O0O +' : '+OOOOO00OOOO00O000 .group (0 ))#line:276
                    return True #line:277
        return False #line:278
    @staticmethod #line:281
    def getchapter (O000O0OOOOOOOO0OO ,OOOOO00O0OOO00O00 ):#line:282
        O0OO00O00000OOOOO =[Setting .blurayinfobin ,'-m','-c',O000O0OOOOOOOO0OO ]#line:283
        Logger .info (O0OO00O00000OOOOO )#line:284
        OOO00OO0O00OO000O =subprocess .run (O0OO00O00000OOOOO ,shell =False ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE )#line:285
        if OOO00OO0O00OO000O .stderr :#line:286
            Logger .error (OOO00OO0O00OO000O .stderr )#line:287
        else :#line:288
            O0000O00O00OOOOO0 =''#line:289
            for O000O00OOO0000OOO in str (OOO00OO0O00OO000O .stdout ).split (r"\n"):#line:290
                OOO0O00OO000O00OO =re .search (r'Chapter:\s*(\d+), Start: ([.:\d]+),',O000O00OOO0000OOO )#line:291
                if OOO0O00OO000O00OO :#line:292
                    O0000O00O00OOOOO0 +='CHAPTER%s=%s\nCHAPTER%sNAME=\n'%(OOO0O00OO000O00OO .group (1 ).zfill (2 ),OOO0O00OO000O00OO .group (2 ),OOO0O00OO000O00OO .group (1 ).zfill (2 ))#line:295
            if O0000O00O00OOOOO0 :#line:296
                O0OOOO00OOO0O0000 =open (OOOOO00O0OOO00O00 ,'w',encoding ='utf-8')#line:297
                O0OOOO00OOO0O0000 .write (O0000O00O00OOOOO0 )#line:298
                O0OOOO00OOO0O0000 .close ()#line:299
                return True #line:300
        return False #line:301
    @staticmethod #line:303
    def change2simp (O0OOOOOO00O0000OO ):#line:304
        O00O0O0OO0O0O0OOO ={'Afrikaans':'af','Arabic':'ar','Asturian':'ast','Azerbaijani':'az','Bulgarian':'bg','Belarusian':'be','Bengali':'bn','Breton':'br','Bosnian':'bs','Catalan':'ca','Chinese':'zh','Czech':'cs','Welsh':'cy','Danish':'da','German':'de','Greek':'el','English':'en','Esperanto':'eo','Spanish':'es','Estonian':'et','Basque':'eu','Persian':'fa','Finnish':'fi','French':'fr','Frisian':'fy','Irish':'ga','Galician':'gl','Hebrew':'he','Hindi':'hi','Croatian':'hr','Hungarian':'hu','Armenian':'hy','Interlingua':'ia','Indonesian':'id','Igbo':'ig','Ido':'io','Icelandic':'is','Italian':'it','Japanese':'ja','Georgian':'ka','Kabyle':'kab','Kazakh':'kk','Khmer':'km','Kannada':'kn','Korean':'ko','Kyrgyz':'ky','Luxembourgish':'lb','Lithuanian':'lt','Latvian':'lv','Macedonian':'mk','Malayalam':'ml','Mongolian':'mn','Marathi':'mr','Malay':'ms','Burmese':'my','Nepali':'ne','Norwegian':'no','Dutch':'nl','Ossetic':'os','Punjabi':'pa','Polish':'pl','Portuguese':'pt','Romanian':'ro','Russian':'ru','Slovak':'sk','Slovenian':'sl','Albanian':'sq','Serbian':'sr','Swedish':'sv','Swahili':'sw','Tamil':'ta','Telugu':'te','Tajik':'tg','Thai':'th','Turkmen':'tk','Turkish':'tr','Tatar':'tt','Udmurt':'udm','Ukrainian':'uk','Urdu':'ur','Uzbek':'uz','Vietnamese':'vi'}#line:386
        if O00O0O0OO0O0O0OOO .__contains__ (O0OOOOOO00O0000OO ):#line:388
            return O00O0O0OO0O0O0OOO [O0OOOOOO00O0000OO ]#line:389
        return 'und'#line:390
    @staticmethod #line:392
    def change2subsimp (OO000000OOOOO0000 ):#line:393
        O00OO0OO0OOOOOOOO ={'English':'eng','Japanese':'jpn'}#line:394
        if O00OO0OO0OOOOOOOO .__contains__ (OO000000OOOOO0000 ):#line:395
            return O00OO0OO0OOOOOOOO [OO000000OOOOO0000 ]#line:396
        return OO000000OOOOO0000 #line:397
    def tsdemux (O000O0O0OO0OO000O ,OO0O0OOOO0OOO0000 ,O00OO0O0OO0O000O0 ,O000OOO0OO0O0OOOO ,otherarg =''):#line:400
        O0O0OOOOO0O0O0O00 =os .path .dirname (O000OOO0OO0O0OOOO )#line:401
        O00OOOOOOOOO00OOO =os .path .basename (O000OOO0OO0O0OOOO )#line:402
        OOOO0000O000000O0 =r'%s\tmp-%s'%(O0O0OOOOO0O0O0O00 ,O00OOOOOOOOO00OOO )#line:403
        OOO0000OOOO0OOO0O =r'%s\ts.meta'%O0O0OOOOO0O0O0O00 #line:404
        O0O0OOO00OOO00OO0 =O000O0O0OO0OO000O .tsinfo (OO0O0OOOO0OOO0000 ,O00OO0O0OO0O000O0 )#line:409
        if O0O0OOO00OOO00OO0 :#line:410
            if not os .path .exists (O0O0OOOOO0O0O0O00 ):#line:411
                os .mkdir (O0O0OOOOO0O0O0O00 )#line:412
            O00O0OO0000O0O0O0 =open (OOO0000OOOO0OOO0O ,'w',encoding ='utf-8')#line:414
            O00O0OO0000O0O0O0 .write ('%s, "%s", track=%s, lang=eng'%(O0O0OOO00OOO00OO0 ['stream_id'],OO0O0OOOO0OOO0000 ,O0O0OOO00OOO00OO0 ['track_id']))#line:415
            O00O0OO0000O0O0O0 .close ()#line:416
            O0O000OOOO0OO00O0 =[Setting .tsmuxerbin ,OOO0000OOOO0OOO0O ,OOOO0000O000000O0 ]#line:418
            Logger .info (O0O000OOOO0OO00O0 )#line:419
            OOOO0OOOOOOOO0OO0 =subprocess .run (O0O000OOOO0OO00O0 ,shell =False ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE )#line:420
            if OOOO0OOOOOOOO0OO0 .stderr :#line:422
                Logger .error (OOOO0OOOOOOOO0OO0 .stderr )#line:423
            else :#line:424
                OOOOO0OOOOOO0O00O =re .search (r'Demux complete.*(Demuxing time: .*)\\r',str (OOOO0OOOOOOOO0OO0 .stdout ))#line:425
                if OOOOO0OOOOOO0O00O :#line:426
                    Logger .info ('output:'+OOOO0000O000000O0 +' : '+OOOOO0OOOOOO0O00O .group (1 ))#line:427
            OO0OO000OO0000O00 =os .listdir (OOOO0000O000000O0 )#line:429
            if len (OO0OO000OO0000O00 )==1 :#line:430
                OO0OO000OO0000O00 =r'%s\%s'%(OOOO0000O000000O0 ,OO0OO000OO0000O00 [0 ])#line:431
                return O000O0O0OO0OO000O .changeaudio (OO0OO000OO0000O00 ,O00OO0O0OO0O000O0 ,O000OOO0OO0O0OOOO ,otherarg )#line:432
        return False #line:433
    def tsmerge (O0OO0O00O0OOOOO0O ,O0O000OO0O0OOOO00 ,O000OO0OO000OO0OO ,ntraks =None ,ntype =None ):#line:436
        O0O00O0O00O0OOOO0 =O0OO0O00O0OOOOO0O .tsinfo (O0O000OO0O0OOOO00 [0 ])#line:437
        if O0O00O0O00O0OOOO0 :#line:438
            OO0OO00OO0000OOO0 =os .path .dirname (O000OO0OO000OO0OO )#line:439
            OO0OOOOO00OO0O00O =r'%s\ts.meta'%OO0OO00OO0000OOO0 #line:440
            if not os .path .exists (OO0OO00OO0000OOO0 ):#line:442
                os .mkdir (OO0OO00OO0000OOO0 )#line:443
            OOOOOO00OO00O000O ='MUXOPT --no-pcr-on-video-pid --new-audio-pes --vbr  --vbv-len=500\n'#line:445
            for OO0OO0OOOO00O0OO0 in O0O00O0O00O0OOOO0 :#line:446
                if ntraks and OO0OO0OOOO00O0OO0 ['track_id']not in ntraks :#line:447
                    continue #line:448
                if ntype and OO0OO0OOOO00O0OO0 ['stream_type']!=ntype :#line:449
                    continue #line:450
                OOOOOO00OO00O000O +='%s, "%s", track=%s\n'%(OO0OO0OOOO00O0OO0 ['stream_id'],'"+"'.join (O0O000OO0O0OOOO00 ),OO0OO0OOOO00O0OO0 ['track_id'])#line:451
            O00OOOOOOO0O0OO00 =open (OO0OOOOO00OO0O00O ,'w',encoding ='utf-8')#line:453
            O00OOOOOOO0O0OO00 .write (OOOOOO00OO00O000O .strip ('\n'))#line:454
            O00OOOOOOO0O0OO00 .close ()#line:455
            OO0OO00O00O00OO0O =[Setting .tsmuxerbin ,OO0OOOOO00OO0O00O ,O000OO0OO000OO0OO ]#line:457
            Logger .info (OO0OO00O00O00OO0O )#line:458
            OO0O0O0O0OO0O000O =subprocess .run (OO0OO00O00O00OO0O ,shell =False ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE )#line:459
            if OO0O0O0O0OO0O000O .stderr :#line:461
                Logger .error (OO0O0O0O0OO0O000O .stderr )#line:462
            else :#line:463
                O0OOOOO0OOO0O0OOO =re .search (r'(.*)',str (OO0O0O0O0OO0O000O .stdout ))#line:464
                if O0OOOOO0OOO0O0OOO :#line:465
                    Logger .info ('output:'+O000OO0OO000OO0OO +' : '+O0OOOOO0OOO0O0OOO .group (1 ))#line:466
                    return True #line:467
        return False #line:468
    def getname (OOO00O00000O0O0OO ,O0O0O0OO00OOOOO0O ,O00OOO00O0O00O0OO ,otype ='',muti =False ):#line:471
        O0OOOO0O0O0OOOOO0 ={'pre':'','version':'','resolution':'','source':'BluRay','type':otype ,'bit':'','format':'','effect':'','audio':''}#line:473
        OOOOO0O00OO0OO0O0 =re .match (r'(.*[12]\d{3})\.(.*)-',O00OOO00O0O00O0OO )#line:474
        if OOOOO0O00OO0OO0O0 :#line:475
            O0OOOO0O0O0OOOOO0 ['pre']=OOOOO0O00OO0OO0O0 .group (1 )#line:476
            if muti :#line:478
                O000O00O0000O00O0 =re .search (r'\.S\d+\.',O0OOOO0O0O0OOOOO0 ['pre'])#line:479
                if not O000O00O0000O00O0 :#line:480
                    O0OOOO0O0O0OOOOO0 ['pre']=re .sub (r'(\.[12]\d{3})$',r'.S01\1',O0OOOO0O0O0OOOOO0 ['pre'])#line:481
            O000O0OOO000OO00O =OOO00O00000O0O0OO .mediainfo (O0O0O0OO00OOOOO0O )#line:482
            if O000O0OOO000OO00O .__contains__ ('video'):#line:483
                OO0O0OOOOO00O0OOO =O000O0OOO000OO00O ['video'][0 ]#line:484
                if not O0OOOO0O0O0OOOOO0 ['type']and OO0O0OOOOO00O0OOO .__contains__ ('Writing library'):#line:487
                    O0OOOO0O0O0OOOOO0 ['type']=OO0O0OOOOO00O0OOO ['Writing library'].split (' ').pop (0 ).replace ('pro','')#line:488
                    if OO0O0OOOOO00O0OOO .__contains__ ('Bit depth')and OO0O0OOOOO00O0OOO ['Bit depth']!='8 bits':#line:490
                        O0OOOO0O0O0OOOOO0 ['bit']=re .sub (r'(\d+) bits',r'\1bit',OO0O0OOOOO00O0OOO ['Bit depth'])#line:491
                if O0OOOO0O0O0OOOOO0 ['type']=='Remux':#line:493
                    O0OOOO0O0O0OOOOO0 ['format']=OO0O0OOOOO00O0OOO ['Format']#line:494
                _OOOOO0O00OO000OO0 ='1080'#line:495
                if int (re .sub (r'\D','',OO0O0OOOOO00O0OOO ['Height']))>1080 or int (re .sub (r'\D','',OO0O0OOOOO00O0OOO ['Width']))>1920 :#line:497
                    _OOOOO0O00OO000OO0 ='2160'#line:498
                _OO000OOOOOO0O0O0O ='p'#line:499
                if O0OOOO0O0O0OOOOO0 ['type']=='Remux'and OO0O0OOOOO00O0OOO .__contains__ ('Scan type')and OO0O0OOOOO00O0OOO ['Scan type']!='Progressive':#line:501
                    _OO000OOOOOO0O0O0O ='i'#line:502
                if _OOOOO0O00OO000OO0 =='1080':#line:503
                    O0OOOO0O0O0OOOOO0 ['resolution']='%s%s'%(_OOOOO0O00OO000OO0 ,_OO000OOOOOO0O0O0O )#line:504
                else :#line:505
                    O0OOOO0O0O0OOOOO0 ['resolution']='%s%s.UHD'%(_OOOOO0O00OO000OO0 ,_OO000OOOOOO0O0O0O )#line:506
                    if OO0O0OOOOO00O0OOO .__contains__ ('Color primaries')and OO0O0OOOOO00O0OOO ['Color primaries']!='BT.709':#line:507
                        O0OOOO0O0O0OOOOO0 ['effect']='HDR'#line:508
                        if 'Dolby Vision'in OO0O0OOOOO00O0OOO ['HDR format']:#line:509
                            O0OOOO0O0O0OOOOO0 ['effect']='DV'#line:510
                if OO0O0OOOOO00O0OOO .__contains__ ('Original source medium'):#line:512
                    if OO0O0OOOOO00O0OOO ['Original source medium']!='Blu-ray':#line:513
                        O0OOOO0O0O0OOOOO0 ['source']=re .sub (r'\W','',OO0O0OOOOO00O0OOO ['Original source medium'])#line:514
                O0000O000O0O00O0O =[]#line:516
                if O000O0OOO000OO00O .__contains__ ('audio'):#line:517
                    OO00O0O00O0OO0000 ={}#line:518
                    O0O0000OOO0OO0O00 =0 #line:519
                    OOOO00O0O00OO0OO0 =0 #line:520
                    for O000O0OOO0OOOOO00 in O000O0OOO000OO00O ['audio']:#line:521
                        OOOO00O0O00OO0OO0 +=1 #line:522
                        if O000O0OOO0OOOOO00 .__contains__ ('Channel(s)'):#line:523
                            OOO0000OOO00000O0 =re .search (r'(\d+) channel',O000O0OOO0OOOOO00 ['Channel(s)'])#line:524
                            O00OOO0000O0OOO0O =int (OOO0000OOO00000O0 .group (1 ))#line:525
                        else :#line:526
                            O00OOO0000O0OOO0O =1 #line:527
                        if (not OO00O0O00O0OO0000 )or O00OOO0000O0OOO0O >O0O0000OOO0OO0O00 :#line:528
                            OO00O0O00O0OO0000 =O000O0OOO0OOOOO00 #line:529
                            O0O0000OOO0OO0O00 =O00OOO0000O0OOO0O #line:530
                    OOO0O00OOO0000O0O =re .sub (r'(\w+).*',r'\1',OO00O0O00O0OO0000 ['Format'])#line:533
                    O0OO0000O0OOO0OOO =''#line:534
                    if OO00O0O00O0OO0000 .__contains__ ('Commercial name'):#line:535
                        O0OO0000O0OOO0OOO =OO00O0O00O0OO0000 ['Commercial name']#line:536
                    O00OO00OO0OOOO0O0 =''#line:537
                    if OOO0O00OOO0000O0O =='DTS':#line:538
                        if O0OO0000O0OOO0OOO =='DTS-HD Master Audio':#line:540
                            OOO0O00OOO0000O0O =OOO0O00OOO0000O0O +'-HD.MA'#line:541
                    elif OOO0O00OOO0000O0O =='MLP':#line:542
                        if 'TrueHD'in O0OO0000O0OOO0OOO :#line:543
                            OOO0O00OOO0000O0O ='TrueHD'#line:544
                        if 'Atmos'in O0OO0000O0OOO0OOO :#line:545
                            O00OO00OO0OOOO0O0 ='Atmos'#line:546
                    if OOO0O00OOO0000O0O =='AC-3':#line:548
                        OOO0O00OOO0000O0O ='DD'#line:549
                    elif OOO0O00OOO0000O0O =='PCM':#line:550
                        OOO0O00OOO0000O0O ='LPCM'#line:551
                    O0000O000O0O00O0O .append (OOO0O00OOO0000O0O )#line:552
                    if O0O0000OOO0OO0O00 in (1 ,2 ,5 ):#line:562
                        OO0OOO0000000O0O0 =str (O0O0000OOO0OO0O00 )+'.0'#line:563
                    else :#line:564
                        OO0OOO0000000O0O0 =str (O0O0000OOO0OO0O00 -1 )+'.1'#line:565
                    if OOO0O00OOO0000O0O !='DTS'or OO0OOO0000000O0O0 !='5.1':#line:566
                        O0000O000O0O00O0O .append (OO0OOO0000000O0O0 )#line:567
                    if O00OO00OO0OOOO0O0 :#line:570
                        O0000O000O0O00O0O .append (O00OO00OO0OOOO0O0 )#line:571
                    if OOOO00O0O00OO0OO0 >1 :#line:574
                        O0000O000O0O00O0O .append ('%sAudio'%str (OOOO00O0O00OO0OO0 ))#line:575
                O0OOOO0O0O0OOOOO0 ['audio']='.'.join (O0000O000O0O00O0O )#line:577
                OO000O0O00OO00000 =[]#line:580
                _OO0OOOOOOO00OO0O0 =OOOOO0O00OO0OO0O0 .group (2 )#line:581
                O0OOOOO0O000O0O00 =[['Director','cut','DC'],'Extended','Theatrical','Unrated','Limited','Uncut',['Criterion','Collection','CC'],'CC','DC']#line:583
                for O0000O0OOO00000OO in O0OOOOO0O000O0O00 :#line:584
                    O00OOO0O00OOO0OO0 =True #line:585
                    O0OO0O0OOOOOOOO00 =''#line:586
                    if isinstance (O0000O0OOO00000OO ,list ):#line:587
                        O0OO0O0OOOOOOOO00 =O0000O0OOO00000OO .pop ()#line:588
                        for OOOOO0O000OOO0O00 in O0000O0OOO00000OO :#line:589
                            if not re .search (OOOOO0O000OOO0O00 ,_OO0OOOOOOO00OO0O0 ,re .IGNORECASE ):#line:590
                                O00OOO0O00OOO0OO0 =False #line:591
                                break #line:592
                    else :#line:593
                        if not re .search (O0000O0OOO00000OO ,_OO0OOOOOOO00OO0O0 ,re .IGNORECASE ):#line:594
                            O00OOO0O00OOO0OO0 =False #line:595
                    if O00OOO0O00OOO0OO0 :#line:596
                        if O0OO0O0OOOOOOOO00 :#line:597
                            OO000O0O00OO00000 .append (O0OO0O0OOOOOOOO00 )#line:598
                        else :#line:599
                            OO000O0O00OO00000 .append (O0000O0OOO00000OO )#line:600
                O0OOOO0O0O0OOOOO0 ['version']='.'.join (OO000O0O00OO00000 )#line:601
        O00OOO0O0000O0OO0 =''#line:603
        for O00O0OOO0O00OOOO0 in O0OOOO0O0O0OOOOO0 .values ():#line:604
            if O00O0OOO0O00OOOO0 :#line:605
                O00OOO0O0000O0OO0 ='%s.%s'%(O00OOO0O0000O0OO0 ,O00O0OOO0O00OOOO0 )#line:606
        return "%s-MeYu"%O00OOO0O0000O0OO0 .strip ('.')#line:607
