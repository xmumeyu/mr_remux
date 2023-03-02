# -*- coding: utf-8 -*-

from argparse import RawTextHelpFormatter
from bitstring import BitStream
from ctypes import *
import argparse
import time
import sys
import os

# EXP
import multiprocessing as mp
import subprocess as sp
import psutil
import re
from plugins.remux.setting import Setting


# ######################################################################
# 原作者信息，基于以下版本改造
# # Author: 	yusesope
# # Version: 	0.0.4_beta
# # Info: 		https://www.makemkv.com/forum/viewtopic.php?f=12&t=18602
# ######################################################################


# ################################ EXP #################################

class FFmpeg:
	def __init__(self, input_file):
		super(FFmpeg, self).__init__()
		self.input_file = input_file
		self.FFMPEG_BIN = Setting.ffmpegbin
		self.info = self.get_info()
		self.is_running = False
		self.process = None

	def open_pipe(self, dv_layer, bufsize):
		layer_idx = {
			"bl": 0,
			"el": 1
		}
		command = [
			self.FFMPEG_BIN,
			'-hide_banner',
			'-loglevel', 'panic',
			'-i', self.input_file,
			'-map', '0:{}'.format(
				layer_idx.get(
					dv_layer
				)
			),
			'-c', 'copy',
			'-f', 'hevc',
			'-'
		]
		pipe = sp.Popen(
			command,
			stdout=sp.PIPE,
			bufsize=bufsize
		)
		self.is_running = True
		self.process = psutil.Process(pipe.pid)
		return pipe

	def kill(self, proc_pid):
		# process = psutil.Process(proc_pid)
		for proc in self.process.children(recursive=True):
			proc.kill()
		self.process.kill()
		self.is_running = False

	@staticmethod
	def get_sec(time_str):
		hh_mm_ss, mil = time_str.split(".")
		h, m, s = hh_mm_ss.split(":")
		return int(h) * 3600 + int(m) * 60 + int(s) + (float(mil) / 100)

	def get_info(self):
		pattern_vui = re.compile(r"(vui_num_units_in_tick|vui_time_scale).*?=\s?(\d+)")
		pattern_dur = re.compile(r"duration:\s?(\d{2}:\d{2}:\d{2}\.\d{2})", re.I)
		pattern_vid = re.compile(r"stream\s?#0:\d[\[\]0-9x]+:\s?video:", re.I)
		sps = False
		vui_timing_info = dict(
			duration=0,
			vui_num_units_in_tick=0,
			vui_time_scale=0,
		)
		n_video_stream = 0
		command = [
			self.FFMPEG_BIN,
			'-hide_banner',
			'-i', self.input_file,
			'-c', 'copy',
			'-bsf:v', 'trace_headers',
			'-f', 'null',
			'-'
		]
		proc = sp.Popen(
			command,
			stdout=sp.PIPE,
			stderr=sp.STDOUT,
			universal_newlines=True
		)
		self.is_running = True
		self.process = psutil.Process(proc.pid)
		counter = 0
		for line in proc.stdout:
			if not n_video_stream >= 2:
				search_vid = re.search(pattern_vid, line)
				if search_vid:
					n_video_stream += 1
			if not vui_timing_info["duration"]:
				search_dur = re.search(pattern_dur, line)
				if search_dur:
					vui_timing_info["duration"] = self.get_sec(search_dur.group(1))
			elif not sps and "Sequence Parameter Set" in line:
				sps = True
			elif sps:
				search_vui = re.search(pattern_vui, line)
				if search_vui:
					vui_timing_info[search_vui.group(1)] = float(search_vui.group(2))

			counter += 1
			if len(list(filter(None, [v != 0 for v in vui_timing_info.values()]))) == len(vui_timing_info) or counter > 2000 or not line:
				self.kill(proc.pid)
				break
		return dict(n_video_stream=n_video_stream, vui_timing_info=vui_timing_info)


class Reader_Experimental(mp.Process):
	def __init__(
		self,
		file,
		dv_layer,
		skip_hdr10plus_flag
	):
		super(Reader_Experimental, self).__init__()
		self.file = file
		self.dv_layer = dv_layer
		self.ffmpeg = FFmpeg(self.file)
		self.skip_hdr10plus_flag = skip_hdr10plus_flag
		self.output_queue = mp.Queue()
		self.event = mp.Event()
		self.event.set()
		self.active = mp.Event()
		self.active.set()
		self.pipe = None
		self.chunk_size = 1024 * 1024 * 1
		self.global_offset = 0
		self.buffer = []
		self.starting_nalus = [
			NalUnitType.NAL_UNIT_ACCESS_UNIT_DELIMITER,
			NalUnitType.NAL_UNIT_VPS,
			NalUnitType.NAL_UNIT_SPS,
			NalUnitType.NAL_UNIT_PPS,
			NalUnitType.NAL_UNIT_PREFIX_SEI
		]
		self.slice_nalu = [
			NalUnitType.NAL_UNIT_CODED_SLICE_TRAIL_N,
			NalUnitType.NAL_UNIT_CODED_SLICE_TRAIL_R,
			NalUnitType.NAL_UNIT_CODED_SLICE_TSA_N,
			NalUnitType.NAL_UNIT_CODED_SLICE_TSA_R,
			NalUnitType.NAL_UNIT_CODED_SLICE_STSA_N,
			NalUnitType.NAL_UNIT_CODED_SLICE_STSA_R,
			NalUnitType.NAL_UNIT_CODED_SLICE_RADL_N,
			NalUnitType.NAL_UNIT_CODED_SLICE_RADL_R,
			NalUnitType.NAL_UNIT_CODED_SLICE_RASL_N,
			NalUnitType.NAL_UNIT_CODED_SLICE_RASL_R,
			NalUnitType.NAL_UNIT_CODED_SLICE_BLA_W_LP,
			NalUnitType.NAL_UNIT_CODED_SLICE_BLA_W_RADL,
			NalUnitType.NAL_UNIT_CODED_SLICE_BLA_N_LP,
			NalUnitType.NAL_UNIT_CODED_SLICE_IDR_W_RADL,
			NalUnitType.NAL_UNIT_CODED_SLICE_IDR_N_LP,
			NalUnitType.NAL_UNIT_CODED_SLICE_CRA
		]
		self.dts_set = False
		self.latest_dts = 0
		self.tc = self.set_tc()

	def get_file_duration(self):
		return self.ffmpeg.info.get("vui_timing_info").get("duration")

	def set_tc(self):
		vui_timing_info = self.ffmpeg.info.get("vui_timing_info")
		if vui_timing_info["vui_num_units_in_tick"] and vui_timing_info["vui_time_scale"]:
			tc = vui_timing_info["vui_num_units_in_tick"] / vui_timing_info["vui_time_scale"]
		else:
			tc = -1
		return tc

	def reset_buffer(self, nalu=None):
		self.buffer = []
		self.dts_set = False
		if nalu:
			self.buffer.append(nalu)

	def add_nalu_to_au(self, nalu):
		if nalu.type in self.starting_nalus:
			if self.buffer and self.buffer[-1].type not in self.starting_nalus:
				self.output_queue.put(self.buffer)
				self.reset_buffer()
		elif nalu.type in self.slice_nalu:
			if (self.tc > 0) and not self.dts_set:
				nalu.dts = self.latest_dts + self.tc
				self.latest_dts = nalu.dts
				self.dts_set = True
		self.buffer.append(nalu)

	@staticmethod
	def get_dummy_data():
		dummy_data = "00000001460110"
		return BitStream("0x{0}{0}".format(dummy_data)).bytes

	@staticmethod
	def get_list_offsets(stream):
		list_offsets = list(stream.findall('0x000001', bytealigned=True))
		return list_offsets

	def parse_nalus(self, list_offsets, stream):
		for index in range(0, (len(list_offsets) - 1)):
			nalu = NalUnit()
			nalu.dv_layer = self.dv_layer
			nalu.offset = list_offsets[index]
			nalu.global_offset = self.global_offset + nalu.offset
			nalu.type = stream[(nalu.offset + 25):(nalu.offset + 31)].uint
			nalu.size = list_offsets[index + 1] - nalu.offset
			if stream[(nalu.offset + nalu.size - 8):(nalu.offset + nalu.size + 24)] == "0x00000001":
				nalu.size -= 8
			nalu.data = stream[(nalu.offset + 24):(nalu.offset + nalu.size)]
			if self.skip_hdr10plus_flag\
				and self.dv_layer != "el"\
				and nalu.type == NalUnitType.NAL_UNIT_PREFIX_SEI:
				# Matches ITU-T T.35 SMPTE ST 2094-40
				if nalu.data[:24] == "0x4E0104":
					continue
			self.add_nalu_to_au(nalu)
		return True

	def read(self,stream):
		list_offsets = self.get_list_offsets(stream)
		self.parse_nalus(list_offsets,stream)
		latest_valid_offset = list_offsets.pop(-1)
		return latest_valid_offset

	def chunks(self):
		while True:
			data = self.pipe.stdout.read(self.chunk_size)
			if not data:
				data = self.get_dummy_data()
				self.active.clear()
			yield data
			if not self.active.is_set():
				break
			self.event.wait()

	def standby(self):
		self.event.clear()
		self.event.wait()

	def run(self):
		# print("{} -> READER {}\n ".format(os.getpid(), self.dv_layer))
		self.pipe = self.ffmpeg.open_pipe(self.dv_layer, self.chunk_size)
		unprocessed_data = BitStream("")

		while True:
			for data in self.chunks():
				stream = BitStream(bytes=data)
				stream.prepend(unprocessed_data)
				latest_valid_offset = self.read(stream)
				unprocessed_data = stream[latest_valid_offset:]
				self.global_offset += (len(stream) - len(unprocessed_data))
			if not self.active.is_set():
				self.output_queue.put("END")
				self.standby()


class Writer_Experimental(mp.Process):
	def __init__(
		self,
		out_file,
		list_readers_queue,
		mode,
		fel_to_mel_flag
	):
		super(Writer_Experimental, self).__init__()
		self.out_file = out_file
		self.out_file_handler = None
		self.list_readers_queue = list_readers_queue
		self.mode = mode
		self.fel_to_mel_flag = fel_to_mel_flag
		self.total_written_au = 0
		self.active = mp.Event()
		self.active.set()
		self.output_queue = mp.Queue()
		self.written_data = {"bl": 0, "el": 0, "dts_bl": 0, "dts_el": 0}
		self.cpp_lib = None
		self.buffer = BitStream("")
		self.MAX_BUFFER_SIZE = 10 * 1024 * 1024
		self.pipe = None

	@staticmethod
	def init_cpp_lib():
		lib_name = "linux_cpp_lib.so"

		cpp_lib_path = os.path.join(
			os.path.dirname(os.path.realpath(__file__)),
			lib_name
		)
		cpp_lib = cdll.LoadLibrary(cpp_lib_path)
		cpp_lib.generate_mel_rpu.argstype = [
			POINTER(c_ubyte),
			c_int,
			POINTER(c_int)
		]
		cpp_lib.generate_mel_rpu.restype = POINTER(c_ubyte)
		cpp_lib.generate_profile81_rpu.argstype = [
			POINTER(c_ubyte),
			c_int,
			POINTER(c_int)
		]
		cpp_lib.generate_profile81_rpu.restype = POINTER(c_ubyte)
		return cpp_lib

	def fel_to_mel(self, fel_rpu_nalu):
		mel_rpu_nalu = NalUnit()

		try:
			cpp_array_size = c_uint()
			cpp_array = self.cpp_lib.generate_mel_rpu(
				create_string_buffer(
					fel_rpu_nalu.data.bytes,
					int(fel_rpu_nalu.data.len / 8)
				),
				int(fel_rpu_nalu.data.len / 8),
				byref(cpp_array_size)
			)
			mel_rpu_nalu.data = BitStream(
				bytearray(
					cpp_array[:cpp_array_size.value]
				)
			)
			self.cpp_lib.free_rpu(cpp_array)
		except:
			pass

		return mel_rpu_nalu

	def uhd_bd_to_profile81(self, rpu_nalu):
		profile81_rpu_nalu = NalUnit()

		try:
			cpp_array_size = c_uint()
			cpp_array = self.cpp_lib.generate_profile81_rpu(
				create_string_buffer(
					rpu_nalu.data.bytes,
					int(rpu_nalu.data.len / 8)
				),
				int(rpu_nalu.data.len / 8),
				byref(cpp_array_size)
			)
			profile81_rpu_nalu.data = BitStream(
				bytearray(
					cpp_array[:cpp_array_size.value]
				)
			)
			self.cpp_lib.free_rpu(cpp_array)
		except:
			pass

		return profile81_rpu_nalu

	def update_written_data(self, nalu):
		if isinstance(nalu, NalUnit):
			self.written_data[nalu.dv_layer] = nalu.global_offset + nalu.size
			self.output_queue.put(self.written_data)

	def fill_buffer(self, access_unit):
		for nalu in access_unit:
			if isinstance(nalu, NalUnit) and nalu.data:
				if nalu.dv_layer == "bl":
					nalu.data.prepend("0x00000001")
					self.buffer.append(nalu.data)
				elif nalu.dv_layer == "el":
					if nalu.type == NalUnitType.NAL_UNIT_UNSPECIFIED_62:
						if self.fel_to_mel_flag:
							nalu = self.fel_to_mel(nalu)
						elif self.mode == 2:
							nalu = self.uhd_bd_to_profile81(nalu)
						nalu.data.prepend("0x00000001")
						self.buffer.append(nalu.data)
					else:
						if self.mode == 1:
							nalu.data.prepend("0x000000017e01")
							self.buffer.append(nalu.data)
				if nalu.dts:
					self.written_data["dts_{}".format(nalu.dv_layer)] = nalu.dts

	def write(self):
		if self.buffer.len != 0:
			try:
				self.buffer.tofile(self.out_file_handler)
				self.buffer.clear()
			except:
				self.active.clear()

	def run(self):
		# print("{} -> WRITER".format(os.getpid()))
		with open(self.out_file, 'wb') as out_f:
			try:
				self.out_file_handler = out_f
				if self.fel_to_mel_flag or self.mode == 2:
					self.cpp_lib = self.init_cpp_lib()

				switch = 0
				n_finished_readers = 0
				while True:
					access_unit = self.list_readers_queue[switch].get()

					if access_unit == "END":
						n_finished_readers += 1
						if len(self.list_readers_queue) == n_finished_readers:
							self.active.clear()
					else:
						self.fill_buffer(access_unit)
						self.update_written_data(access_unit[-1])

						self.total_written_au += 1

					switch ^= 1

					if self.buffer.len > self.MAX_BUFFER_SIZE or not self.active.is_set():
						self.write()

					if not self.active.is_set():
						break

			except KeyboardInterrupt:
				sys.stdout.close()
				self.active.clear()


def format_size(size):
	_bytes = size / 8
	if _bytes > 1024 * 1024 * 1024:
		out = "{:>7.2f} GB".format(round(_bytes / 1024 / 1024 / 1024, 2))
	elif _bytes > 1024 * 1024:
		out = "{:>7.2f} MB".format(round(_bytes / 1024 / 1024, 2))
	elif _bytes > 1024:
		out = "{:>7.2f} KB".format(round(_bytes / 1024, 2))
	else:
		out = "{:>7}  B".format(_bytes)
	return out


def graceful_shutdown(list_process):
	for idx in reversed(range(0, len(list_process))):
		while True:
			if not list_process[idx].active.is_set():
				break
		list_process[idx].terminate()
	list_process = list()

# ############################ END EXP #################################


class NalUnitType:
	NAL_UNIT_CODED_SLICE_TRAIL_N = 0
	NAL_UNIT_CODED_SLICE_TRAIL_R = 1

	NAL_UNIT_CODED_SLICE_TSA_N = 2
	NAL_UNIT_CODED_SLICE_TSA_R = 3

	NAL_UNIT_CODED_SLICE_STSA_N = 4
	NAL_UNIT_CODED_SLICE_STSA_R = 5

	NAL_UNIT_CODED_SLICE_RADL_N = 6
	NAL_UNIT_CODED_SLICE_RADL_R = 7

	NAL_UNIT_CODED_SLICE_RASL_N = 8
	NAL_UNIT_CODED_SLICE_RASL_R = 9

	NAL_UNIT_RESERVED_VCL_N10 = 10
	NAL_UNIT_RESERVED_VCL_R11 = 11
	NAL_UNIT_RESERVED_VCL_N12 = 12
	NAL_UNIT_RESERVED_VCL_R13 = 13
	NAL_UNIT_RESERVED_VCL_N14 = 14
	NAL_UNIT_RESERVED_VCL_R15 = 15

	NAL_UNIT_CODED_SLICE_BLA_W_LP = 16
	NAL_UNIT_CODED_SLICE_BLA_W_RADL = 17
	NAL_UNIT_CODED_SLICE_BLA_N_LP = 18
	NAL_UNIT_CODED_SLICE_IDR_W_RADL = 19
	NAL_UNIT_CODED_SLICE_IDR_N_LP = 20
	NAL_UNIT_CODED_SLICE_CRA = 21
	NAL_UNIT_RESERVED_IRAP_VCL22 = 22
	NAL_UNIT_RESERVED_IRAP_VCL23 = 23

	NAL_UNIT_RESERVED_VCL24 = 24
	NAL_UNIT_RESERVED_VCL25 = 25
	NAL_UNIT_RESERVED_VCL26 = 26
	NAL_UNIT_RESERVED_VCL27 = 27
	NAL_UNIT_RESERVED_VCL28 = 28
	NAL_UNIT_RESERVED_VCL29 = 29
	NAL_UNIT_RESERVED_VCL30 = 30
	NAL_UNIT_RESERVED_VCL31 = 31

	NAL_UNIT_VPS = 32
	NAL_UNIT_SPS = 33
	NAL_UNIT_PPS = 34
	NAL_UNIT_ACCESS_UNIT_DELIMITER = 35
	NAL_UNIT_EOS = 36
	NAL_UNIT_EOB = 37
	NAL_UNIT_FILLER_DATA = 38
	NAL_UNIT_PREFIX_SEI = 39
	NAL_UNIT_SUFFIX_SEI = 40

	NAL_UNIT_RESERVED_NVCL41 = 41
	NAL_UNIT_RESERVED_NVCL42 = 42
	NAL_UNIT_RESERVED_NVCL43 = 43
	NAL_UNIT_RESERVED_NVCL44 = 44
	NAL_UNIT_RESERVED_NVCL45 = 45
	NAL_UNIT_RESERVED_NVCL46 = 46
	NAL_UNIT_RESERVED_NVCL47 = 47
	NAL_UNIT_UNSPECIFIED_48 = 48
	NAL_UNIT_UNSPECIFIED_49 = 49
	NAL_UNIT_UNSPECIFIED_50 = 50
	NAL_UNIT_UNSPECIFIED_51 = 51
	NAL_UNIT_UNSPECIFIED_52 = 52
	NAL_UNIT_UNSPECIFIED_53 = 53
	NAL_UNIT_UNSPECIFIED_54 = 54
	NAL_UNIT_UNSPECIFIED_55 = 55
	NAL_UNIT_UNSPECIFIED_56 = 56
	NAL_UNIT_UNSPECIFIED_57 = 57
	NAL_UNIT_UNSPECIFIED_58 = 58
	NAL_UNIT_UNSPECIFIED_59 = 59
	NAL_UNIT_UNSPECIFIED_60 = 60
	NAL_UNIT_UNSPECIFIED_61 = 61
	NAL_UNIT_UNSPECIFIED_62 = 62
	NAL_UNIT_UNSPECIFIED_63 = 63
	NAL_UNIT_INVALID = 64


class NalUnit(object):
	def __init__(self):
		self._offset = 0
		self._global_offset = 0
		self._size = 0
		self._type = None
		self._data = 0
		self._dv_layer = None
		self._nuh_layer_id = 0
		self._payload = None
		self._raw_data = None
		self._dts = 0

	@property
	def dts(self):
		return self._dts

	@dts.setter
	def dts(self, val):
		self._dts = val

	@property
	def offset(self):
		return self._offset

	@offset.setter
	def offset(self, val):
		self._offset = val

	@property
	def global_offset(self):
		return self._global_offset

	@global_offset.setter
	def global_offset(self, val):
		self._global_offset = val

	@property
	def size(self):
		return self._size

	@size.setter
	def size(self, val):
		self._size = val

	@property
	def type(self):
		return self._type

	@type.setter
	def type(self, val):
		self._type = val

	@property
	def data(self):
		return self._data

	@data.setter
	def data(self, val):
		self._data = val

	@property
	def dv_layer(self):
		return self._dv_layer

	@dv_layer.setter
	def dv_layer(self, val):
		self._dv_layer = val

	@property
	def nuh_layer_id(self):
		return self.nuh_layer_id

	@nuh_layer_id.setter
	def nuh_layer_id(self, val):
		self._nuh_layer_id = val

	@property
	def raw_data(self):
		if not self._raw_data:
			self._raw_data = self.remove_emulation_prevention_three_byte()
		return self._raw_data

	def remove_emulation_prevention_three_byte(self):
		NumBytesInNaluData = int(len(self._data) / 8)
		rbsp_byte = BitStream()

		i = 0
		while i < NumBytesInNaluData:
			if (i + 2) < NumBytesInNaluData and self._data.peek('bits:24') == "0x000003":
				rbsp_byte.append(self._data.read('bits:8'))
				rbsp_byte.append(self._data.read('bits:8'))
				emulation_prevention_three_byte = self._data.read('bits:8')
				i += 3
			else:
				rbsp_byte.append(self._data.read('bits:8'))
				i += 1
		return rbsp_byte


def progress(list_state, string=None):
	display = list()
	for state in list_state:
		_type = state[0]
		current = state[1]
		total = state[2]
		percentage = round(100.0 * current / float(total), 1)
		display.append("{}: {}".format(_type, (str(percentage) + "%").ljust(8, " ")))
	if string:
		display.append("({})".format(string))
	sys.stdout.write("{}\r".format("".join(display)))
	sys.stdout.flush()
	return True


def format_seconds_to_hhmmss(seconds):
	hours = seconds // (60 * 60)
	seconds %= (60 * 60)
	minutes = seconds // 60
	seconds %= 60
	if hours != 0:
		formatted_string = "{:02d}h {:02d}m {:02d}s".format(
			int(hours),
			int(minutes),
			int(seconds)
		)
	else:
		formatted_string = "{:02d}m {:02d}s".format(
			int(minutes),
			int(seconds)
		)
	return formatted_string


def mux_exp(in_file, out_file, fel_to_mel=False, skip_hdr10plus=False, lbf_exp=500, mode_exp=1):

	list_process = list()

	bl_reader = Reader_Experimental(in_file, "bl", skip_hdr10plus)
	bl_reader.start()
	list_process.append(bl_reader)

	el_reader = Reader_Experimental(in_file, "el", False)
	el_reader.start()
	list_process.append(el_reader)

	writer = Writer_Experimental(
		out_file,
		[
			bl_reader.output_queue,
			el_reader.output_queue,
		],
		mode_exp,
		fel_to_mel
	)
	writer.start()
	list_process.append(writer)

	written_data = dict(bl=0, el=0, dts_bl=0, dts_el=0)
	file_duration = bl_reader.get_file_duration()

	while writer.active.is_set() or not writer.output_queue.empty():
		for reader in [bl_reader, el_reader]:
			if reader.output_queue.qsize() > lbf_exp:
				reader.event.clear() if reader.event.is_set() else None
			else:
				if reader.output_queue.qsize() < (lbf_exp / 10):
					reader.event.set() if not reader.event.is_set() else None

		time.sleep(0.5)

		while not writer.output_queue.empty():
			written_data = writer.output_queue.get()
		written_total_data = written_data["bl"] + written_data["el"]
		if written_total_data > 0:
			progress(
				[
					["BL_ANALYSIS", written_data["dts_bl"], file_duration],
					["EL_ANALYSIS", written_data["dts_el"], file_duration]
				],
				"BL_EL_RPU WRITING: {}".format(format_size(written_total_data))
			)

	writer.join()
	graceful_shutdown(list_process)

