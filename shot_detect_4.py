#shot_detect_4.py 05/28/16  Simplified
import mraa 
import time
import socket   #for sockets
import sys  #for exit

INTERVAL = .025                # Sound Signature Sample time
BYSEC_INTERVAL =1
SENDMSG_INTERVAL =300           # Minimum time between sending something to cloud

TRIGGER_GPIO = 6               # The TRIGGER GPIO

trig = mraa.Gpio(TRIGGER_GPIO)   # Get the TRIGGER pin object
trig.dir(mraa.DIR_IN)           # Set the direction as input

def getTriggerf():
    """ This function operates for minimal send interval or trigger event """
    t = time.time()
    next_sample_time = t + SENDMSG_INTERVAL
    
    while (1):
        t = time.time()
        if (trig.read() != 1):
            # Trigger detected
            return (0) 
        if t > next_sample_time:
            #print 'Timed Out, no trigger event'
            return (1)
        else:
            # No trigger detected
            continue

            
def getSignature():
    """ This function returns a list of high/low pulses and the number of toggles """                
    t = time.time() 
    next_sample_time = t + INTERVAL
    lowCt=0
    highCt=0
    prevstate=0
    toggleCt=0  
                
    while True:
        t = time.time()
        trigpin=trig.read()
        if (trigpin != prevstate):
            toggleCt += 1
            prevstate= trigpin

        if (trigpin == 1):     # valid high pulse
            highCt += 1
                  
        else:     # Valid low pulse         
            lowCt += 1
 
        if t > next_sample_time:
                shotdata=[]
                shotdata.append (highCt)
                shotdata.append (lowCt)
                shotdata.append (toggleCt)
                return shotdata
            
if __name__ == '__main__':
    host = '127.0.0.1'
    port = 41234

    nullmsg = '{"n": "Shot", "v": 0.0}'
    shot=0
    disturb=0
    shotCt=0
    shotnullmsg = '{"n": "shot5min", "v": 0}'
    disturbnullmsg = '{"n": "Disturb", "v": 0}'
    t = time.time()
    next_sample_time = t + SENDMSG_INTERVAL
    
    # initialize our socket...
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()

    while 1:

        # 1st checks for SendMsg Interval for number of shots
        print 'MAIN WHILE LOOP Restart'
        t = time.time()

        if t > next_sample_time:
            try :
            	shotmsg = ''.join(('{"n": "shot5min", "v": ', str(shotCt),'}'))
                #Set the whole string
                s.sendto(shotmsg, (host, port))
                print 'Shot Ct over 5min Message Sent', shotCt
                shotCt = 0
                next_sample_time = t + SENDMSG_INTERVAL

            except socket.error, shotmsg:
                print 'Error Code : ' + str(shotmsg[0]) + ' Message ' + shotmsg[1]
                sys.exit()

        else:
       
	    # wait until trigger or timed out
            lowtrig = getTriggerf()
 
            if lowtrig != 0:
            	
                # No trigger events nor disturbances 
                try:
                    #Set the whole string
                    s.sendto(nullmsg, (host, port))
                    print 'No trigger events, nullmsg sent'

                except socket.error, msg:
                    print 'Error Code : ' + str(nullmsg[0]) + ' Message ' + nullmsg[1]
                    sys.exit() 
                try:
                    #Set the whole string
                    s.sendto(disturbnullmsg, (host, port))
                    print 'No Disturbances, nullmsg sent'

                except socket.error, msg:
                    print 'Error Code : ' + str(disturbnullmsg[0]) + ' Message ' + disturbnullmsg[1]
                    sys.exit() 

            else:
            	# Trigger event occured
                tuno = time.time()
                secsample_time = tuno + BYSEC_INTERVAL
                loopCt=0
       
                while 1:
                    tuno = time.time()

                    shotdata =getSignature ()
                    # print shotdata

                    if shotdata[1] !=0 and shotdata[2] !=1:
		        # Check sound disturbance for possible shot fired
                        disturb += 1
                      
                        if float(shotdata[1]) / shotdata[2] < 0.5 or float(shotdata[1]) / shotdata[2] > 7.5:
                            disturb += 1
                            print 'disturb signature ', shotdata
                        else:
                            # looks like a shot
                            first_shotdata=list(shotdata)
                            shotdata =getSignature ()
                            print '1st and 2nd ', first_shotdata, shotdata
                            if shotdata[1] < 12 and shotdata[2] <4:           
                                shot += 1
                                disturb += 10
                                print 'shot', shot
                            else:    
                                disturb += 1
                                print 'echo'
                            
                    if tuno > secsample_time:
                        # Filter for long repeated noise, excessive	
                        if shot > 8: 
                            shot = 0
                            print 'overshoot/sec shot = 0'
                        try :
	
                            #Set the whole string
                            shotpersecmsg = ''.join(('{"n": "Shot", "v": ', str(shot),'}'))
                            s.sendto(shotpersecmsg, (host, port))
                            shotCt += shot
                            shot = 0
                            # print 'Shot Count per minute ', shotCt
                    
                        except socket.error, msg:
                            print 'Error Code : ' + str(shotpersecmsg[0]) + ' Message ' + shotpersecmsg[1]
                            sys.exit()

                  
                        try :
                            print 'Disturbance/sec ', disturb	

                            disturbpersecmsg = ''.join(('{"n": "Disturb", "v": ', str(disturb),'}'))
                            #Set the whole string
                            s.sendto(disturbpersecmsg, (host, port))
                            # print shotpersecmsg1
                            disturb=0
                    
                        except socket.error, msg:
                            print 'Error Code : ' + str(disturbpersecmsg[0]) + ' Message ' + disturbpersecmsg[1]
                            sys.exit() 
                        break

        continue                


