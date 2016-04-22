# Shot_Detector 2
import mraa 
import time
import socket   #for sockets
import sys  #for exit

INTERVAL = .100                   # Sound Signature Sample time
BYSEC_INTERVAL =1
SENDMSG_INTERVAL =60           # Minimum time between sending something to cloud

#LED_GPIO = 5                   # The LED pin
TRIGGER_GPIO = 6               # The TRIGGER GPIO
#led = mraa.Gpio(LED_GPIO)      # Get the LED pin object
#led.dir(mraa.DIR_OUT)          # Set the direction as output
trig = mraa.Gpio(TRIGGER_GPIO)   # Get the TRIGGER pin object
trig.dir(mraa.DIR_IN)           # Set the direction as input

#ledState = False               # LED is off to begin with
#led.write(0)


def getTriggerf():
    """ This function operates for minimal send interval of trigger event """
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
    toggleCt=1  # Had 1st toggle approaching function
                
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
    msg = '{"n": "Shot", "v": 1.0}'
    msg1 = '{"n": "Shot", "v": .2}'
    nullmsg = '{"n": "Shot", "v": 0.0}'
    shot=0
    disturb=0
    shotCt=0
    shotnullmsg = '{"n": "shots", "v": 0}'
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

        t = time.time()

        if t > next_sample_time:
            try :
            	shotmsg = ''.join(('{"n": "shots", "v": ', str(shotCt),'}'))
                #Set the whole string
                s.sendto(shotmsg, (host, port))
                print 'Shot Ct Message Sent', shotCt
                shotCt = 0
                next_sample_time = t + SENDMSG_INTERVAL

            except socket.error, msg:
                print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
                sys.exit()

        else:
            print 'going into get trigger'
            
	# wait until trigger or timed out
            lowtrig = getTriggerf()
 
            if lowtrig != 0:
                 
                try:
                    #Set the whole string
                    s.sendto(nullmsg, (host, port))
                    print 'No trigger events, nullmsg sent'

                except socket.error, msg:
                    print 'Error Code : ' + str(nullmsg[0]) + ' Message ' + nullmsg[1]
                    sys.exit() 

            else:
            	# Trigger event occured
                tuno = time.time()
                secsample_time = tuno + BYSEC_INTERVAL
                loopCt=0
       
                while 1:
                    tuno = time.time()
                    loopCt +=1
                    shotdata =getSignature ()
                    #print 'Signature Detected'
                    print shotdata

                    if shotdata[1] > 0 < 25 and shotdata[2] > 1 < 50 :
                        shot += 1
                        print shot
                    else:
                        disturb += 0.2
                        print disturb

                    if tuno > secsample_time:
                        try :
                            if shot > 4:
                                shot = 0.2
                                shotCt =0	
                            #Set the whole string
                            shotpersecmsg = ''.join(('{"n": "Shot", "v": ', str(shot),'}'))
                            s.sendto(shotpersecmsg, (host, port))
                            shotCt = shot
                            shot = 0
                            print 'Threshold reached ', shotCt
                    
                        except socket.error, msg:
                            print 'Error Code : ' + str(shotpersecmsg[0]) + ' Message ' + shotpersecmsg[1]
                            sys.exit()

                  
                        try :
                            disturb= float(disturb) / (loopCt)
                            shotpersecmsg1 = ''.join(('{"n": "Shot", "v": ', str(disturb),'}'))
                            #Set the whole string
                            s.sendto(shotpersecmsg1, (host, port))
                            disturb=0
                    
                        except socket.error, msg:
                            print 'Error Code : ' + str(shotpersecmsg1[0]) + ' Message ' + shotpersecmsg1[1]
                            sys.exit() 
                        break

            print 'onto main while loop'                
            continue    
                
        # Button click, detected, now toggle the LED
#        if ledState == True:
#            led.write(1)
#            ledState = False
#        else:
#            led.write(0)
#            ledState = True

#    time.sleep(0.005)





