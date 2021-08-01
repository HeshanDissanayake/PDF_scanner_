from time import sleep
from threading import Thread
import os
from fpdf import FPDF
from picamera import PiCamera
camera = PiCamera()
w = int(1364*0.45)
h = int(1944*0.45)

camera.resolution = (w, h)


_ =  input("Press ENTER to begin")
isRead = True


def activate_actuator():
    sleep(1)
    print("turning page...")
    sleep(2)
    


def check_input():
    global In
    _ = input()
    In = True

def genOutputFileName():
    nums = [0]
    for file in os.listdir('pdf'):
        nums.append(int(file.strip('scanned_file_').strip('.pdf')))
        
    return 'pdf/scanned_file_' + str(max(nums)+1) + ".pdf"

def show(num, status):
    print("\033c")
    print("Page Number: ", num)
    print(status)

image_num = 1 

thread = Thread(target=check_input)
thread.start()

# remove previouse images in the images directory
for i in os.listdir('images'):
    os.remove('images/'+i)

In = False 
while(True):
    show(image_num, "Capturing Image..")
    
    camera.start_preview()
    camera.capture('images/'+str(image_num)+'.jpg')
    sleep(1)
    camera.stop_preview() 

    show(image_num, "Captured ✔️")
    activate_actuator()
    
    image_num = image_num + 1

    if In:
        break

print("\033c")
print("Scanning Done")
print(image_num, "pages scanned")
sleep(0.5)

output_file = genOutputFileName()
print("converting Images to PDF: "+output_file)
# with open(output_file, "wb") as f:
#     f.write(img2pdf.convert([i for i in os.listdir('images') if i.endswith(".jpeg")]))
# print("OutPut saved to: ", output_file)

pdf = FPDF()
# imagelist is the list with all image filenames
imagelist = [i for i in os.listdir('images') if i.endswith(".jpg")]
for image in imagelist:
    pdf.add_page()
    pdf.image("images/"+image,0,0)
pdf.output(output_file, "F")


thread.join()



