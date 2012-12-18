#!/bin/env python
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import sys, json
import sys, time, glob, os, numpy, datetime
import matplotlib.pyplot as plt


def parse_file(fn):
    l_json = []
    f = open(fn)
    for l in f:
        dl = l.split(" ");
        sdtime = dl[2];
        try:
            dt = time.strptime("14/09/12 %s000" % sdtime, '%d/%m/%y %H:%M:%S.%f');
        except:
            print "Could not parse date: \n%s\nwith:\n%s" % (l, repr(l.split(" ")))
            sys.exit()
        ms = int(sdtime.split(".")[1])
        t = int(time.mktime(dt))*1000+ms
        if "incomplete" in l:
            #print "Parsing", l, ":"
            #print l.split('{')
            data = json.loads('{' + l.split('{')[1])
            data["ts"] = t
            l_json.append(data)
    return l_json

def main():
    data_c1 = parse_file(sys.argv[1]+'_syslog-1_cli_json')
    data_c2 = parse_file(sys.argv[1]+'_syslog-2_cli_json')
    data_s1 = parse_file(sys.argv[1]+'_syslog-1_srv_json')
    data_s2 = parse_file(sys.argv[1]+'_syslog-2_srv_json')
    # now plot
    plot_data(sys.argv[1], data_c1, data_c2, data_s1, data_s2)

def plot_data(fn, data_c1, data_c2, data_s1,  data_s2):
    figurePlot = plt.figure(figsize=(23.5, 18.0))
    rowNum = 5

    DNAME='my_max_send_q'
    plotAX3 = plt.subplot(rowNum,1,1)
    plt.title(DNAME)
    plt.plot(zipj(data_s1, "ts"), zipj(data_s1, DNAME), "-", zipj(data_s2, "ts"), zipj(data_s2, DNAME), "-")
    
    DNAME='ACK_coming_speed'
    plotAX3 = plt.subplot(rowNum,1,2)
    plt.title(DNAME)
    plt.plot(zipj(data_s1, "ts"), zipj(data_s1, DNAME), "-", zipj(data_s2, "ts"), zipj(data_s2, DNAME), "-")#,
#             zipj(data_s1, "ts"), zipj(data_s1, 'my_rtt'), "-", zipj(data_s2, "ts"), zipj(data_s2, 'my_rtt'), "-")

    DNAME="buf_len"    
    plotAX1 = plt.subplot(rowNum,1,3)
    plt.title(DNAME)
    plt.plot(zipj(data_c1, "ts"), zipj(data_c1, DNAME), "-")
    
    DNAME='incomplete_seq_len'
    plotAX2 = plt.subplot(rowNum,1,4)
    plt.title(DNAME)
    plt.plot(zipj(data_c1, "ts"), zipj(data_c1, DNAME), "-")

    DNAME='my_rtt'
    plotAX5 = plt.subplot(rowNum,1,5)
    plt.title(DNAME)
    plt.plot(zipj(data_c1, "ts"), zipj(data_c1, DNAME), "-", zipj(data_c2, "ts"), zipj(data_c2, DNAME), "-")    
    
    figurePlot.savefig(fn+".png", dpi=100)
    
def zipj(l_json, name):
    d = []
    for j in l_json:
        d.append(j[name])
    return d

if __name__ == '__main__':
    main()
