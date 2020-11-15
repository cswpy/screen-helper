# A Web-based Eye-Tracker
Developed for the HackAD Challenge for Virtual Good 2020, this web-based application utilize opencv to track eyes and send notifications to the browser when distracted.

## Inspiration
College is hard, finishing college online with zoom calls and no friends is particularly hard. The online distractions are constantly stealing our attention away from the things that matter. Our eyes grow sore after hours and hours of reading and lecturing. So we created the webapp to help you restore the focus during lectures and rest your eyes from time to time.

## How it was built

* Eye Tracking
  * [OpenCV](https://opencv.org/)
* Backend
  * [Flask](https://flask.palletsprojects.com/)
  * [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/)
* Webcam
  * [imutils](https://pypi.org/project/imutils/)

## What we have learned
1. Deploy computer vision models in webapp
2. Render video stream in Flask
3. Using Flask-SocketIO for bi-lateral client-server communication

## Challenges
- Pivoting the initial idea to an actionable project requires much efforts. 
- Giving up certain features that are too hard to implement is hard. 
- Debugging the ML model so that it works in lightning speed...
- Finding a way to initiate client-server communication
- Smoothing the noise from the ML model to get more stable results

## How to use it

### Deploy
1. Create a new virtual environment to keep the project dependencies separate from your other projects
2. Clone the github repository:
    ```bash
    git clone https://github.com/cswpy/screen-helper.git
    cd screen-helper
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run
    ```bash
    python app.py -i <ip address> -o <port>
    ```
    To run it on localhost, use `<ip address>` = 127.0.0.1 and `<port>`=5000.

### Usage
- After running, the web app will be hosted at `http://<ip address>:<port>/`. 
Paste this address in a web browser. The landing page will ask you to fill a form with 
your name and your choice of mode. After choosing the mode, choose the interval for which you want
the application to notify you (in minutes). Once you've filled the form, you're ready for a productive
online session!  

#### Modes
- `Study mode`: Choose this mode if you are planning on studying/working on your laptop for a prolonged
period of time. The web app will track your eyes and notify you if you have been
staring at the screen for too long. Click on "Show me the magic!" to see the ML model's analysis of the video feed
from your camera.

- `Class mode`: Choose this mode if you will be attending an online class and want to be notified whenever you get
 distracted. The web app will track your eyes and notify you if you have lost attention for too long. 
 Click on "Show me the magic!" to see the ML model's analysis of the video feed
from your camera.

## Contributors
- Phillip Wang
- Reem Hazim
- Yernar Mukayev


Credits to Antoine Lame for eye tracker’s trained model files


## Known