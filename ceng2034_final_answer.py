#!/usr/bin/python3


# REMZI BULUTLU - 160709013

import os
import requests
import uuid
import hashlib
import sys
import multiprocessing

def child():
	print('Child PID:', os.getpid())
	download_file("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg")
	download_file("http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg")
	download_file("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg")
	download_file("https://upload.wikimedia.org/wikipedia/tr/9/98/Mu%C4%9Fla_S%C4%B1tk%C4%B1_Ko%C3%A7man_%C3%9Cniversitesi_logo.png")
	os._exit(0)

def download_file(url, file_name=None):
	r = requests.get(url, allow_redirects=True)
	file = file_name if file_name else str(uuid.uuid4())
	open(file, 'wb').write(r.content)

def checksum(file_name, d1):		#controls duplicate files downloaded
	dups = {}
	afile = open(file_name, 'rb')
	hasher = hashlib.md5()
	buff = afile.read()
	while len(buff) > 0:
		hasher.update(buff)
		buff = afile.read()
	afile.close()
	file_hash = hasher.hexdigest()
	if file_hash in dups:
                dups[file_hash].append(file_name)
	else:
                dups[file_hash] = [file_name]
	joinDicts(d1, dups)

def joinDicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]

def printResults(dict1):
	results = list(filter(lambda x: len(x) > 1, dict1.values()))
	if len(results) > 0:
		print('Duplicates Found:')
		print('The following files are identical. The name could differ, but the content is identical')
		print('___________________')
		for result in results:
		    for subresult in result:
		        print('\t\t%s' % subresult)
		    print('___________________')
 
	else:
		print('No duplicate files found.')

if __name__ == "__main__":
	dups = {}
	newPid = os.fork()
	if newPid == 0:
		child()
	else:
		os.wait() 	# avoids Orphan Process situation (keeps the parent process waiting till the child process finishes)
		manager = multiprocessing.Manager()
		dups = manager.dict()
		processes = []
		for file_name in os.listdir("./"):
			p = multiprocessing.Process(target=checksum, args=(file_name, dups))
			processes.append(p)
			p.start()

		for process in processes:
			process.join()	
	printResults(dups)
