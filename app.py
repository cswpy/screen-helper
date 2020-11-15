# USAGE
# python webstreaming.py --ip 0.0.0.0 --port 8000

# import the necessary packages
from imutils.video import VideoStream
from gaze_tracking import GazeTracking
from playsound import playsound
import simpleaudio as sa
from flask import Response, Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
import threading
import argparse
import imutils
import time
import time
import cv2


# Loading the audio file
#wave_obj = sa.WaveObject.from_wave_file("sound1.wav")

# counters to keep track of number of eye position changes
counter_screen = 0
counter_attention_lost = 0
#message keeps track of latest message displayed on video feed
message = ""
#now keeps track of the last time we compared the count of screen versus attention lost
now = 0

# Flags to keep track of whether the user was staring at screen/lost attention
staring_screen = False
attention_lost = False

# Make person's name and mode global
name = ""
mode = ""

# For study mode: how often to send a break notification (in secs)
break_time_interval = 1800		#default 30 min

# For class mode: how many consecutive seconds of attention lost qualify a notifcation (in secs)
attention_lost_threshold = 1800     #default 30 min

gaze=GazeTracking()

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)
outputFrame = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# initialize the video stream and allow the camera sensor to
# warmup
#vs = VideoStream(usePiCamera=1).start()
vs = VideoStream(src=0).start()
time.sleep(2.0)

@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")

@app.route('/form-handler', methods=['POST'])
def handle_data():
	global name, mode, break_time_interval, attention_lost_threshold
	name = request.form['name']
	mode = request.form['mode']
	if mode == "Study":
		break_time_interval = int(request.form['interval']) * 60
	else:
		attention_lost_threshold = int(request.form['interval']) * 60
	return render_template("working_page.html", mode=mode, name=name)

def head_pose(frameCount):
	# grab global references to the video stream, output frame, and
	# lock variables
	global vs, outputFrame, lock, gaze, now, message, counter_screen, counter_attention_lost, staring_screen, attention_lost
	global name, mode
	# initialize the motion detector and the total number of frames
	# read thus far
	total = 0
	staring_screen = False
	screen_timer = 0

	# loop over frames from the video stream
	while True:
		# read the next frame from the video stream, resize it,
		# convert the frame to grayscale, and blur it
		frame = vs.read()
		# frame = imutils.resize(frame, width=400)
		# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# gray = cv2.GaussianBlur(gray, (7, 7), 0)

		# grab the current timestamp and draw it on the frame
		# timestamp = datetime.datetime.now()
		# cv2.putText(frame, timestamp.strftime(
		# 	"%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
		# 	cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

		# We send this frame to GazeTracking to analyze it
		gaze.refresh(frame)

		frame = gaze.annotated_frame()
		#display the message depending on whether the user is looking at screen
		#or lost attention (see end of this function where message is determined)
		text = message

		# if gaze.is_blinking():
		# 	text = "Blinking"

		if gaze.is_right():
			# text = "Looking right"
			#increment attention lost counter by 1
			counter_screen = counter_attention_lost + 1

		elif gaze.is_left():
			# text = "Looking left"
			# increment attention lost counter by 1
			counter_screen = counter_attention_lost + 1

		elif gaze.is_center():
			# text = "Looking center"
			#increment looking at screen counter by 1
			counter_screen = counter_screen + 1

		else:
			# text = "Attention lost"
			counter_attention_lost = counter_attention_lost + 1

			#time.sleep(5)
			# if (( not gaze.is_blinking()) or ( not gaze.is_left()) or ( not gaze.is_center())):
			# 	threading.Thread(target=playsound, args=('sound1.wav',), daemon=True).start()
			#wave_obj.play()
		cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (255, 255, 0), 2)

		# left_pupil = gaze.pupil_left_coords()
		# right_pupil = gaze.pupil_right_coords()
		#cv2.putText(frame, "Left:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
		#cv2.putText(frame, "Right: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

		# cv2.imshow("Eye tracker",    frame)

		if cv2.waitKey(1) == 27:
			break

		# acquire the lock, set the output frame, and release the
		# lock
		with lock:
			outputFrame = frame.copy()

		#If more than one sec has passed since last comparison
		if time.time() - now >= 1:
			#check if lost attention more than looking at screen
			if counter_attention_lost >= counter_screen:
				message = "attention lost"
				# socketio.emit('attention lost', {'data': 30})
			else:
				message = "staring at the screen"

			#reset the timer
			now = time.time()
			#reset the counters
			counter_attention_lost = 0
			counter_screen = 0

		# Check if current mode is study mode
		if mode == 'Study':
			#check if user is staring at screen
			if message == "staring at the screen":
				#check if user was not staring at screen before
				if not staring_screen:
					#start the timer
					screen_timer = time.time()
					#set the flag to true
					staring_screen = True
				else: #if user was already staring at screen before
					#If break_time_interval passed
					if time.time() - screen_timer >= break_time_interval:
						#send class mode notification
						socketio.emit('study mode notification', {'data': 30})
						#wave_obj.play()
						playsound('sound1.mp3', True)
						#reset staring_screen flag
						staring_screen = False
			else: #if the user is not staring at the screen
				staring_screen = False
		#check if mode is class mode
		elif mode == 'Class':
			if message == "attention lost":
				if not attention_lost: #if attention lost for the first time
					screen_timer = time.time()
					attention_lost = True
				else: # if attention lost before
					if time.time()-screen_timer >= attention_lost_threshold:
						socketio.emit('class mode notification', {'data': 30})
						#wave_obj.play()
						playsound('sound1.mp3', True)
						attention_lost = False
			else: # user is looking at the screen
				attention_lost = False


def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock

	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame is None:
				continue

			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

			# ensure the frame was successfully encoded
			if not flag:
				continue

		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

# check to see if this is the main thread of execution
if __name__ == '__main__':
	# construct the argument parser and parse command line arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str, required=True,
		help="ip address of the device")
	ap.add_argument("-o", "--port", type=int, required=True,
		help="ephemeral port number of the server (1024 to 65535)")
	ap.add_argument("-f", "--frame-count", type=int, default=32,
		help="# of frames used to construct the background model")
	args = vars(ap.parse_args())

	# start a thread that will perform motion detection
	t = threading.Thread(target=head_pose, args=(
		args["frame_count"],))
	t.daemon = True
	now = time.time()
	t.start()

	# start the flask app
	# app.run(host=args["ip"], port=args["port"], debug=True,
	# 	threaded=True, use_reloader=False)
	socketio.run(app, host=args["ip"], port=args["port"], debug=True,
		use_reloader=False)



# release the video stream pointer
vs.stop()