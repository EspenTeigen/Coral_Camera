from classes.camera import Camera
from periphery import GPIO
import threading
from multiprocessing.pool import ThreadPool
import time
from classes.display import Display



def main():
    print("initializing")
    pool = ThreadPool(processes=1)
    #Time operator have to push button after product is detected
    IMG_SAVE_DELAY = 500
    #This is used to signal that if operator dont push button then save image to approved folder
    flagPhotoSensor = False
    #Resolution on image
    resolution = (1280,720)
    #Paths to put images
    path_approved = '/media/storage/good/'
    path_not_approved = '/media/storage/bad/'
    #Create camera object that takes images and store in approved or not approved folder
    camera = Camera(resolution, 'png', path_approved, path_not_approved)
    #GPIO stuff
    on_off = GPIO(7 ,'in')
    disallowed_img = GPIO(138, 'in')
    disallowed_img.edge = 'rising'
    photoSensor = GPIO(140, 'in')
    photoSensor.edge = 'rising'
    #Create Display object
    display = Display()
    #Variable to handle debounce on input from photosensor
    lastPhotoSensorValue = False
    #Variable to handle debounce on input from operator button
    lastOperatorBtnValue = False
    #Get time in ms
    currentTime_ms = lambda: int(round(time.time() * 1000))
    #Calculate new time - old time to get time difference between two events
    deltaTime_ms = lambda oldTime_ms: int(round(time.time() * 1000)) - oldTime_ms
    #Store time to calculate time difference
    oldTime_ms = currentTime_ms()
    print("initialization done")


    #Run forever
    while True:
        #If system is turned on by switch, run program
        display.off()
        if on_off.read() or True:
            print("System started")
            #Make sure no old values are stored
            flagPhotoSensor = False
            camera.camera.start()
            #Stay in loop as long as system is turned on
            while on_off.read() or True:

                #If there is a product in front of camera, take a picture and record the time
                if photoSensor.read() and not lastPhotoSensorValue and not flagPhotoSensor:
                    
                    #img = camera.camera.get_image()
                    async_img = pool.apply_async(camera.take_image)
                    oldTime_ms = currentTime_ms()
                    #Save that photo sensor has been high
                    flagPhotoSensor = True

                #If operator push button before IMG_SAVE_DELAY time, save image to not approved folder
                #and blink red light once to inform operator
                while deltaTime_ms(oldTime_ms) <= IMG_SAVE_DELAY:
                    if disallowed_img.read() and not lastOperatorBtnValue:
                        img = async_img.get()
                        threading.Thread(target = display.show_img, args=(img, False)).start()
                        camera.save_img(img, False)
                        flagPhotoSensor = False

                lastOperatorBtnValue = disallowed_img.read()
                
                #if operator dont push button before IMG_SAVE_DELAY time run out, save 
                #image to approved folder and blink green light. 
                if (deltaTime_ms(oldTime_ms) > IMG_SAVE_DELAY) and flagPhotoSensor:
                    img = async_img.get()
                    threading.Thread(target = display.show_img, args=(img, True)).start()
                    camera.save_img(img, True)
                    flagPhotoSensor = False

                
            camera.camera.stop()
            lastPhotoSensorValue = photoSensor.read()
                    
if __name__ == '__main__':
    main()
