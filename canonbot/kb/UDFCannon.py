import sys, requests, json, os


# setup the correct URL
CCAPIHOST = os.getenv('CCAPIHOST','partner.predictika.com')
CCAPIPORT = os.getenv('CCAPIPORT','5500')

CC_IP = '0cd0a4e6.ngrok.io'
CC_PORT = '8080'

# set this to True for actual get/post 
POST_TO_CCAPI=True

CC_ENV = "http://"+CC_IP+"/ccapi/ver100"
INIT_CMD = "http://"+CC_IP+"/ccapi"
INIT_DONE = False

ZOOM_STEP = 10


URLSTR = 'http://'+CCAPIHOST+':'+CCAPIPORT+'/ccapi/cccmd'
headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

cmds = [ 'init', 'takepicture', 'deletepicture', 'tiltup', 'tiltdown', 
         'panleft', 'panright', 'zoomin', 'zoomout',
         'cameraon', 'cameraoff' , 'modepicture', 'modevideo','startrecording','stoprecording','zoomposition']



ccapi_commands = { 
                   'takepicturestart' : { 
                       'url' : '/shooting/control/shutterbutton/manual',
                       'body': { 
                                 "action": "half_press", 
                                 "af"    : True 
                               }
                   },
                   'takepicturefull' : { 
                       'url' : '/shooting/control/shutterbutton/manual',
                       'body': { 
                                 "action": "full_press", 
                                 "af"    : True 
                               }
                   },
                   'takepicturestop' : { 
                       'url' : '/shooting/control/shutterbutton/manual',
                       'body': { 
                                 "action": "release", 
                                 "af"    : False 
                               }
                   },
                   'zoomin' : {
                       'url' : '/shooting/control/zoom',
                       'body': { 
                                 "value": 100
                               }
                   },
                   'zoomout': {
                       'url': '/shooting/control/zoom',
                       'body': {
                       "value": 0
                                }
                   },'modepicture': {
                        'url': '/shooting/control/moviemode',
                        'body': {
                            "action": "off"
                        }
                    },
                   'modevideo': {
                        'url': '/shooting/control/moviemode',
                        'body': {
                            "action": "on"
                        }
                    },
                   'startrecording': {
                        'url': '/shooting/control/recbutton',
                        'body': {
                            "action": "start"
                        }
                    },
                   'stoprecording': {
                        'url': '/shooting/control/recbutton',
                        'body': {
                            "action": "stop"
                        }
                    },
                   'zoomposition': {
                        'url': '/shooting/control/zoom',
                        'body': {}
                    },
                   'init' : {
                       'url' : INIT_CMD,
                       'body': { }
                   },
                   'deviceinfo' : { 
                       'url' : '/deviceinformation',
                       'body': { }
                   },
                 }



def sendCCAPICommand(urlstr, body, request_type, takeurl_asis=False):

    retval = 200
    message = 'successful!'
    if (takeurl_asis):
        urlstr_full = urlstr
    else:
        urlstr_full = CC_ENV + urlstr
    print("In sendCCAPICommand to url="+urlstr_full+ " body="+str(body))
    try:
        if (request_type == 'get'):
            #print("+++++GET+++++")
            if (POST_TO_CCAPI):
                response = requests.get(url=urlstr_full, headers=headers)
                retval = response.status_code
        else:
            #print("+++++POST+++++")
            if (POST_TO_CCAPI):
                response = requests.post(url=urlstr_full, headers=headers, json=body)
                retval = response.status_code
        #retval = response.status_code
        if ((retval == 200) or (retval == 201)):
            message = 'Command successful!'
        else:
            message = 'Error occurred while sending command! Status='+ str(response.status_code) + ' Reason= ' + str(response.reason)
            print(message)
    except:
        message = 'Exception occurred while sending command!'

    return retval, message

def takepicture():
    print("In takepicture")

    data = ccapi_commands['takepicturestart']
    urlstr = data['url']
    body = data['body']
    r, m = sendCCAPICommand(urlstr, body, 'post')

    data = ccapi_commands['takepicturefull']
    urlstr = data['url']
    body = data['body']
    r, m = sendCCAPICommand(urlstr, body, 'post')

    data = ccapi_commands['takepicturestop']
    urlstr = data['url']
    body = data['body']
    r, m = sendCCAPICommand(urlstr, body, 'post')

    return  r, m

def deviceinfo():
    print("In deviceinfo")

    data = ccapi_commands['deviceinfo']
    urlstr = data['url']
    body = data['body']
    r, m = sendCCAPICommand(urlstr, body, 'get')

    return  r, m

def zoomin():
    print("In zoomin")
    data = ccapi_commands['zoomin']
    urlstr = data['url']
    zoompos = zoomposition() + ZOOM_STEP
    body = {"value": zoompos}
    r, m = sendCCAPICommand(urlstr, body, 'post')
    return  r, m

def zoomout():
    print("In zooming out")
    data = ccapi_commands['zoomout']
    urlstr = data['url']
    zoompos = zoomposition() - ZOOM_STEP
    body = {"value": zoompos}
    r, m = sendCCAPICommand(urlstr, body, 'post')
    return  r, m

def zoomposition():
    print("Getting zoom position")
    data = ccapi_commands['zoomposition']
    urlstr = data['url']

    currentPosition = 0
    urlstr_full = CC_ENV + urlstr
    try:
        if (POST_TO_CCAPI):
            response = requests.get(url=urlstr_full, headers=headers)
            retval = response.status_code
            if ((retval == 200) or (retval == 201)):
                currentPosition = int(response.json()["value"])
                message = 'Command successful!'

            else:
                message = 'Error occurred while sending command! Status=' + str(response.status_code) + ' Reason= ' + str(
                    response.reason)
    except:
        message = 'Exception occurred while sending command!'
    print(message)

    return currentPosition


def modepicture():
    print("In Picture Mode")
    data = ccapi_commands['modepicture']
    urlstr = data['url']
    body = data['body']
    r, m = sendCCAPICommand(urlstr, body, 'post')
    return  r, m

def modevideo():
    print("In Video Mode")
    data = ccapi_commands['modevideo']
    urlstr = data['url']
    body = data['body']
    r, m = sendCCAPICommand(urlstr, body, 'post')
    return  r, m

def startrecording():
    print("Recording started")
    data = ccapi_commands['startrecording']
    urlstr = data['url']
    body = data['body']
    r, m = sendCCAPICommand(urlstr, body, 'post')
    return  r, m

def stoprecording():
    print("Recording stopped")
    data = ccapi_commands['stoprecording']
    urlstr = data['url']
    body = data['body']
    r, m = sendCCAPICommand(urlstr, body, 'post')
    return  r, m

def initializeCCAPI():
    print("In initializeCCAPI")

    data = ccapi_commands['init']
    urlstr = data['url']
    body = data['body']
    r, m = sendCCAPICommand(urlstr, body, 'get', True)

    return  r, m


cmdMethods = { "takepicture" : takepicture, 
               "deviceinfo"  : deviceinfo,
               "zoomin"      : zoomin,
               "zoomout"     : zoomout,
               "init"        : initializeCCAPI,
               "startrecording": startrecording,
               "stoprecording": stoprecording,
               "modevideo"   : modevideo,
               "modepicture" : modepicture,
             }

def ExecuteCommand(cmdname, option=''):
    print('Executing Command = ' + str(cmdname) + ' ' + str(option))

    global INIT_DONE
    if (INIT_DONE == False):
        initializeCCAPI()
        INIT_DONE = True

    if (cmdname in cmdMethods):
        ret, msg = cmdMethods[cmdname]()
    else:
        ret = 400
        msg = "Unimplemented command"
        #print(msg)

    #print("Status = " + str(ret))
    #print("Message = " + str(message))

    return ret, msg


def main(argv):
    print("POST command from bot ...")
    print("ACTUAL POSTING TO CCAPI IS " + str(POST_TO_CCAPI))
 
    for cmd in cmds:
        r, m = ExecuteCommand(cmd)
        print("Return value="+str(r)+" Message="+str(m))


if __name__ == "__main__":
    main(sys.argv[1:])
