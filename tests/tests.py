import subprocess
import time
import unittest

class Test_g_ex_comp(unittest.TestCase):
	def test_f(self):
		subprocess.run(['python3', '../g_ex_comp.py', '-c', 'testfile_in', '-o', 'testfile_comp', '-f', '-q'])
		subprocess.run(['python3', '../g_ex_comp.py', '-d', 'testfile_comp', '-o', 'testfile_decomp'])
		check = subprocess.run(['diff', 'testfile_in', 'testfile_decomp'], capture_output=True, text=True)
		self.assertEqual(check.stdout, '')

	def test_ff(self):
		subprocess.run(['python3', '../g_ex_comp.py', '-c', 'testfile_in', '-o', 'testfile_comp', '-ff', '-q'])
		subprocess.run(['python3', '../g_ex_comp.py', '-d', 'testfile_comp', '-o', 'testfile_decomp'])
		check = subprocess.run(['diff', 'testfile_in', 'testfile_decomp'], capture_output=True, text=True)
		self.assertEqual(check.stdout, '')

def create_testfile():
	with open('wordlist', 'r') as stream:
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
		testcontent += wordlist[(seed + len(testcontent)) % 500]
		if (seed * i) % 10 < 2:
			testcontent += ', '
		elif (seed * i) % 10 == 2:
			testcontent += '. '
		else:
			testcontent += ' '
		i += 1
	with open('testfile_in', 'w+') as stream:
		stream.write(testcontent.strip())

if __name__ == '__main__':
	create_testfile()
	unittest.main()