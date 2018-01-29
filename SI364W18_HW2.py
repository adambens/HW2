## SI 364
## Winter 2018
## HW 2 - Part 1
## Adam Benson

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import json
import requests


#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

#This is Part 2
class AlbumEntryForm(FlaskForm):
	albumName = StringField('Enter the name of an album:', validators=[Required()])
	albumRating = RadioField('How much do you like this album? (1 low, 3 high)', choices=[('1','1'),('2','2'),('3','3')], validators=[Required()])
	submit = SubmitField('Submit')


####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)


#Part 1

#Artist Form
@app.route('/artistform')
def artist_form():
    return render_template('artistform.html')

#Artist Links
@app.route('/artistlinks')
def artist_links():
    return render_template('artist_links.html')

#Artist Info
@app.route('/artistinfo')
def artist_info():
	params = dict()
	baseURL = "https://itunes.apple.com/search?"
	artist = request.args.get('artist',"")
	params = {'term': artist, 'entity' : 'musicTrack'}
	response = requests.get(baseURL, params = params)
	jsonResponse = json.loads(response.text)
	artistObject = jsonResponse['results']
	return render_template('artist_info.html', artist=artist, objects=artistObject)


#Specific Artist
@app.route('/specific/song/<artist_name>', methods = ['GET', 'POST'])
def specific_artist(artist_name):
	params = dict()
	baseURL = "https://itunes.apple.com/search?"
	params = {'term': artist_name, 'entity' : 'musicTrack'}
	response = requests.get(baseURL, params = params).json()['results']
	return render_template('specific_artist.html', results = response)


###########################################################################
## Part 2 #################################################################
###########################################################################

#Album Entry
@app.route('/album_entry', methods = ['GET', 'POST'])
def album_entry():
    myForm = AlbumEntryForm()
    return render_template('album_entry.html',form=myForm)

#Album Result
@app.route('/album_result', methods= ['POST', 'GET'])
def album_result():
	name = request.args.get('albumName')
	rating = request.args.get('albumRating')
	results = [name, rating]
	return render_template('album_data.html', results= results)





if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
