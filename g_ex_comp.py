#!/usr/bin/env python3
import argparse
import os.path
import re
import sys
import time

control_sign_list = ['|', '[', ']', '{', '}']

def main():
	parser = argparse.ArgumentParser(prog = 'g_ex_comp', description = 'Experimental (de)compression, not intended for production use!')
	parser.add_argument('-c', '--compress', help='file to compress')
	parser.add_argument('-d', '--decompress', help='file to decompress')
	parser.add_argument('-n', '--normal', action='store_true', help='normal compression based on string sections')
	parser.add_argument('-f', '--fast', action='store_true', help='fast compression based on full word phrases')
	parser.add_argument('-ff', '--veryfast', action='store_true', help='very fast compression based on full words only')
	parser.add_argument('-o', '--output', help='output file')
	parser.add_argument('-q', '--quiet', action='store_true', help='no information in stdout except for error messages')
	args = parser.parse_args()
	if (args.compress is None and args.decompress is None) or (args.compress is not None and args.decompress is not None):
		print('Faulty input. Terminating.')
		sys.exit(0)
	if args.compress is not None:
		compress(args)
	elif args.decompress is not None:
		decompress(args)

def compress(args):
	if not os.path.isfile(args.compress):
		print('Source does not exist. Terminating.')
	with open(args.compress, 'r') as stream:
		raw = stream.read()
	control_sign = False
	for i in control_sign_list:
		if i not in raw:
			control_sign = i
			break
	if not control_sign:
		print('Could not determine markers. Terminating.')
		sys.exit(0)
	if not args.quiet:
		size_orig = len(raw)
		print(f'compressing {size_orig} ...')
		comp_start = time.time()
	if args.fast:
		out_full = f_compress(raw,control_sign)
	elif args.veryfast:
		out_full = ff_compress(raw,control_sign)
	elif args.normal:
		out_full = n_compress(raw, control_sign)
	with open(args.output, 'w+') as stream:
		stream.write(out_full)
	if not args.quiet:
		comp_end = time.time()
		size_final = len(out_full)
		size_percent = int(100 / size_orig * size_final)
		elapsed_time = round(comp_end - comp_start, 2)
		print(f'compressed to {size_final}')
		print(f'Down to {size_percent}% in {elapsed_time}s')

def _util_findstrmatches(sub, s):
	counter = 0
	i = 0
	while True:
		i = s.find(sub, i)
		if i == -1:
			break
		counter += 1
		i += len(sub)
	return counter

def _util_mapcheck(s, mapkeys):
	for i in mapkeys:
		if s in i:
			return True
	return False

def n_compress(raw, control_sign):
	compress_map = {}
	min_length = 4
	max_length = int(len(raw) / 3)
	i = 0
	while i < (len(raw) - min_length * 2):
		j = i + min_length
		tmp_result = ''
		tmp_maxgain = 0
		tmp_maxcount = 0
		while j < (len(raw) - min_length):
			j += 1
			tmp = raw[i:j]
			tmp_gain = len(tmp) - 3
			tmp_count = _util_findstrmatches(tmp, raw)
			if tmp_count < 2 or tmp_maxgain > (tmp_gain * tmp_count) - (len(tmp) + 3):
				break
			elif tmp in compress_map:
				continue
			tmp_result = tmp
			tmp_maxgain = (tmp_gain * tmp_count) - (len(tmp) + 3)
			tmp_maxcount = tmp_count
		if not _util_mapcheck(tmp_result, compress_map.keys()):
			compress_map[tmp_result] = {'gain': len(tmp_result) - 3, 'count': tmp_maxcount, 'truegain': tmp_maxgain}
		i += 1
	out_map = control_sign
	out_compressed = raw
	map_id = 1
	for i in compress_map:
		if compress_map[i]['truegain'] <= 1 or compress_map[i]['count'] > _util_findstrmatches(i, out_compressed):
			continue
		out_compressed = out_compressed.replace(i, f'{control_sign}{map_id}{control_sign}')
		out_map += f'{control_sign}{map_id}{control_sign}{i}'
		map_id += 1
	out_map += control_sign + control_sign
	return out_map + out_compressed

def f_compress(raw, control_sign):
	compress_map = {}
	word_map = re.split(r'\W+', raw)
	i = 0
	while i < len(word_map): # TODO: this might leave an empty last var
		if len(word_map[i].strip()) < 1:
			del word_map[i]
		else:
			i += 1
	for i in range(0, len(word_map)):
		tmp = word_map[i]
		counter = 1
		tmp_map = {}
		while (i + counter) < len(word_map):
			tmp += f' {word_map[i + counter]}'
			tmp_gain = len(tmp) - 3
			if tmp_gain > 0:
				tmp_count = sum(1 for _ in (re.finditer(tmp, raw)))
				if tmp_count < 2:
					break
				tmp_map[tmp] = {'gain': tmp_gain, 'count': tmp_count, 'truegain': (tmp_gain * tmp_count) - (len(tmp) + 3)}
			counter += 1
		if len(tmp_map) == 0:
			continue
		tmp_map = dict(sorted(tmp_map.items(), key=lambda item: item[1]['truegain'], reverse=True))
		tmp_result = next(iter(tmp_map.keys()))
		compress_map[tmp_result] = tmp_map[tmp_result]
	out_map = control_sign
	out_compressed = raw
	map_id = 1
	for i in compress_map:
		if compress_map[i]['truegain'] <= 1 or compress_map[i]['count'] > sum(1 for _ in (re.finditer(i, out_compressed))):
			continue
		out_compressed = out_compressed.replace(i, f'{control_sign}{map_id}{control_sign}')
		out_map += f'{control_sign}{map_id}{control_sign}{i}'
		map_id += 1
	out_map += control_sign + control_sign
	return out_map + out_compressed

def ff_compress(raw, control_sign):
	compress_map = {}
	for i in re.split(r'\W+', raw):
		if len(i) < 4:
			continue
		if i in compress_map:
			compress_map[i]['count'] += 1
		else:
			compress_map[i] = {'name': i, 'count' : 1, 'gain': len(i) - 3}
	for i in compress_map:
		compress_map[i]['truegain'] = (compress_map[i]['count'] * compress_map[i]['gain']) - (len(i) + 3)
	compress_map = dict(sorted(compress_map.items(), key=lambda item: item[1]['truegain'], reverse=True))
	map_index = 1
	for i in compress_map:
		compress_map[i]['gain'] = len(i) - (2 + len(str(map_index)))
		compress_map[i]['truegain'] = (compress_map[i]['count'] * compress_map[i]['gain']) - (len(i) + (2 + len(str(map_index))))
		map_index += 1
	compress_map = dict(sorted(compress_map.items(), key=lambda item: item[1]['truegain'], reverse=True))
	out_map = control_sign
	out_compressed = raw
	map_id = 1
	for i in compress_map:
		if compress_map[i]['truegain'] <= 1:
			continue
		out_compressed = out_compressed.replace(i, f'{control_sign}{map_id}{control_sign}')
		out_map += f'{control_sign}{map_id}{control_sign}{i}'
		map_id += 1
	out_map += control_sign + control_sign
	return out_map + out_compressed

def decompress(args):
	if not os.path.isfile(args.decompress):
		print('Source does not exist. Terminating.')
	with open(args.decompress, 'r') as stream:
		raw = stream.read()
	if raw[0] != raw[1] or raw[0] not in control_sign_list:
		print('Source seemingly not compressed. Terminating.')
	control_sign = raw[0]
	split_index = raw.find(control_sign + control_sign, 2)
	compress_map = raw[0:split_index + 1]
	decompressed = raw[split_index + 2:]
	re_string = f'\\{control_sign}\\d+\\{control_sign}[^\\{control_sign}]+'
	compress_items = re.findall(re_string, compress_map)
	for i in compress_items:
		med_pos = i.find(control_sign, 1)
		decomp_search = i[:med_pos + 1]
		decomp_orig = i[med_pos + 1:]
		decompressed = decompressed.replace(decomp_search, decomp_orig)
	with open(args.output, 'w+') as stream:
		stream.write(decompressed)

if __name__ == '__main__':
	main()