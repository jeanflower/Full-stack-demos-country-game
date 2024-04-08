# See https://fastapi.tiangolo.com/deployment/docker/#build-a-docker-image-for-fastapi
# See https://fastapi.tiangolo.com/tutorial/request-files/
# for VSCode to stop warnings, install dependencies locally e.g.
# python3 -m pip3 install fastapi

from typing import Union, Annotated
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import shutil
import cv2

from .findPaths import getShortestPathUsingNames

# print(cv2.__version__)

app = FastAPI()

@app.get("/hello")
def read_root():
  return {"Hello": "World"}

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
  file_location = f"/tmp/{file.filename}"
  with open(file_location, "wb+") as file_object:
    shutil.copyfileobj(file.file, file_object)

  sample_image = cv2.imread(file_location)
  mean = sample_image.mean() 
  return {"info": f"file '{file.filename}' saved at '{file_location}', mean val {mean}"}

@app.get("/")
async def main():
  content = """
<!DOCTYPE html>
<html>
<head>
    <title>Python app demo</title>
</head>
<body>
    <a href='/game'>game</a>
    <br/>
    <a href='/upload'>upload file</a>
</body>
</html>
    """
  return HTMLResponse(content=content)

@app.get("/upload")
async def main():
  content = """
<!DOCTYPE html>
<html>
<head>
    <title>Upload</title>
</head>
<body>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <!-- File input field -->
        <label for="file">Choosen file will be saved on server :</label>
        <input type="file" id="file" name="file" accept=".txt, .pdf, .jpg, .png">
 
        <br><br>
         
        <!-- Submit button -->
        <input type="submit" value="Upload">
    </form>
</body>
</html>
    """
  return HTMLResponse(content=content)

@app.get("/game")
async def main():
  content = """
<!DOCTYPE html>
<html>
<head>
    <title>Country paths</title>
</head>
<body>
    <form action="/path" method="get">
        <!-- File input field -->
        <input type="text" id="start" name="start">
        <input type="text" id="end" name="end">

        <br><br>
         
        <!-- Submit button -->
        <input type="submit" value="Get path">
    </form>
</body>
</html>
    """
  return HTMLResponse(content=content)

@app.get("/path")
async def find_path(start: str = 'Portugal', end: str = 'Germany'):

  path =  getShortestPathUsingNames(start, end)
  print(path)
  result = """<!DOCTYPE html>
<html>
<head>
    <title>Country paths</title>
</head>
<body>
    <form action="/path" method="get">
        <!-- File input field -->
        <input type="text" id="start" name="start">
        <input type="text" id="end" name="end">

        <br><br>
        
        <!-- Submit button -->
        <input type="submit" value="Get path">
    </form>
"""  
  result = result + 'Path from ' + start + ' to ' + end + """
    <div>
"""
  if len(path) == 0:
    result = result + 'You shall not pass'
  for country in path:
    result = result + '<br/>' + country
  result = result + """
</div>
</body>
</html>
    """
  return HTMLResponse(content=result)

@app.get("/pathRaw")
async def find_path(start: str = 'Portugal', end: str = 'Germany'):
  path =  getShortestPathUsingNames(start, end)
  return path