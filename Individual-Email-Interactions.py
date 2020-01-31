import csv

#!/usr/bin/env python
# coding: utf-8

# This code gives:
#  - ID_list: the list of all the unique IDs in the data set.
#  - sendingAmountList: the number of emails sent by each ID.
#  - receivedAmountList: the number of emails received by each ID.
#  - recipientsPerSender: a list of lists of the recipients of each sender.
#  - uniqueRPS: A list of all the unique recipients from each sender.
#  - nemailslist: The number of emails sent to each recipient from each sender.
#  - responseratio: The ratio of emails sent to emails received.

# In[1]:


# Import all the usual hoes
import pandas as pd
import numpy as np


# In[2]:


# Read in the data and create a unique list of senders and recipients
data = pd.read_excel('SNA_DATA.xlsx')
senderlist = data['Sender'].unique().tolist()
recipientlist = data['Recipient'].unique().tolist()


# In[3]:


# Create a full list of all the unique IDs in the data set
uniqueRecipientList = [n for n in recipientlist if n not in senderlist]
ID_list = senderlist + uniqueRecipientList


# In[4]:


# Create a sender list to loop through
temp = list(data['Sender'])

# Create a list to store the send count of each ID
sendingAmountList = []

# Loop through each ID and initialise the sendcount
for ID in ID_list:
    count=0

    # For each sender in the data, add one to the count for each email
    for sender in temp:
        if sender==ID:
            count+=1
    sendingAmountList.append(count)


# In[5]:


# Now do the same thing for recipients
temp1 = list(data['Recipient'])
receivedAmountList = []

for ID in ID_list:
    count = 0

    for receiver in temp1:
        if receiver==ID:
            count+=1
    receivedAmountList.append(count)


# In[6]:


# Now we want to get the recipient IDs of each sender. This is going to be a bitch.
# Create a list to store the list of recipients for each sender.
recipientsPerSender = []
for ID in ID_list:

    # Create the list of recipients for this sender
    recipientThisSender = []

    for i in range(0,len(temp)):
        if ID==temp[i]:
            recipient = data.iloc[i,8]
            recipientThisSender.append(recipient)
    recipientsPerSender.append(recipientThisSender)


# In[7]:


# Initiate a list to store only the unique recipients of each senders emails
uniqueRPS = []

# Loop through each sender to find how many emails they've sent to a particular recipient
for sender in recipientsPerSender:

    uniqueSender = [ii for n,ii in enumerate(sender) if ii not in sender[:n]]
    uniqueRPS.append(uniqueSender)


# In[8]:


# Count how many times each recipient has received an email from each sender.
nemailslist = []
for sender in recipientsPerSender:

    nemails = {x:sender.count(x) for x in sender}
    nemailslist.append(nemails)


# In[9]:


# Now we're creating a metric for each person's responsiveness by taking a ratio of their emails sent to received
# Create a list to store the repsonse ratios
responseratio = []

# Loop through each person's number of emails sent
for i in sendingAmountList:

    # Calcualte the response ratio if the denominator isn't zero. If it is, put in 1000000 and deal with it later
    if receivedAmountList[i] != 0:
        response = sendingAmountList[i]/receivedAmountList[i]
        responseratio.append(response)
    else:
        responseratio.append(1000000)



bigList = [None]
bigList.append(ID_list)
bigList.append(sendingAmountList)
bigList.append(receivedAmountList)
bigList.append(recipientsPerSender)
bigList.append(uniqueRPS)
bigList.append(nemailslist)
bigList.append(responseratio)

with open("output.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(bigList)
