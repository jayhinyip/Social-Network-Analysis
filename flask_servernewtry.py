from flask import Flask, render_template, request, redirect, url_for, g, session, send_from_directory
from os import path, walk
import os
import pandas as pd
import time
import pymysql
import numpy as np
from Rankstatement import rankstatement
from IDtoName import IDtoName

db = pymysql.connect(
    host = "localhost",
    user = "root",
    passwd= "root",
    database="testdatabase",
    cursorclass=pymysql.cursors.DictCursor,
autocommit = True)

cursor  = db.cursor()

nwdb = pymysql.connect(
    host = "localhost",
    user = "root",
    passwd= "root",
    database="NWdatabase",
autocommit = True)

nwcursor = nwdb.cursor()
# Assign the name of the application to 'app'
app = Flask(__name__)

# Key required for 'session'
app.secret_key = os.urandom(24)

#######################################################################
# Login
#######################################################################
@app.route('/',methods=['GET','POST'])
def login():

    # Output message if something goes wrong
    error = ''

    # If the user requests to log in (POST)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        # Replace 'user' with None to reset the session
        session.pop('user',None)

        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # Check if account exists in MySQL
        cursor.execute('SELECT * FROM pythonlogin.accounts WHERE username = %s AND password = %s', (username, password))
        #Fetch one record and return result
        account = cursor.fetchone()

        print(account)

        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True

            # The user session is for 'username'
            session['user'] = request.form['username']
            session['branch'] = account['Branch']

            # Redirect to homepage after succesful login
            return redirect(url_for('homepage'))

        else:

            # Error message if doesnt log in
            error = 'Invalid Credentials, Please Try Again'

    # Default render login.html
    return render_template('login.html',error=error)

#######################################################################
# Check Session
#######################################################################
@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

#######################################################################
# Homepage
#######################################################################
@app.route('/homepage')
def homepage():
    if g.user:
        username = session['user']

        #Replace underscores in branch name with spaces
        userbranch = session['branch']
        if "_" in userbranch:
            userbranch = userbranch.replace("_", " ")
        return render_template('homepage.html', branch = userbranch, name = username)
    return redirect(url_for('login'))
def lookupstatment(branch):
   return 'SELECT *FROM branchdatabase.' + str(branch)

#######################################################################
# My Profile
#######################################################################
@app.route('/project')
def profile():
    if g.user:

        #Replace underscores in branch name with spaces
        userbranch = session['branch']
        if "_" in userbranch:
            userbranch = userbranch.replace("_", " ")

        topcol = []
        topcol1 = []
        topcoljobs = []
        rankedlads = rankstatement(str(session['branch']), 'EigenvectorCent')
        for i in range(0,3):
            topcol.append(rankedlads[i][0])

        for x in range(len(topcol)):
            IDnamejob = IDtoName(topcol[x])
            fullname = IDnamejob[0]
            jobtitle = IDnamejob[1]
            topcol1.append(fullname)
            topcoljobs.append(jobtitle)


        knowbro = []
        knowbro1 = []
        knowbrojobs = []
        rankedlads = rankstatement(str(session['branch']), 'BetweenessCent')
        for i in range(0,3):
            knowbro.append(rankedlads[i][0])

        for x in range(len(knowbro)):
            IDnamejob = IDtoName(knowbro[x])
            fullname = IDnamejob[0]
            jobtitle = IDnamejob[1]
            knowbro1.append(fullname)
            knowbrojobs.append(jobtitle)

        isobro = []
        isobro1 = []
        isobrojobs = []
        rankedlads = rankstatement(str(session['branch']), 'CLoseCent')
        reversedlads = rankedlads[::-1]
        for i in range(0,3):
            isobro.append(reversedlads[i][0])

        for x in range(len(isobro)):
            IDnamejob = IDtoName(isobro[x])
            fullname = IDnamejob[0]
            jobtitle = IDnamejob[1]
            isobro1.append(fullname)
            isobrojobs.append(jobtitle)

        return render_template('project.html', branch = userbranch, topcol = topcol1, topcoljobs = topcoljobs, knowbro = knowbro1, knowbrojobs = knowbrojobs, isobro = isobro1, isobrojobs = isobrojobs)
    return redirect(url_for('login'))


#######################################################################
# Project Search
#######################################################################
@app.route('/search', methods=['GET','POST'])
def search():

    if request.method == "POST":
        branch = request.form['branch']

        #Check if branch exists in tabledatabase
        cursor.execute('SELECT table_name FROM information_schema.tables WHERE table_schema = \'branchdatabase\' AND TABLE_NAME = %s ', [branch])
        data = cursor.fetchall()

        branchfound = 1
        namedlist = []
        if len(data) == 1 and branchfound == 1:
            cursor.execute(lookupstatment(branch))
            data = cursor.fetchall()

            #Create list of employee names from their IDs
            employeelist = [d['TargetID'] for d in data]
            for i in range(len(employeelist)):
                IDnamejob = (IDtoName(employeelist[i]))
                fullname = IDnamejob[0]
                namedlist.append(fullname)
        else:
            branchfound = 0

        datalength = len(namedlist)


        return render_template('search.html', data = namedlist, datalen = datalength, branchfound = branchfound)
    return render_template('search.html')
    #return redirect(url_for('login'))

#######################################################################
# Interactive Map
#######################################################################
@app.route("/project_map")
def draw_graph():
        if g.user:
            # Replace underscores in branch name with spaces
            userbranch = session['branch']
            file_name = userbranch + '.gexf'

            return render_template('project_map.html', file_name = file_name)
        return redirect(url_for('login'))

#######################################################################
# Interactive Map 2
#######################################################################
@app.route("/project_map2")
def draw_graph2():
        if g.user:
            # Replace underscores in branch name with spaces
            userbranch = session['branch']
            file_name = userbranch + '.gexf'

            return render_template('project_map2.html', file_name = file_name)
        return redirect(url_for('login'))

#######################################################################
# FAQ, About and Contact Page
#######################################################################
@app.route('/<page>')
def details(page):
    if g.user:
        if page == 'about':
            message1 = 'About Us'
            message2 = 'This webpage is a search engine for each employee \
                        social connectivity. The properties of each employee \
                        are based on their email traffic within the company'
        elif page == 'FAQ':
            message1 = 'FAQ Section'
            message2 = 'This is the FAQ Section'
        elif page == 'contact':
            message1 = 'Contact Us'
            message2 = 'This is the contact page'
        return render_template('{}.html'.format(page),message1=message1,message2=message2)
    return redirect(url_for('login'))

#######################################################################
# Favicon identifyer
######################################################################
@app.route('/favicon.ico')
def favicon():
    # If asked of favicon, return icon favicon.ico
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

#######################################################################
# Debug and Initialisation
#######################################################################
if __name__ == '__main__':

    # Load the database
    #print('Loading Webserver...')

    # This is for debugging and searches for updated files whenever
    # the file is run. Auto refreshes the local server.
    extra_dirs = ['/static',]
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in walk(extra_dir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)
    app.run(extra_files=extra_files,debug=True)
