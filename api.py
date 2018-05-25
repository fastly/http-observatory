#!/usr/bin/env python3
from flask import Flask, request, jsonify
from httpobs.scanner.local import scan
import json
import threading

app = Flask(__name__)

results = ''
status = ''
scanning = False

@app.route('/analyze', methods=['POST'])
def startScan():
    global scanning

    host = request.args.get('host','observatory.mozilla.org')
    http_port = request.args.get('http_port','80')
    https_port = request.args.get('https_port','443')
    path = request.args.get('path','/')
    verify = request.args.get('verify', True)
    
    cookies = {}
    headers = {}
    if request.json is not None:
    	if 'cookies' in request.json: cookies = request.json['cookies'] 
    	if 'headers' in request.json: headers = request.json['headers'] 
    
    if scanning:
    	return 'scanner busy'
    else:
    	scanning = True
    	
    settings = {'status':'scan started',
    		'host': host,
    		'http_port': http_port,
    		'https_port': https_port,
    		'path': path,
    		'verify': verify,
    		'cookies': cookies,
    		'headers': headers}
    print(settings)
    
    thr = threading.Thread(target=runScan, args=(host, http_port, https_port, path, verify, cookies, headers), kwargs={})
    thr.start()
    
    return jsonify(settings)

@app.route('/analyze', methods=['GET'])
def getResults():
	global scanning
	global results
	if scanning:
		return 'still scanning'
	return jsonify(results)

@app.route('/status', methods=['GET'])
def getStatus():
	global status
	return jsonify({'status':status})
    
def runScan(host, http_port, https_port, path, verify, cookies, headers):
	global scanning
	global results
	global status
	
	results = ''
	status = 'Running'

	results = scan(host,
         http_port=http_port,
         https_port=https_port,
         path=path,
         verify=verify,
         cookies=cookies,
         headers=headers)     
	
	print('scan finished')
	status = 'Done'	
	scanning = False

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=4500)