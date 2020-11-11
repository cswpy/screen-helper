# A Web-based Eye-Tracker
Developed for NYUAD 2020 Challenge, this web-based application utilize opencv to track eyes and send notifications to the browser when distracted.

## Inspiration
College is hard, finishing college online with zoom calls and no friends is particularly hard. The online distractions are constantly stealing our attention away from the things that matter. Our eyes grow sore after hours and hours of reading and lecturing. So we created the webapp to help you restore the focus during lectures and rest your eyes from time to time.

## How it was built

* Eye Tracking
  * [OpenCV](https://opencv.org/)
* Backend
  * [Flask](https://flask.palletsprojects.com/)
  * Socket.io
* Webcam
  * [imutils](https://pypi.org/project/imutils/)

## What we have learned
1. Deploy computer vision models in webapp
2. Render video stream in Flask
3. Using socket.io for front-back end communications
......

## Challenges
Pivoting the initial idea to an actionable project requires much efforts. Giving up certain features that are too hard to implement is hard. Debugging the ML model so that it works in lightning speed...


### Deploy
Run
```bash
python app.py -i <ip address> -o <port>
```
to deploy the application locally

## Known