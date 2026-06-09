import os
import subprocess
import sys
import time
import unittest

path_self = os.path.dirname(os.path.abspath(__file__))
path_parent = path_self[0:path_self.rfind('/')]
path_masterfile = os.path.join(path_parent, 'g_ex_comp.py')
path_testfile_in = os.path.join(path_self, 'testfile_in')
path_testfile_comp = os.path.join(path_self, 'testfile_comp')
path_testfile_decomp = os.path.join(path_self, 'testfile_decomp')

class Test_g_ex_comp(unittest.TestCase):
	def test_n(self):
		subprocess.run(['python3', path_masterfile, '-c', path_testfile_in, '-o', path_testfile_comp, '-n', '-q'])
		subprocess.run(['python3', path_masterfile, '-d', path_testfile_comp, '-o', path_testfile_decomp])
		check = subprocess.run(['diff', path_testfile_in, path_testfile_decomp], capture_output=True, text=True)
		self.assertEqual(check.stdout, '')

	def test_f(self):
		subprocess.run(['python3', path_masterfile, '-c', path_testfile_in, '-o', path_testfile_comp, '-f', '-q'])
		subprocess.run(['python3', path_masterfile, '-d', path_testfile_comp, '-o', path_testfile_decomp])
		check = subprocess.run(['diff', path_testfile_in, path_testfile_decomp], capture_output=True, text=True)
		self.assertEqual(check.stdout, '')

	def test_ff(self):
		subprocess.run(['python3', path_masterfile, '-c', path_testfile_in, '-o', path_testfile_comp, '-ff', '-q'])
		subprocess.run(['python3', path_masterfile, '-d', path_testfile_comp, '-o', path_testfile_decomp])
		check = subprocess.run(['diff', path_testfile_in, path_testfile_decomp], capture_output=True, text=True)
		self.assertEqual(check.stdout, '')

def create_testfile():
	print('Generating test file.')
	with open(os.path.join(path_self, 'wordlist'), 'r') as stream:
		wordlist = stream.read().split()
	seed = int(time.time())
	step = (seed % 25) + 10
	i = step
	while i <= len(wordlist):
		wordlist[i] = wordlist[i].title()
		i += step
	testcontent = ''
	maxwords = seed % 1000 + 25000
	i = 0
	while i < maxwords:
		tmp_word = wordlist[(seed + len(testcontent)) % 500]
		if(seed * i) % 7 == 0:
			tmp_word = tmp_word.capitalize()
		testcontent += tmp_word
		if (seed * i) % 15 < 2:
			testcontent += ', '
		elif (seed * i) % 15 == 2:
			testcontent += '. '
		elif (seed * i) % 15 == 3:
			testcontent += '? '
		elif (seed * i) % 15 == 4:
			testcontent += '! '
		else:
			testcontent += ' '
		if 2 < (seed * i) % 15 < 5 and (seed * i) % 3 == 0:
			testcontent += '\n'
			seed += 1
		i += 1
	with open(path_testfile_in, 'w+') as stream:
		stream.write(testcontent.strip())
	print('Done. Testing ...')

if __name__ == '__main__':
	create_testfile()
	unittest.main()