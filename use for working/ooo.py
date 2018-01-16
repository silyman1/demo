#*-*coding=utf-8

f = open('p3616b.txt','r')
lines = f.readlines()
h = []
for line in lines:
	if line.strip() != '':
		newline = '{"' + line.strip() + '"},\n'
		h.append(newline)
		print newline 
f.close()
fo = open('result.txt','w+')
fo.writelines(h)
fo.close()