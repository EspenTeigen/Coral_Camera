import pygame
import pygame.camera
from pygame.locals import *
import time
import os
import re


class Camera:
    def __init__(self, resolution, filetype, path_approved, path_not_approved):
        pygame.init()
        #Configure camera
        self.CAMERA_RES = resolution
        self.DISPLAY_RES = (1080,720)
        self.FILETYPE = '.' + filetype
        self.PATH_APPROVED = path_approved	
        self.PATH_NOT_APPROVED = path_not_approved
        self.img_number_approved= self.get_filenumber_from_directory(self.PATH_APPROVED)
        self.img_number_not_approved = self.get_filenumber_from_directory(self.PATH_NOT_APPROVED)
        pygame.camera.init()
        #Get camera and start it
        self.camera = pygame.camera.Camera(pygame.camera.list_cameras()[1], self.CAMERA_RES)
        

    def take_image(self):
        for i in range(0,3):
            img = self.camera.get_image()
        return img

    def save_img(self, img, approved):
        #Take image and save it
        if approved:
            #Increment to get a new image number
            self.img_number_approved = self.img_number_approved + 1
            #Construct filename with numbering and leading zeros
            file = self.PATH_APPROVED + str('{:05}'.format(self.img_number_approved)) + self.FILETYPE
        else:
            #Increment to get a new image number
            self.img_number_not_approved = self.img_number_not_approved + 1
            #Construct filename with numbering and leading zeros
            file = self.PATH_NOT_APPROVED + str('{:05}'.format(self.img_number_not_approved)) + self.FILETYPE
        
        pygame.image.save(img, file)

    #Look in /media/storage/good and bad and get the highest number on image-file
    def get_filenumber_from_directory(self, path):
        numbers = []
        #Get list of files in directory
        list = os.listdir(path)
        #If directory is empty return value 0 since there is no images
        if len(list) == 0:
            return 0
        else :    
            #Get file names and extract the integers
            for i in range(0, len(list)):
                data = list[i].split(".")
                numbers.append(data[0])
        
            #Find highest integrer name on image
            higestNumber = int(max(numbers)) 
            return higestNumber

 