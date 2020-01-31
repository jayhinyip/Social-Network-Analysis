from flask import Flask, render_template, request
from os import path, walk
import pandas as pd
import time

from evenness import evenness
from successionPlanner import successionPlanner
from makeNetwork import makeNetwork
from impactRecommender import impactRecommender
from highCostIdentifier import highCostIdentifier
from hiPoIdentifier import Responsiveness

app = Flask(__name__,static_url_path='/static')
#@app.route('/local_dashboard/', methods=['post', 'get'])
@app.route('/', defaults={'page': 'local_dashboard'})
@app.route('/<page>',methods=['GET','POST'])


def html_lookup(page):
    name = ''
    message = ''
    message2 = ''
    message4 = ''
    message5 = ''
    message3 = ''


    # Some browsers ask for favicon.ico, so redirect to local dashboard
    if(page == 'favicon.ico'):
        page = 'local_dashboard'

    if(page == 'local_dashboard'):

        # What the search box should say, return for all type of requests
        welcome_message = "Enter Employee Name"

        # If POST request (a user search)
        if request.method == 'POST':

            # Store the ID as a string
            ID = request.form.get('Input')
            name = str(ID)

            # Check that this is a valid ID
            for i in range(len(ID_list)):
                if str(ID) == str(ID_list[i]):

                    # Make a network graph for the user in a local context
                    (G, labels, edgeThicc,n_nodes) = makeNetwork(str(ID), 'Local', data)

                    # Number of candidates to find
                    candidates = 4

                    # Find the responsiveness and store in  a string
                    response = Responsiveness(str(ID),2,data)
                    message5 = str(response)

                    # Find the potential sucessors for the employee
                    (succCandidates, succLabels) = successionPlanner(str(ID), data, candidates)
                    succString = '• '
                    for b in range(candidates-1):
                        if(b>0):
                            succString = succString + '\n• ' + succCandidates[b][0]
                        else:
                            succString = succString + succCandidates[b][0]

                    message2 = succString

                    # Evenness and store as a string to be passed to the webpage
                    even = evenness(str(ID), data)
                    message = str(even)

                    # Number of connections to find
                    connections = 4

                    # Find the (connections) high impact individuals
                    middleMen = impactRecommender(str(ID),G,data,connections)

                    # Store these into a string with dot points
                    message4 = ''
                    if(middleMen == 'invalid'):
                        message4 = 'This is already a high impact individual'
                    else:
                        for b in range(len(middleMen)):
                            if(b>0):
                                message4 = message4+ '\n• ' + middleMen[b]
                            else:
                                message4 = '• ' + middleMen[b]

    # The global_dashboard function works the same as the local above
    # The context vaue is changed, generating a larger scope

    elif(page == 'global_dashboard'):
        welcome_message = 'Enter Employee Name'
        if request.method == 'POST':
            userInput = request.form.get('Input')
            ID = userInput
            name = str(userInput)

            for i in range(len(ID_list)):

                if str(ID) == str(ID_list[i]):
                    response = Responsiveness(str(ID),2,data)
                    message5 = str(response);
                    (G, labels, edgeThicc,n_nodes) = makeNetwork(str(ID), 'Global', data)
                    message2 = 'Active Connections: ' + str(n_nodes)
                    even = evenness(str(ID), data)
                    message = str(even)
                    name = str(ID)
                    connections = 4
                    highCostList = highCostIdentifier(G, connections)

                    middleMen = impactRecommender(str(ID),G,data,connections)
                    if(middleMen == 'invalid'):
                        message4 = 'This is already a high impact individual'
                    else:
                        for b in range(len(middleMen)):
                            if(b>0):
                                message4 = message4+ '\n• ' + middleMen[b]
                            else:
                                message4 = '• ' + middleMen[b]

                    for b in range(connections):
                        if(b>0):
                            message2 = message2 + '\n• ' + highCostList[b][0]
                        else:
                            message2 = '• ' + highCostList[b][0]



    elif(page == 'city_dashboard'):
        welcome_message = 'Enter City Name'

        # If a search has been inputted
        if request.method == 'POST':

            userInput = request.form.get('Input')

            context = 'SendersCity'
            name = str(userInput)

            ID = userInput

            # Look for a user in this city that cna be used for looking up
            # and generating a network Graph

            for i in range(len(data)):
                if(data['SendersCity'][i] == name):
                    ID = data['Sender'][i]
                    break

            # Search for this user and repeat the process from local.
            for i in range(len(ID_list)):
                name = str(ID)
                even = 20
                (G, labels, edgeThicc,n_nodes) = makeNetwork(str(ID), context, data)
                message = str(n_nodes)
                connections = 4
                highCostList = highCostIdentifier(G, connections)
                middleMen = impactRecommender(str(ID),G,data,connections)
                if(middleMen == 'invalid'):
                    message4 = 'This is already a high impact individual'
                else:
                    for b in range(len(middleMen)):
                        if(b>0):
                            message4 = message4+ '\n• ' + middleMen[b]
                        else:
                            message4 = '• ' + middleMen[b]

                for b in range(len(highCostList)):
                    if(b>0):
                        #if exists
                        message3 = message3 + '\n• ' + highCostList[b][0]
                    else:
                        message3 = '• ' + highCostList[b][0]
                break

    # department_dashboard works in the same way as city, but with a
    # different scope.

    elif(page == 'department_dashboard'):
        welcome_message = 'Enter Department Name'
        if request.method == 'POST':
            userInput = request.form.get('Input')
            name = str(userInput)
            for i in range(len(data)):
                if(data['SendersDepartment'][i] == name):
                    ID = data['Sender'][i]
                    break
            context = 'SendersDepartment'



            for i in range(len(ID_list)):
                name = str(ID)
                even = 20
                (G, labels, edgeThicc,n_nodes) = makeNetwork(str(ID), context, data)
                message = str(n_nodes)
                connections = 4
                highCostList = highCostIdentifier(G, connections)
                middleMen = impactRecommender(str(ID),G,data,connections)
                if(middleMen == 'invalid'):
                    message4 = 'This is already a high impact individual'
                else:
                    for b in range(len(middleMen)):
                        if(b>0):
                            message4 = message4+ '\n• ' + middleMen[b]
                        else:
                            message4 = '• ' + middleMen[b]

                for b in range(len(highCostList)):
                    if(b>0):
                        message3 = message3 + '\n• ' + highCostList[b][0]
                    else:
                        message3 = '• ' + highCostList[b][0]
                break

    # office_dashboard works the same as city, but in a different scope.
    elif(page == 'office_dashboard'):
        welcome_message = 'Enter Office Name'

        if request.method == 'POST':

            context = 'SendersOffice'
            userInput = request.form.get('Input')
            name = str(userInput)

            for i in range(len(data)):
                if(data['SendersOffice'][i] == name):
                    ID = data['Sender'][i]
                    break

            for i in range(len(ID_list)):
                name = str(ID)
                even = 20
                (G, labels, edgeThicc,n_nodes) = makeNetwork(str(ID), context, data)
                message = str(n_nodes)
                connections = 4
                highCostList = highCostIdentifier(G, connections)
                middleMen = impactRecommender(str(ID),G,data,connections)
                if(middleMen == 'invalid'):
                    message4 = 'This is already a high impact individual'
                else:
                    for b in range(len(middleMen)):
                        if(b>0):
                            message4 = message4+ '\n• ' + middleMen[b]
                        else:
                            message4 = '• ' + middleMen[b]

                for b in range(len(highCostList)):
                    if(b>0):

                        message3 = message3 + '\n• ' + highCostList[b][0]
                    else:
                        message3 = '• ' + highCostList[b][0]
                break

    # Render the webpage with the required information.
    return render_template('{}.html'.format(page),welcome_message=welcome_message,name=name,message = message,message3=message3,message2=message2,message4=message4,message5=message5)


if __name__ == '__main__':

    # Load the database
    print('Loading Database...')
    data = pd.read_excel('SNA_DATA.xlsx')
    senderlist = data['Sender'].unique().tolist()
    recipientlist = data['Recipient'].unique().tolist()

    # Create a full list of all the unique IDs in the data set
    uniqueRecipientList = [n for n in recipientlist if n not in senderlist]
    ID_list = senderlist + uniqueRecipientList

    # This is for debugging and searches for updated files whenever
    # the file is run. 
    extra_dirs = ['/static',]
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in walk(extra_dir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)
    app.run(extra_files=extra_files,debug=True)
