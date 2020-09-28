from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse, HttpRequest
from .functions.functions import handle_uploaded_file
from .forms import StudentForm
import requests
import psutil
import csv

# Create your views here.
def indexPage(request):
    testfile = pd.read_csv('test_new.csv')
    time_table = testfile[['click_time', 'click_id']].groupby('click_time').count().sort_values('click_time',ascending=True)
    time_table_index_list = time_table.index.to_list()
    time_table_values_list = time_table['click_id'].values.tolist()
    # PreT = testfile[testfile['predicted'] == 1]
    # preF = testfile[testfile['predicted'] == 0]
    totalc = testfile[testfile.columns[-2]].sum()
    seconds_minutes = [i[-4:] for i in time_table_index_list]

    '''
    response = requests.post('http://127.0.0.1:5000/predict', json={
    "click_id" : "0",
    "ip" : "5744",
    "app" : "9",
   "device" : "1",
    "os" : "3",
    "channel" : "107",
    "click_time" : "10-11-2017  04:00:00"})

    print(response.status_code)
    print(response.json())
    '''



    # stacked bar graph
    testfile2 = pd.read_csv('test_res.csv')

    testfile2['ip'] = testfile2['ip'].astype('category')
    df3 = testfile2.groupby(['ip', 'predicted']).size().unstack(fill_value=0)
    df3['counter'] = df3[1] + df3[0]

    df3 = df3.sort_values('counter', ascending=False).nlargest(10, 'counter')
    df3_0_list = df3[0].values.tolist()
    df3_1_list = df3[1].values.tolist()
    df3_label=df3.index.to_list()

    # stacked bar graph 2
    testfile_channel = pd.read_csv('test_res.csv')

    testfile_channel['channel'] = testfile_channel['channel'].astype('category')
    df5 = testfile_channel.groupby(['channel', 'predicted']).size().unstack(fill_value=0)
    df5['counter'] = df5[1] + df5[0]

    df5 = df5.sort_values('counter', ascending=False).nlargest(10, 'counter')
    df5_0_list = df5[0].values.tolist()
    df5_1_list = df5[1].values.tolist()
    df5_label = df5.index.to_list()


    #Bar Graph

    df4 = testfile2.groupby(['ip', 'device', 'predicted']).size().unstack(fill_value=0)
    df4['counter'] = df4.sum(axis=1)
    df4_suspicious = df4[df4[1] <= 1].sort_values('counter', ascending=False).nlargest(10, 'counter')
    df4_0_list = df4_suspicious['counter'].values.tolist()
    list_ip_device=df4_suspicious.index.tolist()
    new_list = []
    for i in list_ip_device:
        new_list.append(''.join(str(i)))


    #''''''''''''''''''''''''''''''''''''''
    csv = "test_new.csv"
    files = {'upload_file': open(csv, 'rb')}
    response=requests.post('http://127.0.0.1:5000/predict', files=files)
    response2 = requests.get('http://127.0.0.1:5000/usage')
    response3 = requests.get('http://127.0.0.1:5000/score')

    usage=response2.text[1:-2]
    score =response3.iter_lines()
    print(score)

    dataset = pd.read_json(response.json())
    dataset.to_csv('test_res.csv', index=False)
    #dataset.to_csv('fisrtUI/functions/test_res.csv', index=False)

    #..........................................

    cpu=psutil.cpu_percent()
    cpu_util=[cpu,100-cpu]
    memory=psutil.virtual_memory().percent
    memory_util=[memory,1-memory]


    # you can calculate percentage of available memory


    #.......................................



    testfile2 = pd.read_csv('test_res.csv')
    time_table2 = testfile2[['click_time', 'predicted']].groupby('click_time').sum().sort_values('click_time',
                                                                                               ascending=True)
    time_table_index_list2 = time_table2.index.to_list()
    time_table_values_list2 = time_table2['predicted'].values.tolist()
    totala = testfile2[testfile2['predicted'] == 1]
    totaln = testfile2[testfile2['predicted'] == 0]
    pied=[len(totala.index),len(totaln.index)]
    seconds_minutes2 = [i[-4:] for i in time_table_index_list2]

    vara=seconds_minutes
    varb=time_table_values_list
    varc=seconds_minutes2
    vard=time_table_values_list2


    context={'varb': varb, "vara":vara,"varc":varc,"vard":vard, 'usage':usage, 'pied':pied, 's0':df3_0_list, 's1':df3_1_list,
             'ip':df3_label, 'ip_device':new_list, 'ip_device_values':df4_0_list, 'c0':df5_0_list, 'c1':df5_1_list,
             'channel':df5_label, 'cpu_util':cpu_util, 'memory_util':memory_util, 'score':score}
    return render(request,'index.html',context)

#testfile=pd.read_csv('C:/Users/Rahul/PycharmProjects/djangoProject/Dashboard/test_new.csv')
#testfile=pd.read_csv('test_new.csv')
'''PreT=testfile[testfile['predicted']==1]
preF=testfile[testfile['predicted']==0]
grouped=testfile[testfile['predicted']==1]
#totalc=testfile[testfile.columns[-2]].sum()
print(PreT)
#print(testfile)'''

def index(request):
    if request.method == 'POST':
        student = StudentForm(request.POST, request.FILES)
        if student.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return indexPage(request)
    else:
        student = StudentForm()
        return render(request,"insert.html",{'form':student})


