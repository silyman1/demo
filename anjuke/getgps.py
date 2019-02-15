# -*- coding: utf-8 -*-
import requests

def geocodeG(address):
    par = {'address': address, 'key': '44004bce62f708e61df776b076bb1b92'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, par)
    answer = response.json()
    print answer
    GPS=answer['geocodes'][0]['location'].split(",")
    return GPS[0],GPS[1]
if __name__ == '__main__':
	addr = '亭林山庄'
	y,x = geocodeG(addr)
	print y,x