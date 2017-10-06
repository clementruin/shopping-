from flask import Flask, render_template
import shopping

app = Flask(__name__)

#get my .csv to stay 1 second only in the browser cache
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
	app.run()


