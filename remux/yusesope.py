from argparse import RawTextHelpFormatter #line:3
from bitstring import BitStream #line:4
from ctypes import *#line:5
import argparse #line:6
import time #line:7
import sys #line:8
import os #line:9
import multiprocessing as mp #line:12
import subprocess as sp #line:13
import psutil #line:14
import re #line:15
from plugins .remux .setting import Setting #line:16
class FFmpeg :#line:29
	def __init__ (OO0OO00000OO0O0OO ,OOO000OOO0000O000 ):#line:30
		super (FFmpeg ,OO0OO00000OO0O0OO ).__init__ ()#line:31
		OO0OO00000OO0O0OO .input_file =OOO000OOO0000O000 #line:32
		OO0OO00000OO0O0OO .FFMPEG_BIN =Setting .ffmpegbin #line:33
		OO0OO00000OO0O0OO .info =OO0OO00000OO0O0OO .get_info ()#line:34
		OO0OO00000OO0O0OO .is_running =False #line:35
		OO0OO00000OO0O0OO .process =None #line:36
	def open_pipe (O00OO0O0OO000OO00 ,OOO0OOO00O0OOOO0O ,O0OO00OO000O0OOOO ):#line:38
		O0OO00000OO00O0OO ={"bl":0 ,"el":1 }#line:42
		O0OOOO0000OOO0OOO =[O00OO0O0OO000OO00 .FFMPEG_BIN ,'-hide_banner','-loglevel','panic','-i',O00OO0O0OO000OO00 .input_file ,'-map','0:{}'.format (O0OO00000OO00O0OO .get (OOO0OOO00O0OOOO0O )),'-c','copy','-f','hevc','-']#line:56
		O00O000O000OOO00O =sp .Popen (O0OOOO0000OOO0OOO ,stdout =sp .PIPE ,bufsize =O0OO00OO000O0OOOO )#line:61
		O00OO0O0OO000OO00 .is_running =True #line:62
		O00OO0O0OO000OO00 .process =psutil .Process (O00O000O000OOO00O .pid )#line:63
		return O00O000O000OOO00O #line:64
	def kill (OO00OO0O0O00O0O0O ,O000OOO0O0000O00O ):#line:66
		for O0OOOOO0O0O00OOO0 in OO00OO0O0O00O0O0O .process .children (recursive =True ):#line:68
			O0OOOOO0O0O00OOO0 .kill ()#line:69
		OO00OO0O0O00O0O0O .process .kill ()#line:70
		OO00OO0O0O00O0O0O .is_running =False #line:71
	@staticmethod #line:73
	def get_sec (O0OO0OO00O00OOO00 ):#line:74
		OO0O0000OO00OO0O0 ,O00O0000OO00O0OOO =O0OO0OO00O00OOO00 .split (".")#line:75
		OO0O00OOOOOOO0000 ,O0O000OOOO0OOOOO0 ,OO00O0O000000O0O0 =OO0O0000OO00OO0O0 .split (":")#line:76
		return int (OO0O00OOOOOOO0000 )*3600 +int (O0O000OOOO0OOOOO0 )*60 +int (OO00O0O000000O0O0 )+(float (O00O0000OO00O0OOO )/100 )#line:77
	def get_info (O0OOOOO0O000000OO ):#line:79
		OOOOOOO0O0OO0000O =re .compile (r"(vui_num_units_in_tick|vui_time_scale).*?=\s?(\d+)")#line:80
		OO0O00OOOO0O00O00 =re .compile (r"duration:\s?(\d{2}:\d{2}:\d{2}\.\d{2})",re .I )#line:81
		OOO0OO0OOO000O00O =re .compile (r"stream\s?#0:\d[\[\]0-9x]+:\s?video:",re .I )#line:82
		O0OOOOO00OO0O000O =False #line:83
		OOOO00OO0O0O0O0OO =dict (duration =0 ,vui_num_units_in_tick =0 ,vui_time_scale =0 ,)#line:88
		O0OO000000000000O =0 #line:89
		O0OOO0O000OOOOO00 =[O0OOOOO0O000000OO .FFMPEG_BIN ,'-hide_banner','-i',O0OOOOO0O000000OO .input_file ,'-c','copy','-bsf:v','trace_headers','-f','null','-']#line:98
		OOO0O000O00OOOO00 =sp .Popen (O0OOO0O000OOOOO00 ,stdout =sp .PIPE ,stderr =sp .STDOUT ,universal_newlines =True )#line:104
		O0OOOOO0O000000OO .is_running =True #line:105
		O0OOOOO0O000000OO .process =psutil .Process (OOO0O000O00OOOO00 .pid )#line:106
		OO0O00OO000O00O0O =0 #line:107
		for O0O0O00OO00O0OO00 in OOO0O000O00OOOO00 .stdout :#line:108
			if not O0OO000000000000O >=2 :#line:109
				OOOO0O00OOO0000O0 =re .search (OOO0OO0OOO000O00O ,O0O0O00OO00O0OO00 )#line:110
				if OOOO0O00OOO0000O0 :#line:111
					O0OO000000000000O +=1 #line:112
			if not OOOO00OO0O0O0O0OO ["duration"]:#line:113
				O0OO000OO0O0OOO0O =re .search (OO0O00OOOO0O00O00 ,O0O0O00OO00O0OO00 )#line:114
				if O0OO000OO0O0OOO0O :#line:115
					OOOO00OO0O0O0O0OO ["duration"]=O0OOOOO0O000000OO .get_sec (O0OO000OO0O0OOO0O .group (1 ))#line:116
			elif not O0OOOOO00OO0O000O and "Sequence Parameter Set"in O0O0O00OO00O0OO00 :#line:117
				O0OOOOO00OO0O000O =True #line:118
			elif O0OOOOO00OO0O000O :#line:119
				OOOO00O0000O0O0OO =re .search (OOOOOOO0O0OO0000O ,O0O0O00OO00O0OO00 )#line:120
				if OOOO00O0000O0O0OO :#line:121
					OOOO00OO0O0O0O0OO [OOOO00O0000O0O0OO .group (1 )]=float (OOOO00O0000O0O0OO .group (2 ))#line:122
			OO0O00OO000O00O0O +=1 #line:124
			if len (list (filter (None ,[OO0O00O00OO0OOO0O !=0 for OO0O00O00OO0OOO0O in OOOO00OO0O0O0O0OO .values ()])))==len (OOOO00OO0O0O0O0OO )or OO0O00OO000O00O0O >2000 or not O0O0O00OO00O0OO00 :#line:125
				O0OOOOO0O000000OO .kill (OOO0O000O00OOOO00 .pid )#line:126
				break #line:127
		return dict (n_video_stream =O0OO000000000000O ,vui_timing_info =OOOO00OO0O0O0O0OO )#line:128
class Reader_Experimental (mp .Process ):#line:131
	def __init__ (OO0O00OOOOO0OO000 ,O0O00O000OOO00000 ,OOOOO0O0OO0OO0OOO ,OO0000O0OO0O0OO00 ):#line:137
		super (Reader_Experimental ,OO0O00OOOOO0OO000 ).__init__ ()#line:138
		OO0O00OOOOO0OO000 .file =O0O00O000OOO00000 #line:139
		OO0O00OOOOO0OO000 .dv_layer =OOOOO0O0OO0OO0OOO #line:140
		OO0O00OOOOO0OO000 .ffmpeg =FFmpeg (OO0O00OOOOO0OO000 .file )#line:141
		OO0O00OOOOO0OO000 .skip_hdr10plus_flag =OO0000O0OO0O0OO00 #line:142
		OO0O00OOOOO0OO000 .output_queue =mp .Queue ()#line:143
		OO0O00OOOOO0OO000 .event =mp .Event ()#line:144
		OO0O00OOOOO0OO000 .event .set ()#line:145
		OO0O00OOOOO0OO000 .active =mp .Event ()#line:146
		OO0O00OOOOO0OO000 .active .set ()#line:147
		OO0O00OOOOO0OO000 .pipe =None #line:148
		OO0O00OOOOO0OO000 .chunk_size =1024 *1024 *1 #line:149
		OO0O00OOOOO0OO000 .global_offset =0 #line:150
		OO0O00OOOOO0OO000 .buffer =[]#line:151
		OO0O00OOOOO0OO000 .starting_nalus =[NalUnitType .NAL_UNIT_ACCESS_UNIT_DELIMITER ,NalUnitType .NAL_UNIT_VPS ,NalUnitType .NAL_UNIT_SPS ,NalUnitType .NAL_UNIT_PPS ,NalUnitType .NAL_UNIT_PREFIX_SEI ]#line:158
		OO0O00OOOOO0OO000 .slice_nalu =[NalUnitType .NAL_UNIT_CODED_SLICE_TRAIL_N ,NalUnitType .NAL_UNIT_CODED_SLICE_TRAIL_R ,NalUnitType .NAL_UNIT_CODED_SLICE_TSA_N ,NalUnitType .NAL_UNIT_CODED_SLICE_TSA_R ,NalUnitType .NAL_UNIT_CODED_SLICE_STSA_N ,NalUnitType .NAL_UNIT_CODED_SLICE_STSA_R ,NalUnitType .NAL_UNIT_CODED_SLICE_RADL_N ,NalUnitType .NAL_UNIT_CODED_SLICE_RADL_R ,NalUnitType .NAL_UNIT_CODED_SLICE_RASL_N ,NalUnitType .NAL_UNIT_CODED_SLICE_RASL_R ,NalUnitType .NAL_UNIT_CODED_SLICE_BLA_W_LP ,NalUnitType .NAL_UNIT_CODED_SLICE_BLA_W_RADL ,NalUnitType .NAL_UNIT_CODED_SLICE_BLA_N_LP ,NalUnitType .NAL_UNIT_CODED_SLICE_IDR_W_RADL ,NalUnitType .NAL_UNIT_CODED_SLICE_IDR_N_LP ,NalUnitType .NAL_UNIT_CODED_SLICE_CRA ]#line:176
		OO0O00OOOOO0OO000 .dts_set =False #line:177
		OO0O00OOOOO0OO000 .latest_dts =0 #line:178
		OO0O00OOOOO0OO000 .tc =OO0O00OOOOO0OO000 .set_tc ()#line:179
	def get_file_duration (O000000O00O0OOOOO ):#line:181
		return O000000O00O0OOOOO .ffmpeg .info .get ("vui_timing_info").get ("duration")#line:182
	def set_tc (O0O0O0O00OOO000OO ):#line:184
		OOOOOOOOOOO0O0O00 =O0O0O0O00OOO000OO .ffmpeg .info .get ("vui_timing_info")#line:185
		if OOOOOOOOOOO0O0O00 ["vui_num_units_in_tick"]and OOOOOOOOOOO0O0O00 ["vui_time_scale"]:#line:186
			OOO000O0OOO0OO0OO =OOOOOOOOOOO0O0O00 ["vui_num_units_in_tick"]/OOOOOOOOOOO0O0O00 ["vui_time_scale"]#line:187
		else :#line:188
			OOO000O0OOO0OO0OO =-1 #line:189
		return OOO000O0OOO0OO0OO #line:190
	def reset_buffer (OOOO0O0OO00OOOOO0 ,nalu =None ):#line:192
		OOOO0O0OO00OOOOO0 .buffer =[]#line:193
		OOOO0O0OO00OOOOO0 .dts_set =False #line:194
		if nalu :#line:195
			OOOO0O0OO00OOOOO0 .buffer .append (nalu )#line:196
	def add_nalu_to_au (OOO0000OOO0O0OO0O ,O0O0O0O00OO000O0O ):#line:198
		if O0O0O0O00OO000O0O .type in OOO0000OOO0O0OO0O .starting_nalus :#line:199
			if OOO0000OOO0O0OO0O .buffer and OOO0000OOO0O0OO0O .buffer [-1 ].type not in OOO0000OOO0O0OO0O .starting_nalus :#line:200
				OOO0000OOO0O0OO0O .output_queue .put (OOO0000OOO0O0OO0O .buffer )#line:201
				OOO0000OOO0O0OO0O .reset_buffer ()#line:202
		elif O0O0O0O00OO000O0O .type in OOO0000OOO0O0OO0O .slice_nalu :#line:203
			if (OOO0000OOO0O0OO0O .tc >0 )and not OOO0000OOO0O0OO0O .dts_set :#line:204
				O0O0O0O00OO000O0O .dts =OOO0000OOO0O0OO0O .latest_dts +OOO0000OOO0O0OO0O .tc #line:205
				OOO0000OOO0O0OO0O .latest_dts =O0O0O0O00OO000O0O .dts #line:206
				OOO0000OOO0O0OO0O .dts_set =True #line:207
		OOO0000OOO0O0OO0O .buffer .append (O0O0O0O00OO000O0O )#line:208
	@staticmethod #line:210
	def get_dummy_data ():#line:211
		OOO000OO0000OOO0O ="00000001460110"#line:212
		return BitStream ("0x{0}{0}".format (OOO000OO0000OOO0O )).bytes #line:213
	@staticmethod #line:215
	def get_list_offsets (OO0000OOOO0OOOO00 ):#line:216
		OOOOO000O0O0O0O00 =list (OO0000OOOO0OOOO00 .findall ('0x000001',bytealigned =True ))#line:217
		return OOOOO000O0O0O0O00 #line:218
	def parse_nalus (O0000O0O00OO0OOO0 ,OO00OO00O00O00000 ,OO0OO0O0O0O0OO000 ):#line:220
		for OO00O0000O000OO0O in range (0 ,(len (OO00OO00O00O00000 )-1 )):#line:221
			OOO0O00O0O0000000 =NalUnit ()#line:222
			OOO0O00O0O0000000 .dv_layer =O0000O0O00OO0OOO0 .dv_layer #line:223
			OOO0O00O0O0000000 .offset =OO00OO00O00O00000 [OO00O0000O000OO0O ]#line:224
			OOO0O00O0O0000000 .global_offset =O0000O0O00OO0OOO0 .global_offset +OOO0O00O0O0000000 .offset #line:225
			OOO0O00O0O0000000 .type =OO0OO0O0O0O0OO000 [(OOO0O00O0O0000000 .offset +25 ):(OOO0O00O0O0000000 .offset +31 )].uint #line:226
			OOO0O00O0O0000000 .size =OO00OO00O00O00000 [OO00O0000O000OO0O +1 ]-OOO0O00O0O0000000 .offset #line:227
			if OO0OO0O0O0O0OO000 [(OOO0O00O0O0000000 .offset +OOO0O00O0O0000000 .size -8 ):(OOO0O00O0O0000000 .offset +OOO0O00O0O0000000 .size +24 )]=="0x00000001":#line:228
				OOO0O00O0O0000000 .size -=8 #line:229
			OOO0O00O0O0000000 .data =OO0OO0O0O0O0OO000 [(OOO0O00O0O0000000 .offset +24 ):(OOO0O00O0O0000000 .offset +OOO0O00O0O0000000 .size )]#line:230
			if O0000O0O00OO0OOO0 .skip_hdr10plus_flag and O0000O0O00OO0OOO0 .dv_layer !="el"and OOO0O00O0O0000000 .type ==NalUnitType .NAL_UNIT_PREFIX_SEI :#line:233
				if OOO0O00O0O0000000 .data [:24 ]=="0x4E0104":#line:235
					continue #line:236
			O0000O0O00OO0OOO0 .add_nalu_to_au (OOO0O00O0O0000000 )#line:237
		return True #line:238
	def read (OO00O00000OOO00OO ,OO0OO000OOOO00O00 ):#line:240
		OO0O0OOO0O0OO0O0O =OO00O00000OOO00OO .get_list_offsets (OO0OO000OOOO00O00 )#line:241
		OO00O00000OOO00OO .parse_nalus (OO0O0OOO0O0OO0O0O ,OO0OO000OOOO00O00 )#line:242
		O000OOO0000O0OO0O =OO0O0OOO0O0OO0O0O .pop (-1 )#line:243
		return O000OOO0000O0OO0O #line:244
	def chunks (OOOO0O0O0000OOO0O ):#line:246
		while True :#line:247
			OOOOOO00O0O0OO0O0 =OOOO0O0O0000OOO0O .pipe .stdout .read (OOOO0O0O0000OOO0O .chunk_size )#line:248
			if not OOOOOO00O0O0OO0O0 :#line:249
				OOOOOO00O0O0OO0O0 =OOOO0O0O0000OOO0O .get_dummy_data ()#line:250
				OOOO0O0O0000OOO0O .active .clear ()#line:251
			yield OOOOOO00O0O0OO0O0 #line:252
			if not OOOO0O0O0000OOO0O .active .is_set ():#line:253
				break #line:254
			OOOO0O0O0000OOO0O .event .wait ()#line:255
	def standby (OO0O00O00OOO000OO ):#line:257
		OO0O00O00OOO000OO .event .clear ()#line:258
		OO0O00O00OOO000OO .event .wait ()#line:259
	def run (O000O00OO00000000 ):#line:261
		O000O00OO00000000 .pipe =O000O00OO00000000 .ffmpeg .open_pipe (O000O00OO00000000 .dv_layer ,O000O00OO00000000 .chunk_size )#line:263
		O00OO0OO0OOOOO000 =BitStream ("")#line:264
		while True :#line:266
			for O00000O0000O00O0O in O000O00OO00000000 .chunks ():#line:267
				O0OO00O000O0OO000 =BitStream (bytes =O00000O0000O00O0O )#line:268
				O0OO00O000O0OO000 .prepend (O00OO0OO0OOOOO000 )#line:269
				O0O0O000O0OO0O00O =O000O00OO00000000 .read (O0OO00O000O0OO000 )#line:270
				O00OO0OO0OOOOO000 =O0OO00O000O0OO000 [O0O0O000O0OO0O00O :]#line:271
				O000O00OO00000000 .global_offset +=(len (O0OO00O000O0OO000 )-len (O00OO0OO0OOOOO000 ))#line:272
			if not O000O00OO00000000 .active .is_set ():#line:273
				O000O00OO00000000 .output_queue .put ("END")#line:274
				O000O00OO00000000 .standby ()#line:275
class Writer_Experimental (mp .Process ):#line:278
	def __init__ (OOO0O000OOOOOO000 ,OOOO00OO00OOO0OOO ,O0O0OO0000OO000OO ,OO000OOO0O0000000 ,OO0O00O00OOOO00O0 ):#line:285
		super (Writer_Experimental ,OOO0O000OOOOOO000 ).__init__ ()#line:286
		OOO0O000OOOOOO000 .out_file =OOOO00OO00OOO0OOO #line:287
		OOO0O000OOOOOO000 .out_file_handler =None #line:288
		OOO0O000OOOOOO000 .list_readers_queue =O0O0OO0000OO000OO #line:289
		OOO0O000OOOOOO000 .mode =OO000OOO0O0000000 #line:290
		OOO0O000OOOOOO000 .fel_to_mel_flag =OO0O00O00OOOO00O0 #line:291
		OOO0O000OOOOOO000 .total_written_au =0 #line:292
		OOO0O000OOOOOO000 .active =mp .Event ()#line:293
		OOO0O000OOOOOO000 .active .set ()#line:294
		OOO0O000OOOOOO000 .output_queue =mp .Queue ()#line:295
		OOO0O000OOOOOO000 .written_data ={"bl":0 ,"el":0 ,"dts_bl":0 ,"dts_el":0 }#line:296
		OOO0O000OOOOOO000 .cpp_lib =None #line:297
		OOO0O000OOOOOO000 .buffer =BitStream ("")#line:298
		OOO0O000OOOOOO000 .MAX_BUFFER_SIZE =10 *1024 *1024 #line:299
		OOO0O000OOOOOO000 .pipe =None #line:300
	@staticmethod #line:302
	def init_cpp_lib ():#line:303
		OO0O000OOO0000000 ="linux_cpp_lib.so"#line:304
		O0OO0000OO0000OO0 =os .path .join (os .path .dirname (os .path .realpath (__file__ )),OO0O000OOO0000000 )#line:309
		O0OOO0OO0O00000OO =cdll .LoadLibrary (O0OO0000OO0000OO0 )#line:310
		O0OOO0OO0O00000OO .generate_mel_rpu .argstype =[POINTER (c_ubyte ),c_int ,POINTER (c_int )]#line:315
		O0OOO0OO0O00000OO .generate_mel_rpu .restype =POINTER (c_ubyte )#line:316
		O0OOO0OO0O00000OO .generate_profile81_rpu .argstype =[POINTER (c_ubyte ),c_int ,POINTER (c_int )]#line:321
		O0OOO0OO0O00000OO .generate_profile81_rpu .restype =POINTER (c_ubyte )#line:322
		return O0OOO0OO0O00000OO #line:323
	def fel_to_mel (OO00000OO0OOOOO00 ,O0O00000O0O0OO00O ):#line:325
		OO0O0OOOO00O0O0OO =NalUnit ()#line:326
		try :#line:328
			O0OO0O0O000O000O0 =c_uint ()#line:329
			O00000O0OO0000O00 =OO00000OO0OOOOO00 .cpp_lib .generate_mel_rpu (create_string_buffer (O0O00000O0O0OO00O .data .bytes ,int (O0O00000O0O0OO00O .data .len /8 )),int (O0O00000O0O0OO00O .data .len /8 ),byref (O0OO0O0O000O000O0 ))#line:337
			OO0O0OOOO00O0O0OO .data =BitStream (bytearray (O00000O0OO0000O00 [:O0OO0O0O000O000O0 .value ]))#line:342
			OO00000OO0OOOOO00 .cpp_lib .free_rpu (O00000O0OO0000O00 )#line:343
		except :#line:344
			pass #line:345
		return OO0O0OOOO00O0O0OO #line:347
	def uhd_bd_to_profile81 (O00O00O0OO00O0OO0 ,OOOO000000OOO0OOO ):#line:349
		OOOO0O00000OO0000 =NalUnit ()#line:350
		try :#line:352
			OO00OOO000O0000OO =c_uint ()#line:353
			O0OOOO0O0O0000000 =O00O00O0OO00O0OO0 .cpp_lib .generate_profile81_rpu (create_string_buffer (OOOO000000OOO0OOO .data .bytes ,int (OOOO000000OOO0OOO .data .len /8 )),int (OOOO000000OOO0OOO .data .len /8 ),byref (OO00OOO000O0000OO ))#line:361
			OOOO0O00000OO0000 .data =BitStream (bytearray (O0OOOO0O0O0000000 [:OO00OOO000O0000OO .value ]))#line:366
			O00O00O0OO00O0OO0 .cpp_lib .free_rpu (O0OOOO0O0O0000000 )#line:367
		except :#line:368
			pass #line:369
		return OOOO0O00000OO0000 #line:371
	def update_written_data (O00O00OOOOOOO00O0 ,O0000OO0O0OO0O000 ):#line:373
		if isinstance (O0000OO0O0OO0O000 ,NalUnit ):#line:374
			O00O00OOOOOOO00O0 .written_data [O0000OO0O0OO0O000 .dv_layer ]=O0000OO0O0OO0O000 .global_offset +O0000OO0O0OO0O000 .size #line:375
			O00O00OOOOOOO00O0 .output_queue .put (O00O00OOOOOOO00O0 .written_data )#line:376
	def fill_buffer (O0O0OO0000O0000OO ,O000O000OO0O0O0O0 ):#line:378
		for OO000OOO000OOO0OO in O000O000OO0O0O0O0 :#line:379
			if isinstance (OO000OOO000OOO0OO ,NalUnit )and OO000OOO000OOO0OO .data :#line:380
				if OO000OOO000OOO0OO .dv_layer =="bl":#line:381
					OO000OOO000OOO0OO .data .prepend ("0x00000001")#line:382
					O0O0OO0000O0000OO .buffer .append (OO000OOO000OOO0OO .data )#line:383
				elif OO000OOO000OOO0OO .dv_layer =="el":#line:384
					if OO000OOO000OOO0OO .type ==NalUnitType .NAL_UNIT_UNSPECIFIED_62 :#line:385
						if O0O0OO0000O0000OO .fel_to_mel_flag :#line:386
							OO000OOO000OOO0OO =O0O0OO0000O0000OO .fel_to_mel (OO000OOO000OOO0OO )#line:387
						elif O0O0OO0000O0000OO .mode ==2 :#line:388
							OO000OOO000OOO0OO =O0O0OO0000O0000OO .uhd_bd_to_profile81 (OO000OOO000OOO0OO )#line:389
						OO000OOO000OOO0OO .data .prepend ("0x00000001")#line:390
						O0O0OO0000O0000OO .buffer .append (OO000OOO000OOO0OO .data )#line:391
					else :#line:392
						if O0O0OO0000O0000OO .mode ==1 :#line:393
							OO000OOO000OOO0OO .data .prepend ("0x000000017e01")#line:394
							O0O0OO0000O0000OO .buffer .append (OO000OOO000OOO0OO .data )#line:395
				if OO000OOO000OOO0OO .dts :#line:396
					O0O0OO0000O0000OO .written_data ["dts_{}".format (OO000OOO000OOO0OO .dv_layer )]=OO000OOO000OOO0OO .dts #line:397
	def write (O0O0OOO00000OOOOO ):#line:399
		if O0O0OOO00000OOOOO .buffer .len !=0 :#line:400
			try :#line:401
				O0O0OOO00000OOOOO .buffer .tofile (O0O0OOO00000OOOOO .out_file_handler )#line:402
				O0O0OOO00000OOOOO .buffer .clear ()#line:403
			except :#line:404
				O0O0OOO00000OOOOO .active .clear ()#line:405
	def run (OOOO0O0OOOO00O0O0 ):#line:407
		with open (OOOO0O0OOOO00O0O0 .out_file ,'wb')as OOO0OOOOOOOO000O0 :#line:409
			try :#line:410
				OOOO0O0OOOO00O0O0 .out_file_handler =OOO0OOOOOOOO000O0 #line:411
				if OOOO0O0OOOO00O0O0 .fel_to_mel_flag or OOOO0O0OOOO00O0O0 .mode ==2 :#line:412
					OOOO0O0OOOO00O0O0 .cpp_lib =OOOO0O0OOOO00O0O0 .init_cpp_lib ()#line:413
				O0OO000OO0OO00O00 =0 #line:415
				OO0O0O0O0O000O00O =0 #line:416
				while True :#line:417
					O0000O0O000OOO0O0 =OOOO0O0OOOO00O0O0 .list_readers_queue [O0OO000OO0OO00O00 ].get ()#line:418
					if O0000O0O000OOO0O0 =="END":#line:420
						OO0O0O0O0O000O00O +=1 #line:421
						if len (OOOO0O0OOOO00O0O0 .list_readers_queue )==OO0O0O0O0O000O00O :#line:422
							OOOO0O0OOOO00O0O0 .active .clear ()#line:423
					else :#line:424
						OOOO0O0OOOO00O0O0 .fill_buffer (O0000O0O000OOO0O0 )#line:425
						OOOO0O0OOOO00O0O0 .update_written_data (O0000O0O000OOO0O0 [-1 ])#line:426
						OOOO0O0OOOO00O0O0 .total_written_au +=1 #line:428
					O0OO000OO0OO00O00 ^=1 #line:430
					if OOOO0O0OOOO00O0O0 .buffer .len >OOOO0O0OOOO00O0O0 .MAX_BUFFER_SIZE or not OOOO0O0OOOO00O0O0 .active .is_set ():#line:432
						OOOO0O0OOOO00O0O0 .write ()#line:433
					if not OOOO0O0OOOO00O0O0 .active .is_set ():#line:435
						break #line:436
			except KeyboardInterrupt :#line:438
				sys .stdout .close ()#line:439
				OOOO0O0OOOO00O0O0 .active .clear ()#line:440
def format_size (O0O00OOOO0OOO00O0 ):#line:443
	_OO0O0O00OOOOO0000 =O0O00OOOO0OOO00O0 /8 #line:444
	if _OO0O0O00OOOOO0000 >1024 *1024 *1024 :#line:445
		O00000000O0OO0OOO ="{:>7.2f} GB".format (round (_OO0O0O00OOOOO0000 /1024 /1024 /1024 ,2 ))#line:446
	elif _OO0O0O00OOOOO0000 >1024 *1024 :#line:447
		O00000000O0OO0OOO ="{:>7.2f} MB".format (round (_OO0O0O00OOOOO0000 /1024 /1024 ,2 ))#line:448
	elif _OO0O0O00OOOOO0000 >1024 :#line:449
		O00000000O0OO0OOO ="{:>7.2f} KB".format (round (_OO0O0O00OOOOO0000 /1024 ,2 ))#line:450
	else :#line:451
		O00000000O0OO0OOO ="{:>7}  B".format (_OO0O0O00OOOOO0000 )#line:452
	return O00000000O0OO0OOO #line:453
def graceful_shutdown (O00000O0O000O0OO0 ):#line:456
	for O0OO00O0OOOO0OOO0 in reversed (range (0 ,len (O00000O0O000O0OO0 ))):#line:457
		while True :#line:458
			if not O00000O0O000O0OO0 [O0OO00O0OOOO0OOO0 ].active .is_set ():#line:459
				break #line:460
		O00000O0O000O0OO0 [O0OO00O0OOOO0OOO0 ].terminate ()#line:461
	O00000O0O000O0OO0 =list ()#line:462
class NalUnitType :#line:467
	NAL_UNIT_CODED_SLICE_TRAIL_N =0 #line:468
	NAL_UNIT_CODED_SLICE_TRAIL_R =1 #line:469
	NAL_UNIT_CODED_SLICE_TSA_N =2 #line:471
	NAL_UNIT_CODED_SLICE_TSA_R =3 #line:472
	NAL_UNIT_CODED_SLICE_STSA_N =4 #line:474
	NAL_UNIT_CODED_SLICE_STSA_R =5 #line:475
	NAL_UNIT_CODED_SLICE_RADL_N =6 #line:477
	NAL_UNIT_CODED_SLICE_RADL_R =7 #line:478
	NAL_UNIT_CODED_SLICE_RASL_N =8 #line:480
	NAL_UNIT_CODED_SLICE_RASL_R =9 #line:481
	NAL_UNIT_RESERVED_VCL_N10 =10 #line:483
	NAL_UNIT_RESERVED_VCL_R11 =11 #line:484
	NAL_UNIT_RESERVED_VCL_N12 =12 #line:485
	NAL_UNIT_RESERVED_VCL_R13 =13 #line:486
	NAL_UNIT_RESERVED_VCL_N14 =14 #line:487
	NAL_UNIT_RESERVED_VCL_R15 =15 #line:488
	NAL_UNIT_CODED_SLICE_BLA_W_LP =16 #line:490
	NAL_UNIT_CODED_SLICE_BLA_W_RADL =17 #line:491
	NAL_UNIT_CODED_SLICE_BLA_N_LP =18 #line:492
	NAL_UNIT_CODED_SLICE_IDR_W_RADL =19 #line:493
	NAL_UNIT_CODED_SLICE_IDR_N_LP =20 #line:494
	NAL_UNIT_CODED_SLICE_CRA =21 #line:495
	NAL_UNIT_RESERVED_IRAP_VCL22 =22 #line:496
	NAL_UNIT_RESERVED_IRAP_VCL23 =23 #line:497
	NAL_UNIT_RESERVED_VCL24 =24 #line:499
	NAL_UNIT_RESERVED_VCL25 =25 #line:500
	NAL_UNIT_RESERVED_VCL26 =26 #line:501
	NAL_UNIT_RESERVED_VCL27 =27 #line:502
	NAL_UNIT_RESERVED_VCL28 =28 #line:503
	NAL_UNIT_RESERVED_VCL29 =29 #line:504
	NAL_UNIT_RESERVED_VCL30 =30 #line:505
	NAL_UNIT_RESERVED_VCL31 =31 #line:506
	NAL_UNIT_VPS =32 #line:508
	NAL_UNIT_SPS =33 #line:509
	NAL_UNIT_PPS =34 #line:510
	NAL_UNIT_ACCESS_UNIT_DELIMITER =35 #line:511
	NAL_UNIT_EOS =36 #line:512
	NAL_UNIT_EOB =37 #line:513
	NAL_UNIT_FILLER_DATA =38 #line:514
	NAL_UNIT_PREFIX_SEI =39 #line:515
	NAL_UNIT_SUFFIX_SEI =40 #line:516
	NAL_UNIT_RESERVED_NVCL41 =41 #line:518
	NAL_UNIT_RESERVED_NVCL42 =42 #line:519
	NAL_UNIT_RESERVED_NVCL43 =43 #line:520
	NAL_UNIT_RESERVED_NVCL44 =44 #line:521
	NAL_UNIT_RESERVED_NVCL45 =45 #line:522
	NAL_UNIT_RESERVED_NVCL46 =46 #line:523
	NAL_UNIT_RESERVED_NVCL47 =47 #line:524
	NAL_UNIT_UNSPECIFIED_48 =48 #line:525
	NAL_UNIT_UNSPECIFIED_49 =49 #line:526
	NAL_UNIT_UNSPECIFIED_50 =50 #line:527
	NAL_UNIT_UNSPECIFIED_51 =51 #line:528
	NAL_UNIT_UNSPECIFIED_52 =52 #line:529
	NAL_UNIT_UNSPECIFIED_53 =53 #line:530
	NAL_UNIT_UNSPECIFIED_54 =54 #line:531
	NAL_UNIT_UNSPECIFIED_55 =55 #line:532
	NAL_UNIT_UNSPECIFIED_56 =56 #line:533
	NAL_UNIT_UNSPECIFIED_57 =57 #line:534
	NAL_UNIT_UNSPECIFIED_58 =58 #line:535
	NAL_UNIT_UNSPECIFIED_59 =59 #line:536
	NAL_UNIT_UNSPECIFIED_60 =60 #line:537
	NAL_UNIT_UNSPECIFIED_61 =61 #line:538
	NAL_UNIT_UNSPECIFIED_62 =62 #line:539
	NAL_UNIT_UNSPECIFIED_63 =63 #line:540
	NAL_UNIT_INVALID =64 #line:541
class NalUnit (object ):#line:544
	def __init__ (O0O00O0OOOOO0O0OO ):#line:545
		O0O00O0OOOOO0O0OO ._offset =0 #line:546
		O0O00O0OOOOO0O0OO ._global_offset =0 #line:547
		O0O00O0OOOOO0O0OO ._size =0 #line:548
		O0O00O0OOOOO0O0OO ._type =None #line:549
		O0O00O0OOOOO0O0OO ._data =0 #line:550
		O0O00O0OOOOO0O0OO ._dv_layer =None #line:551
		O0O00O0OOOOO0O0OO ._nuh_layer_id =0 #line:552
		O0O00O0OOOOO0O0OO ._payload =None #line:553
		O0O00O0OOOOO0O0OO ._raw_data =None #line:554
		O0O00O0OOOOO0O0OO ._dts =0 #line:555
	@property #line:557
	def dts (O0O0O0OO0O0OOOOOO ):#line:558
		return O0O0O0OO0O0OOOOOO ._dts #line:559
	@dts .setter #line:561
	def dts (OO000OOO0O0OOOOO0 ,O000O000O00OO0OO0 ):#line:562
		OO000OOO0O0OOOOO0 ._dts =O000O000O00OO0OO0 #line:563
	@property #line:565
	def offset (O0O0O000O0O0000O0 ):#line:566
		return O0O0O000O0O0000O0 ._offset #line:567
	@offset .setter #line:569
	def offset (O0OOO00O000OOO0OO ,O0OO00O0OO00OOO00 ):#line:570
		O0OOO00O000OOO0OO ._offset =O0OO00O0OO00OOO00 #line:571
	@property #line:573
	def global_offset (O0O0000000O0O0OO0 ):#line:574
		return O0O0000000O0O0OO0 ._global_offset #line:575
	@global_offset .setter #line:577
	def global_offset (O000O00000O00OO0O ,O0O0000000O00OO00 ):#line:578
		O000O00000O00OO0O ._global_offset =O0O0000000O00OO00 #line:579
	@property #line:581
	def size (OO0O00O00O0O0O000 ):#line:582
		return OO0O00O00O0O0O000 ._size #line:583
	@size .setter #line:585
	def size (O0O000OOO0OOO00O0 ,OO00OO0O00O00OOOO ):#line:586
		O0O000OOO0OOO00O0 ._size =OO00OO0O00O00OOOO #line:587
	@property #line:589
	def type (O0000OOO0000OO00O ):#line:590
		return O0000OOO0000OO00O ._type #line:591
	@type .setter #line:593
	def type (OO00OO0O00O0OOOOO ,OOOO0O0OO0OOO0OOO ):#line:594
		OO00OO0O00O0OOOOO ._type =OOOO0O0OO0OOO0OOO #line:595
	@property #line:597
	def data (OO00O00OOOO0O0OOO ):#line:598
		return OO00O00OOOO0O0OOO ._data #line:599
	@data .setter #line:601
	def data (O0OO0O00O0O0O00O0 ,O00O000000000O0O0 ):#line:602
		O0OO0O00O0O0O00O0 ._data =O00O000000000O0O0 #line:603
	@property #line:605
	def dv_layer (OO0OOO0OOO0O00OOO ):#line:606
		return OO0OOO0OOO0O00OOO ._dv_layer #line:607
	@dv_layer .setter #line:609
	def dv_layer (O0O00OOOOOOOOOOOO ,OO00OOO0O00OOO00O ):#line:610
		O0O00OOOOOOOOOOOO ._dv_layer =OO00OOO0O00OOO00O #line:611
	@property #line:613
	def nuh_layer_id (O0O0O000OOOO0OO0O ):#line:614
		return O0O0O000OOOO0OO0O .nuh_layer_id #line:615
	@nuh_layer_id .setter #line:617
	def nuh_layer_id (OO00000O000O0O00O ,O0OOO0O0O0O0O0OO0 ):#line:618
		OO00000O000O0O00O ._nuh_layer_id =O0OOO0O0O0O0O0OO0 #line:619
	@property #line:621
	def raw_data (O0OO0O0O0OOO0O000 ):#line:622
		if not O0OO0O0O0OOO0O000 ._raw_data :#line:623
			O0OO0O0O0OOO0O000 ._raw_data =O0OO0O0O0OOO0O000 .remove_emulation_prevention_three_byte ()#line:624
		return O0OO0O0O0OOO0O000 ._raw_data #line:625
	def remove_emulation_prevention_three_byte (O0O0O0O0O0O0O00OO ):#line:627
		O0O000OOO00O00O00 =int (len (O0O0O0O0O0O0O00OO ._data )/8 )#line:628
		OOOOOO0OO0OO00O00 =BitStream ()#line:629
		O0O0O0O0OOO000OO0 =0 #line:631
		while O0O0O0O0OOO000OO0 <O0O000OOO00O00O00 :#line:632
			if (O0O0O0O0OOO000OO0 +2 )<O0O000OOO00O00O00 and O0O0O0O0O0O0O00OO ._data .peek ('bits:24')=="0x000003":#line:633
				OOOOOO0OO0OO00O00 .append (O0O0O0O0O0O0O00OO ._data .read ('bits:8'))#line:634
				OOOOOO0OO0OO00O00 .append (O0O0O0O0O0O0O00OO ._data .read ('bits:8'))#line:635
				OO00OOOOOOO000OO0 =O0O0O0O0O0O0O00OO ._data .read ('bits:8')#line:636
				O0O0O0O0OOO000OO0 +=3 #line:637
			else :#line:638
				OOOOOO0OO0OO00O00 .append (O0O0O0O0O0O0O00OO ._data .read ('bits:8'))#line:639
				O0O0O0O0OOO000OO0 +=1 #line:640
		return OOOOOO0OO0OO00O00 #line:641
def progress (OO00O00O0OOOO000O ,string =None ):#line:644
	O00OOO0OOOO0OOOOO =list ()#line:645
	for OO00O0OOOO0O0O00O in OO00O00O0OOOO000O :#line:646
		_OO000OO0OOOOOOOO0 =OO00O0OOOO0O0O00O [0 ]#line:647
		O00OO0O000O0O0000 =OO00O0OOOO0O0O00O [1 ]#line:648
		OO0OO00000OO00O0O =OO00O0OOOO0O0O00O [2 ]#line:649
		O00O000O0O0O0OOOO =round (100.0 *O00OO0O000O0O0000 /float (OO0OO00000OO00O0O ),1 )#line:650
		O00OOO0OOOO0OOOOO .append ("{}: {}".format (_OO000OO0OOOOOOOO0 ,(str (O00O000O0O0O0OOOO )+"%").ljust (8 ," ")))#line:651
	if string :#line:652
		O00OOO0OOOO0OOOOO .append ("({})".format (string ))#line:653
	sys .stdout .write ("{}\r".format ("".join (O00OOO0OOOO0OOOOO )))#line:654
	sys .stdout .flush ()#line:655
	return True #line:656
def format_seconds_to_hhmmss (O0O00O00O0O00O0O0 ):#line:659
	O000OOOOOO00OOOO0 =O0O00O00O0O00O0O0 //(60 *60 )#line:660
	O0O00O00O0O00O0O0 %=(60 *60 )#line:661
	OOOOO00OOOO00O0OO =O0O00O00O0O00O0O0 //60 #line:662
	O0O00O00O0O00O0O0 %=60 #line:663
	if O000OOOOOO00OOOO0 !=0 :#line:664
		OOO0OO0OO0O00O00O ="{:02d}h {:02d}m {:02d}s".format (int (O000OOOOOO00OOOO0 ),int (OOOOO00OOOO00O0OO ),int (O0O00O00O0O00O0O0 ))#line:669
	else :#line:670
		OOO0OO0OO0O00O00O ="{:02d}m {:02d}s".format (int (OOOOO00OOOO00O0OO ),int (O0O00O00O0O00O0O0 ))#line:674
	return OOO0OO0OO0O00O00O #line:675
def mux_exp (OOO0O0O0O00O00OO0 ,OOOOO0OO00000000O ,fel_to_mel =False ,skip_hdr10plus =False ,lbf_exp =500 ,mode_exp =1 ):#line:678
	O0OOO0O0O00OO0OO0 =list ()#line:680
	OOOOO0O00O0O000OO =Reader_Experimental (OOO0O0O0O00O00OO0 ,"bl",skip_hdr10plus )#line:682
	OOOOO0O00O0O000OO .start ()#line:683
	O0OOO0O0O00OO0OO0 .append (OOOOO0O00O0O000OO )#line:684
	OO0O00O0O0OO000O0 =Reader_Experimental (OOO0O0O0O00O00OO0 ,"el",False )#line:686
	OO0O00O0O0OO000O0 .start ()#line:687
	O0OOO0O0O00OO0OO0 .append (OO0O00O0O0OO000O0 )#line:688
	O0000O0OO00OOO000 =Writer_Experimental (OOOOO0OO00000000O ,[OOOOO0O00O0O000OO .output_queue ,OO0O00O0O0OO000O0 .output_queue ,],mode_exp ,fel_to_mel )#line:698
	O0000O0OO00OOO000 .start ()#line:699
	O0OOO0O0O00OO0OO0 .append (O0000O0OO00OOO000 )#line:700
	O0OOO0OO0O0O00OO0 =dict (bl =0 ,el =0 ,dts_bl =0 ,dts_el =0 )#line:702
	O0O0OOO00O00O0000 =OOOOO0O00O0O000OO .get_file_duration ()#line:703
	while O0000O0OO00OOO000 .active .is_set ()or not O0000O0OO00OOO000 .output_queue .empty ():#line:705
		for O0OO0O0O000OOOOO0 in [OOOOO0O00O0O000OO ,OO0O00O0O0OO000O0 ]:#line:706
			if O0OO0O0O000OOOOO0 .output_queue .qsize ()>lbf_exp :#line:707
				O0OO0O0O000OOOOO0 .event .clear ()if O0OO0O0O000OOOOO0 .event .is_set ()else None #line:708
			else :#line:709
				if O0OO0O0O000OOOOO0 .output_queue .qsize ()<(lbf_exp /10 ):#line:710
					O0OO0O0O000OOOOO0 .event .set ()if not O0OO0O0O000OOOOO0 .event .is_set ()else None #line:711
		time .sleep (0.5 )#line:713
		while not O0000O0OO00OOO000 .output_queue .empty ():#line:715
			O0OOO0OO0O0O00OO0 =O0000O0OO00OOO000 .output_queue .get ()#line:716
		O0000OO0OOOO00O0O =O0OOO0OO0O0O00OO0 ["bl"]+O0OOO0OO0O0O00OO0 ["el"]#line:717
		if O0000OO0OOOO00O0O >0 :#line:718
			progress ([["BL_ANALYSIS",O0OOO0OO0O0O00OO0 ["dts_bl"],O0O0OOO00O00O0000 ],["EL_ANALYSIS",O0OOO0OO0O0O00OO0 ["dts_el"],O0O0OOO00O00O0000 ]],"BL_EL_RPU WRITING: {}".format (format_size (O0000OO0OOOO00O0O )))#line:725
	O0000O0OO00OOO000 .join ()#line:727
	graceful_shutdown (O0OOO0O0O00OO0OO0 )#line:728
