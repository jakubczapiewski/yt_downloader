#YT Downloader
## General info
This project is backend to YouTube video downloader.


## Setup
Install requirements

`pip3 install -r requirements.txt`

`python3 manage.py makemigrations yt_downloader`
`python3 manage.py migrate`


###Run tests 
`manage.py test` 

## How to use
To run server: `python manage.py runserver`

Create a request: `curl -i -X POST -H "Content-Type: application/json" -d "{""url"":""https://youtu.be/iSutodqCZ74""}" http://127.0.0.1:8000/create_request/`
It returns request id 
You can check your download progress:  `curl -i -X POST http://127.0.0.1:8000/download_progress/` + your request id + `/`
if its 100 your file is ready you can download it:  `curl http://127.0.0.1:8000/download/` + your request id + `/ --output 1.mp4`