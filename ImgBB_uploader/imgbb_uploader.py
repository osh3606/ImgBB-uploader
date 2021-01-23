import base64
import requests
import os
import shutil
import csv    

# Set variables
apiKey = 'ImgBB_API_Key' 		# insert your ImgBB API key
imgPath = "./img/" 					# image path
uploadedFilePath = imgPath + '/uploaded/' 			# move images to other folder after uploaded
extentions = [".jpg", ".jpeg", ".png", ".gif",".webp"]	# Image extentions
csvFileName = 'ImageURLs.csv' 				# Save URLs for each images


# Create directories if not exists
if not os.path.exists(imgPath):
    os.makedirs(imgPath)

if not os.path.exists(uploadedFilePath):
    os.makedirs(uploadedFilePath)

# Initialize CSV file
file_exists = os.path.isfile(csvFileName) 			# Check CSV file exists


if not file_exists: # If CSV file doesn't exists, create CSV file and add headers
    with open(csvFileName, 'a') as csvImageURL:
        headers = ["Image Name", "Full Image", "Medium Image", "Thumbnail"]
        writer = csv.DictWriter(csvImageURL, delimiter=',', lineterminator='\n',fieldnames=headers)
        writer.writeheader()


# Upload, Record URLs and move files
fileList = list(os.walk(imgPath))[0][2] 			# List files in Path

print("imgBB API Uploader")
print("API Key: " + apiKey)

for file in fileList:
    for extention in extentions: # Check file names if it contains image extentions defined in "extentions"
        if extention in file:
            with open(imgPath+file, "rb") as uploadFile:
                url = "https://api.imgbb.com/1/upload"
                payload = {
                    "key": apiKey,
                    "image": base64.b64encode(uploadFile.read()),
                }
                res = requests.post(url, payload)

            if res.status_code == 200: 					# if upload success
                print("Image Successfully Uploaded:",file)
                
                URLlist = [file] # 1st column = File Name
                URLlist.append(res.json()['data']['image']['url']) 	 	# 2nd data = full image URL
                try:
                    URLlist.append(res.json()['data']['medium']['url']) 	# 3rd data = medium image URL, if exist
                except:
                    URLlist.append('') 					# 3rd data = if medium image not exist, blank column
                    pass
                URLlist.append(res.json()['data']['thumb']['url']) 		# 4th data = thumbnail image URL

                with open(csvFileName, 'a') as csvImageURL: 		# record in CSV file [file names + all URLs in row]
                    wr = csv.writer(csvImageURL)
                    wr.writerow(URLlist)
                    
                shutil.move(imgPath+file,uploadedFilePath+file) 		# move uploaded file to 'uploaded folder'
            else:
                print("ERROR")
                print("Server Response: " + str(res.status_code))
            break
csvImageURL.close()
print("All Done!")