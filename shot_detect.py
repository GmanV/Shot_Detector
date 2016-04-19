# Shot_Detector
import mraa 
import time
import socket   #for sockets
import sys  #for exit

INTERVAL = .05                   # Sound Signature Sample time
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
            # No trigger detected
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
        if (trig.read() != prevstate):
            toggleCt += 1
            prevstate= trig.read()

        if (trig.read() == 1):     # valid high pulse
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
    msg = '{"n": "temp", "v": 1.0}'
    nullmsg = '{"n": "temp", "v": 0.0}'
    shotCt=0

#    shotmsg = ''.join(('{"n": "shots", "v": ', str(shotCt),'}'))
    shotnullmsg = '{"n": "shots", "v": 0}'

#    shotmsg = ('{"n": "shots", "v": ', shotCt, '}')
#    shotnullmsg = '{"n": "shots", "v": ', 0, '}'
#    t = time.time()
#    next_sample_time = t + SENDMSG_INTERVAL
    
    # initialize our socket...
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()

    while 1:

# 1st checks for SendMsg Interval for number of shots               

        t = time.time()
        next_sample_time = t + SENDMSG_INTERVAL
        if t > next_sample_time:
            try :
            	shotmsg = ''.join(('{"n": "shots", "v": ', str(shotCt),'}'))
                #Set the whole string
                s.sendto(shotmsg, (host, port))
                print 'Shot Message Sent', shotCt
                shotCt = 0

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
                    print 'Null Message Sent'

                except socket.error, msg:
                    print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
                    sys.exit() 
	


            else:    
                shotdata =getSignature ()
                #print 'Signature Detected'
                print shotdata

                if shotdata[1] > 5 < 100 and shotdata[2] > 5 < 50 :
                    try :
                        #Set the whole string
                        s.sendto(msg, (host, port))
                        shotCt += 1
                        print 'Threshold reached ', shotCt
                        print 'Message Sent ', shotCt
                    
                    except socket.error, msg:
                        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
                        sys.exit()
                continue

        # Button click, detected, now toggle the LED
#        if ledState == True:
#            led.write(1)
#            ledState = False
#        else:
#            led.write(0)
#            ledState = True

#    time.sleep(0.005)



