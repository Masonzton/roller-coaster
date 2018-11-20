from flask import Flask, render_template, request, make_response
import json
import barcode
import random
import base64
from io import StringIO

#function to generate bar codes for tickets
def new_bar():
    num = random.randrange(1,10**13)
    EAN = barcode.get_barcode_class('ean')
    ean = EAN(u'{}'.format(num))
    file = open('static/images/test.svg','wb')
    ean.write(file)
    file.close()
    file = open('static/images/test.svg','r')
    return file.read(), num

def get_avaliable(time):
    avaliable={}
    for i,j in time.items():
        for x,y in j.items():
            if len(y) < 5:  #5 can be substituted for general max slot limit
                avaliable[i+x] = 'avaliable'
            else:
                avaliable[i+x] = 'Unavaliable'
    return avaliable

app = Flask(__name__)

ride_names = {'r1':'Dominator','r2':'Volcano','r3':'Intimidator'}
times = {'t1':'10:00-15','t2':'10:15-30','t3':'10:30-45','t4':'10:45-11:00','t5':'11:00-15'}
#start each time slot off as empty
time_slots = {'r1':{'t1':[], 't2':[], 't3':[],'t4':[],'t5':[]},
'r2':{'t1':[], 't2':[], 't3':[],'t4':[],'t5':[]},
'r3':{'t1':[], 't2':[], 't3':[],'t4':[],'t5':[]}}


@app.route("/", methods=['get','post'])
def index():
    if request.method == 'POST':
        value = request.form.get('B1')
        x,y = tuple(value.split(';'))
        fill =len(time_slots[x][y])
        if fill < 5:
            barcode, num = new_bar()
            time_slots[x][y].append(num)
            #load to json file to be used by touchpoint scanner
            f = open('times.json','w')
            json.dump(time_slots,f)
            f.close()
            ride = ride_names[x]
            time = times[y]
            return render_template('after.html',barcode=barcode[142:],ride=ride,time=time)
        else:
            return 'sorry that time slot is full'
    if request.method == 'GET':
        return render_template('new.html',**get_avaliable(time_slots))

@app.route('/secret')
def secret():
    message = '''by the way this isn't how the actually website would work
    it makes it easier to see behind the scenes'''
    return str(time_slots) + message


if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8000') #port of 8000 was chosen to avoid
    #spam bots that ping common ports for service
