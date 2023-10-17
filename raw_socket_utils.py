import socket
import threading
import time

import numpy as np

from global_def import *
from ctypes import cdll, c_double, c_int, POINTER, c_ubyte, byref, c_char_p

raw_socket_so = cdll.LoadLibrary('./ctypes_raw_socket_send.so')
raw_socket_so.socket_init.argtypes = []
raw_socket_so.socket_init.restype = c_int

raw_socket_so.send_raw_socket.argtypes = [POINTER(c_ubyte), c_int, c_int]
raw_socket_so.send_raw_socket.restype = c_int

def ctypes_raw_socket_init():
	ctypes_raw_socket = raw_socket_so.socket_init()
	log.debug("ctypes_raw_socket : %d", ctypes_raw_socket)

def ctypes_raw_socket_send(rgb_frame, frame_id):
	# ubuffer = (c_ubyte * len(rgb_frame)).from_buffer_copy(bytearray(rgb_frame))
	ubuffer = (c_ubyte * len(rgb_frame)).from_buffer_copy(np.ascontiguousarray(rgb_frame))

	raw_socket_so.send_raw_socket(ubuffer, len(rgb_frame), 0)

def send_raw_socket_packet(data, network_if=default_network_if, src=default_src, dst=default_dst, proto=default_proto):
	# ETH_P_ALL = 3
	# s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
	# s.bind((network_if, 0))
	raw_socket.sendall(dst + src + proto + data)
	#s.close()


def send_rgb_frame_with_raw_socket(rgb_frame, frame_id):
	# log.debug("len(rgb_frame) : %d", len(rgb_frame))
	if frame_id > 0xffff:
		# log.debug("frame_id out of 0xffff")
		return False
	i = 0
	frame_id_bytes = int(frame_id).to_bytes(2, 'big')
	# log.debug("frame_id : %d %s", frame_id, frame_id_bytes)
	sed_id = 0
	for i in range(0, len(rgb_frame), 1480):
		# log.debug("i : %d", i)
		frame_segment = rgb_frame[i:i+1480]
		seq_id_bytes = sed_id.to_bytes(2, 'big')
		data = frame_id_bytes + seq_id_bytes + frame_segment
		send_raw_socket_packet(data)
		sed_id += 1

	frame_segment = rgb_frame[i * 1480: len(rgb_frame) - 1]
	seq_id_bytes = sed_id.to_bytes(2, 'big')
	data = frame_id_bytes + seq_id_bytes + frame_segment
	send_raw_socket_packet(data)
	return True





