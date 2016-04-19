

# Shot_Detector
<<<<<<< HEAD
import mraa 
import time
import socket   #for sockets
import sys  #for exit

INTERVAL = .05                   # Sound Signature Sample time
SENDMSG_INTERVAL =60           # Minimum time between sending something to cloud




=======
>>>>>>> b34f493becfefed0077b32da0fa7221e73587922
#LED_GPIO = 5                   # The LED pin
TRIGGER_GPIO = 6               # The TRIGGER GPIO
#led = mraa.Gpio(LED_GPIO)      # Get the LED pin object
#led.dir(mraa.DIR_OUT)          # Set the direction as output
trig = mraa.Gpio(TRIGGER_GPIO)   # Get the TRIGGER pin object
trig.dir(mraa.DIR_IN)           # Set the direction as input

#ledState = False               # LED is off to begin with
#led.write(0)


def getTriggerf():
    """ This function operates for minimal send interval """
    t = time.time()
    next_sample_time = t + SENDMSG_INTERVAL
    
    while (1):
        t = time.time()
        if t > next_sample_time:
            #print 'Timed Out'
            return (1)
        if (trig.read() != 0):
            # No trigger detected
            continue
        else:
            # Detected a trigger
            return (0)


def getSignature():
    """ This function determines if a valid shot is fired """                
    t = time.time() 
    next_sample_time = t + INTERVAL
    lowCt=0
    highCt=0
    prevstate=0
    toggleCt=1
                
    while True:
        t = time.time()  
        if (trig.read() != prevstate):
            toggleCt += 1
            prevstate= trig.read()
        else:

            if t > next_sample_time:
                #print highCt
                #print lowCt
                #print toggleCt
                shotdata=[]
                shotdata.append (highCt)
                shotdata.append (lowCt)
                shotdata.append (toggleCt)
                return shotdata

        if trig.read() == 1:
             # valid highpulse
             highCt += 1
             continue
                    
        else:
            # Detected a click
            lowCt += 1
            continue
            
            
if __name__ == '__main__':
    host = '127.0.0.1'
    port = 41234
    msg = '{"n": "temp", "v": 1.0}'
    nullmsg = '{"n": "temp", "v": 0.0}'
    shotCt=0
<<<<<<< HEAD


    shotmsg = ''.join(('{"n": "shots", "v": ', str(shotCt),'}'))
    print shotmsg
    shotnullmsg = '{"n": "shots", "v": 0}'
    print shotnullmsg
=======
    shotmsg = ('{"n": "temp", "v": '+ shotCt +'}')
    shotnullmsg = '{"n": "temp", "v": ' + 0 +'}'
>>>>>>> b34f493becfefed0077b32da0fa7221e73587922
    t = time.time()
    next_sample_time = t + SENDMSG_INTERVAL
    
    # initialize our socket...
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()

    while 1:
<<<<<<< HEAD
        shotmsg = ''.join(('{"n": "shots", "v": ', str(shotCt),'}'))

=======
>>>>>>> b34f493becfefed0077b32da0fa7221e73587922
        t = time.time()    
        if t > next_sample_time:
            try :
                #Set the whole string
                s.sendto(shotmsg, (host, port))
<<<<<<< HEAD
                print 'SHot Message Sent', shotCt
=======
#               print 'Message Sent', shotCt
>>>>>>> b34f493becfefed0077b32da0fa7221e73587922
                shotCt=0
                

            except socket.error, msg:
                print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
                sys.exit()
<<<<<<< HEAD
           
        print 'going into get trigger'
	# wait until trigger or timed out
=======
            continue
        # wait until trigger or timed out
>>>>>>> b34f493becfefed0077b32da0fa7221e73587922
        lowtrig = getTriggerf()
 
        if lowtrig != 0:
                 
            try:
                #Set the whole string
                s.sendto(nullmsg, (host, port))
                print 'Null Message Sent'
                print nullmsg

            except socket.error, msg:
                print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
                sys.exit() 
<<<<<<< HEAD
           
=======
            continue
>>>>>>> b34f493becfefed0077b32da0fa7221e73587922
        else:    
            shotdata =getSignature ()
            #print 'Signature Detected'
            print shotdata

            if shotdata[1] > 5 < 100 and shotdata[2] > 5 < 50 :
                try :
                    #Set the whole string
                    s.sendto(msg, (host, port))
                    shotCt += 1
<<<<<<< HEAD
                    print 'Threshold reached', shotCt
=======
                    print 'Message Sent', shotCt
>>>>>>> b34f493becfefed0077b32da0fa7221e73587922

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
<<<<<<< HEAD


=======
>>>>>>> b34f493becfefed0077b32da0fa7221e73587922
