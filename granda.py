import requests
import csv
import json
import numpy as np
from datetime import datetime

access_token = open("MGAuth.txt", mode="r").read()
Dashur_token = open("../token.txt", mode="r",newline='').read()
startTime = '2020-05-05T06:40:00Z'
megaAccountId = [164573067,164565681,164565298,164565860,164565556,164565465,164565783]
MegaList = []
header = []
csvrow = []

now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
time = now.strftime("%H")



## 1. get LD unsuccessful tx

def LDTX(startTime):
    URL='https://api.bazred.net/LiveDealer/V1/Audit/product/15507/failedTransaction?startTime='+ startTime
    headers={'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + access_token}
    r = requests.get(URL, headers=headers)
    data = r.json()
    strData=str(data)
    with open("UnsuccessfulTX.txt", "w") as file:
        file.write(strData.replace('\'','\"'))



## check if it's client account
def isMegaAccount(accountid):
    URL='https://api.adminserv88.com/v1/account/' + accountid
    headers = {'Authorization': 'Bearer ' + Dashur_token, 'X-DAS-TZ': 'UTC', 'X-DAS-CURRENCY': 'USD',
                  'X-DAS-TX-ID': 'TEXT-TX-ID', 'X-DAS-LANG': 'en_GB', 'Content-Type': 'application/json'}
    r = requests.get(url=URL, headers=headers)
    res = r.json()
    data=res["data"]
    if data["parent_id"] in megaAccountId:
        return True

## 2. filter client's unsuccessful tx

def megaUnsuccessfulTx():
    with open("UnsuccessfulTX.txt", mode="r") as file:
        unsuccessful=json.load(file)
    for i in unsuccessful:
        x=i["userName"].split("_", 1)
        if isMegaAccount(x[0]) == True:
            print(i)
            MegaList.append(i)

def getAccountExtRef(accountid):
    URL = 'https://api.adminserv88.com/v1/account/' + str(accountid)
    headers = {'Authorization': 'Bearer ' + Dashur_token, 'X-DAS-TZ': 'UTC', 'X-DAS-CURRENCY': 'USD',
               'X-DAS-TX-ID': 'TEXT-TX-ID', 'X-DAS-LANG': 'en_GB', 'Content-Type': 'application/json'}
    r = requests.get(url=URL, headers=headers)
    res = r.json()
    data = res["data"]
    return data['ext_ref']


## get tx feed by ext_ref(一次查詢一筆)
def getTxFeed(server_id,game_id,action_id):
    url='https://api.adminserv88.com/v1/feed/transaction?external_ref='+ str(server_id) + '-' + str(game_id) + '-' + str(action_id)
    headers={"content-Type":"application/json",'X-DAS-TZ': 'UTC', 'X-DAS-CURRENCY': 'USD', 'X-DAS-TX-ID': 'TEXT-TX-ID', 'X-DAS-LANG': 'en_GB','Authorization': 'Bearer ' + Dashur_token}
    res = requests.get(url=url,headers=headers)
    r=res.json()
    return r

def megaUnsuccessAudit(userId,userTransNumber):
    ## define variables
    actionStatusID = []
    auditList = []
    feedList = []
    actionID = []
    subactionID = 0
    amount = 0
    totlaAmount = []
    totlaAmount.append(0)
    currentNum = 0
    description = []
    msg=[]
    outdata = []
    outdataPayout = 0
    ## params for audit
    totalPayoutAmount = 0
    totalWagerAmount = 0
    totalRefundAmount = 0

    ## params for Dashur
    totalDashurWager = 0
    totalDashurPayout = 0
    ticketstatus=[]
    MG_equals_Dashur_Wager = True
    MG_equals_Dashur_Payout = True

    # calling MG API
    url = 'https://api.bazred.net/LiveDealer/V1/Audit/product/15507/user/' + str(userId) + '/userTransNumber/' + str(userTransNumber)
    headers = {'Content-Type': 'application/x-www-form-urlencoded','Authorization': 'Bearer ' + access_token}
    r = requests.get(url, headers=headers)
    data = r.json()
    auditList.append(data)
    betDetails = data["betDetails"]

    ## make actionID Unique
    for i in betDetails:
        try:
            actionID.append(i["externalBalanceActionID"])
        except:
            pass

    UniqueActionId = np.unique(actionID)

    ## sum up amount in audit (totalWagerAmount & totalPayoutAmount)
    for x in betDetails:
        try:
            actionStatusID.append(x['actionStatusID'])
            if x['actionStatusID'] != 4:
                if x["externalBalanceActionID"] == subactionID:
                    amount = x["amount"] + amount
                    totlaAmount[currentNum] = amount
                    ticketstatus.append(x['ticketStatus'])
                    try:
                        msg.append(x['message'])
                    except:
                        ticketstatus.append(x['ticketStatus'])
                        pass
                elif x["externalBalanceActionID"] != subactionID:
                    subactionID = x["externalBalanceActionID"]
                    currentNum = currentNum + 1
                    amount = x["amount"]
                    totlaAmount.append(amount)
                    description.append(x["description"])
                    ticketstatus.append(x['ticketStatus'])
                    try:
                        msg.append(x['message'])
                    except:
                        pass
        except:
            outdata.append(x)
            pass
    for a in outdata:
        if a['description'] == 'Payout':
            outdataPayout = outdataPayout + a['amount']

    del totlaAmount[0]
    for i in range(len(description)):
        if description[i-1]=='Wager':
            totalWagerAmount = totalWagerAmount + totlaAmount[i-1]
        if description[i-1]=='Payout':
            totalPayoutAmount = totalPayoutAmount + totlaAmount[i-1]

    ## sum up amount in Tx feed

    for i in UniqueActionId:
        feedList.append(getTxFeed(15507, userTransNumber, i))
    time=[]
    for i in feedList:
        feedData=i["data"]
        for j in feedData:
            time.append(j['transaction_time'])
            if (j["category"] == 'WAGER'):
                totalDashurWager = totalDashurWager + j["amount"]
            if j["category"] == 'PAYOUT':
                totalDashurPayout = totalDashurPayout + j["amount"]
            if j["category"] == 'REFUND':
                totalRefundAmount = totalRefundAmount + j["amount"]

    totalWagerAmount = totalWagerAmount * 1000
    totalPayoutAmount = totalPayoutAmount * 1000


    if totalWagerAmount==totalDashurWager:
        MG_equals_Dashur_Wager = True
    else:
        MG_equals_Dashur_Wager = False

    if totalPayoutAmount==totalDashurPayout:
        MG_equals_Dashur_Payout=True
    else:
        MG_equals_Dashur_Payout = False

## append time
    if len(time) != 0:
        csvStartTime = str(time[0])
        csvrow.append(csvStartTime.replace(' ', 'T'))
    else:
        csvrow.append('')

## append actionOD
    csvrow.append(actionStatusID)

## append total amount
    if len(totlaAmount) != 0:
        csvrow.append(str(totlaAmount))
    else:
        csvrow.append('')
## append description
    if len(description) != 0:
        csvrow.append(str(description))
    else:
        csvrow.append('')
## append ticketstatus
    csvrow.append(ticketstatus)
    csvrow.append(outdataPayout)
    csvrow.append(str(totalWagerAmount))
    csvrow.append(str(totalPayoutAmount))
    csvrow.append(str(totalDashurWager))
    csvrow.append(str(totalDashurPayout))
    csvrow.append(str(totalRefundAmount))

    if totalDashurWager > totalWagerAmount:
        csvrow.append(str(totalDashurWager - totalWagerAmount))
    else:
        csvrow.append('')

    if totalPayoutAmount == 0:
        csvrow.append('')

    elif totalPayoutAmount == totalDashurPayout:
        csvrow.append('')
    else:
        csvrow.append('')
    csvrow.append(msg)

# 0.
# MG auth
# Dashur auth

with open('failed_endgame_0504_processed.csv',mode='r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    with open('Royal_' + year + month + day + 'T' + time + '.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['accountid','account_ext_ref', 'gameid','time', 'actionStatusID','amounts', 'descriptions', 'ticketStatus','outdataPayout','audit_wager', 'audit_payout',
             'txfeed_wager', 'txfeed_payout','txfeedRefund','wagerDiscrepency','payoutDiscrepency','message'])
        for i in csv_reader:
            csvrow.append(i[1])
            csvrow.append(i[0])
            csvrow.append(i[5])
            try:
                megaUnsuccessAudit(i[4], i[5])
                writer.writerow(csvrow)
                print(csvrow)
                csvrow.clear()
            except Exception as e:
                csvrow.append(f'An Error occurred: {e}')
                writer.writerow(csvrow)
                csvrow.clear()
                print(f'An Error occurred: {e}')

# # 1. 跑这支程式
# LDTX(startTime)
# megaUnsuccessfulTx()
# with open('Royal_'+year+month+day+'T'+time+'.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile, delimiter=',')
#     writer.writerow(['accountid','account_ext_ref', 'gameid','time', 'actionStatusID','amounts', 'descriptions', 'audit_wager', 'audit_payout',
#          'txfeed_wager', 'txfeed_payout','wagerDiscrepency','payoutDiscrepency','message'])
#     for i in MegaList:
#         for j in i["userTransNumber"]:
#             strUser=str(i['userName'])
#             accountid=strUser.split('_',1)
#             csvrow.append(accountid[0])
#             csvrow.append(getAccountExtRef(accountid[0]))
#             csvrow.append(j)
#             print(i['userName'],end=',')
#             print(j)
#             try:
#                 megaUnsuccessAudit(i["userId"], j)
#                 writer.writerow(csvrow)
#                 print(csvrow)
#                 csvrow.clear()
#             except Exception as e:
#                 csvrow.append(f'An Error occurred: {e}')
#                 writer.writerow(csvrow)
#                 csvrow.clear()
#                 print(f'An Error occurred: {e}')
