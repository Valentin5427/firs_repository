'''
from serial import Serial
print 123

port = Serial()
port.port = 'COM3'
port.baudrate = 9600
port.bytesize = 8
port.parity = 'N'
port.stopbits = 1
port.timeout = 0.1
port.close()
port.open()
'''

def tran(a):
    if len(a) < 3:
        return a
    seqs = []
    seq  = []
    for i in range(len(a)):
        if seq == []:
            seq += a[i]
        else:
            try:
                if int(a[i]) == int(a[i-1]) + 1:
                    seq += a[i]
                else:    
                    seqs += [seq]
                    seq = [a[i]]
            except:
                seqs += [seq]
                seq = [a[i]]
                                       
    seqs += [seq]
    print 'seqs=', seqs
    rez = []
    for i in range(len(seqs)):
 #       print 'len(seqs[i])=', len(seqs[i])
        if len(seqs[i]) < 3:
            rez += seqs[i]
        else:
            print seqs[i][0] + '-' + seqs[i][len(seqs[i]) - 1]
            rez += [seqs[i][0] + '-' + seqs[i][len(seqs[i]) - 1]]    
#            rez += ['ASDFG']    
#            rez = rez + ['ASDFG']    
 #       print 'rez=', rez
    
#    return seqs
    return rez
    
    
    
    
    
a = ['1', '2', '3', '5', '3', '4', '6', 'q']
b = ['1', '2']
c = ['MMM']

r = tran(a)
print r
r = tran(b)
print r
r = tran(c)
print r


