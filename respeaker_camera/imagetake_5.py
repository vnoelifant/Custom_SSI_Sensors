#import picamera
from datetime import datetime
from collections import deque
#import csv
#import os
#import glob
import numpy
#import copy
#import sys
import pygame
import pygame.camera
#from socket import *
#from struct import pack
from PIL import Image
from PIL import ImageStat
from time import sleep
from io import BytesIO
import time
#import base64
import numpy as np
#from autobahn.twisted.websocket import WebSocketClientFactory
#from autobahn.twisted.websocket import WebSocketClientProtocol
#from twisted.python import log
#from twisted.internet import reactor
#from twisted.internet.task import LoopingCall


#log.startLogging(sys.stdout)


class Camera:

    def __init__(self, saveLocation='/home/pi/Desktop/Images/', maxSize=100):
        self.saveLocation = saveLocation
        self.maxSize=maxSize
        self.q = deque()
        self.rotationCount = 0
        #Remove previously stored images and image name list
        #for doc in glob.glob(self.saveLocation + "im*"):
        #    os.remove(doc)
            
        #Initialize Pi Camera
        found = False

        while not found:
            self.webCam = True
            self.cameras = []
            for i in range(0,5):
                title = "/dev/video" + str(i)
                if self.checkDevice(title):
                    pygame.camera.init()
                    pygame.camera.list_cameras()
                    self.cameras.append(pygame.camera.Camera(title,(640,480)))
            if len(self.cameras) == 0:
                self.webCam = False

            self.stream = BytesIO()
            if not self.webCam:
                print("no cam found")
                #self.currentCamera = picamera.PiCamera()
            else:
                found = True
                for cam in self.cameras:
                    cam.start()


        #Opens the file of image names so that text can be written in it
        self.file = open(saveLocation + 'imagenames.txt', 'w')
        #self.writer = csv.writer(file)
        self.newImg = None
        self.lastImg = None
        self.difference = 50000
        
    def onOpen(self):
        print("open")
        self.process_camera_data()
        
    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
    def onClose(self, wasClean, code, reason):
        print(wasClean, code, reason)
        
    def checkDevice(self, title):
        try:
            pass
            #return os.stat(title)
        except:
            return False
    
    def process_camera_data(self):            
        startTime = time.time()
        img = ""
        #Image name consists of "im" than the time
        name = 'im' + str(datetime.now().strftime('%H%M%S')) + '.jpg'        
        print(name)
        
        #Captures image and savesit in the save location
        
        #self.stream = BytesIO()
        #startTakenTime = time.time()
        
        #self.stream.seek(0)
        
        if self.webCam:
            self.currentCamera = self.cameras[self.rotationCount]
            print("Using Web Camera " + str(self.rotationCount))
            self.rotationCount += 1
            if self.rotationCount == len(self.cameras):
                self.rotationCount = 0
            img = self.currentCamera.get_raw()
            return img
        '''
            imgBt = pygame.image.tostring(tmpimg,"RGBA",False)
            img = Image.frombytes("RGBA",(640,480),imgBt)
            #img2 = copy.copy(img)
            img.save(self.stream, format='jpeg')
            
            
        else:
            print("Using Pi Camera")
            self.currentCamera.capture(self.stream, format='jpeg')
            img = Image.open(self.stream)
        
        self.stream.seek(0)
        
        print("Picture taken in " + str(time.time() - startTakenTime) + " seconds")
        if self.newImg != None:
            self.lastImg = self.newImg
        self.newImg = img.convert('L')
        if self.lastImg != None:
            self.difference = similarity(self.lastImg,self.newImg)
        print(self.difference)
        if brightness(self.newImg) > 30 and self.difference > 20000:
            print("Brightness and difference over threshold. Image saved")
            self.q.appendleft(name)
            
            #Write image name in the image name text file
            self.writer.writerow([name])
            self.file.flush()
            
            #self.sendMessage(name.encode('utf8'))
            #imgBytes = bytearray(imgBytes)
            #print('Attempting to send message')
            #self.sendMessage(imgBytes, True)
            #print('Message sent.')
            
            #Removes the oldest imag eif the number of images exceeds the maxSize
            if(len(q) > self.maxSize):
                #Oldest image is removed from queue
                removedImage = q.pop()
                #Oldest image is deleted from file
                os.remove(self.saveLocation + removedImage)
                #Close open writing
                self.file.close()
                #Open the image file Document for reading and read all lines
                self.file = open(self.saveLocation + 'imagenames.txt', 'r')
                lines = self.file.readlines()
                self.file.close()
                #Delete the image names file
                os.remove(self.saveLocation + 'imagenames.txt')
                #Create a new image names file for writing
                self.file = open(self.saveLocation + 'imagenames.txt', 'w')
                self.writer = csv.writer(file)
                #Go line by line through the previously read image name file
                for line in lines:
                    #Remove quotes and newLine from previously read line
                    line = line.strip('\"')
                    line = line.strip('\n"')
                    #Unless the image name is the removed image write it to the new file
                    if(line != removedImage):
                        self.writer.writerow([line])
                        self.file.flush()
            
        print("Picture taken and processed in " + str(time.time() - startTime) + " seconds.")
        imgBytes = self.stream.getvalue()
        return imgBytes
        '''
        #Wait a set time before taking an image
        #sleep(waitTime)
        #reactor.callLater(1, self.process_camera_data)


def brightness(img):
    stats = ImageStat.Stat(img)
    return stats.rms[0]

def similarity(last, new):
    smallLast = numpy.asarray(last.resize([40,40], Image.ANTIALIAS))
    smallNew = numpy.asarray(new.resize([40,40], Image.ANTIALIAS))
    return numpy.sum((smallLast-smallNew)**2)





'''
if __name__ =='__main__':

   factory = WebSocketClientFactory()
   factory.protocol = MyClientProtocol
   reactor.connectTCP("192.168.1.3", 45000, factory)
   reactor.run()
'''
   
    