import pickle
import pandas as pd
from flask import Flask , request, render_template
app = Flask(__name__)
model = pickle.load(open("model1.pkl","rb"))
data = pd.read_csv('clean_data.csv')
profiles=pd.read_csv('profiles.csv')

tech='' #string
fot=''  #string
pt=''
hob=''  #string
mov=''
mus=''
l=[12]
''' #assigning values requested from webpage '''
# adding to dataset directly and accesing later
    

    
''' end '''



''' app routes '''

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login.html')
def login():
	return render_template('login.html')

@app.route('/signup.html')
def signup():
	return render_template('signup.html')

@app.route('/verification.html')
def verification():
	return render_template('verification.html')

@app.route('/interests.html')
def index1():
    return render_template('/interests.html')
    
@app.route('/profile.html')
def profile():
    return render_template('/profile.html')

@app.route('/eval',methods = ['GET','POST'])
def eval():
    if request.method=='POST':
        ind=request.form                  # returns an immutable dictionary
    print(ind)
    l.append(ind) 
    
    return render_template('fieldOfTech.html')


@app.route('/eval2',methods = ['GET','POST'])
def eval2():
    if request.method=='POST':
        fo=request.form    
    l.append(fo)            # returns an immutable dictionary
    ind=l[1]
    
    mus=ind['music']
    mov=ind['movie']
    hob=ind['finalValue']
    pt=ind['personalityType']
    
    fo=l[2]
    
    string=fo['finalBinaryForTech']  # string = x['finalBinaryForTech']
    
    f_list={'AE':[0,7],'CSE':[1,12],'ME':[2,5],'CIV':[3,6],'ECE':[4,6],'CME':[5,8]}
    
    s_fot=''
    s_t=''
    for i in f_list.keys():
        try:
            index = string.index(i)+len(i)
            s_fot+= string[index:f_list[i][1]+index]
            print(string[index:f_list[i][1]+index],len(string[index:f_list[i][1]+index]))
            s_t+='1'
        except:
            s_fot+='0'*f_list[i][1]
            s_t+='0'
    
    preds = [[float(mus),float(mov),float(hob),float(s_t),float(pt),float(s_fot)]]
    
    
    assigned_cluster = model.predict(preds)[0]
    
    temp={'music': preds[0][0],
     'movie': preds[0][1] ,
     'hobbies': preds[0][2] ,
     'techologies': preds[0][3] ,
     'personality_type': preds[0][4] ,
     'fields_of_tech': preds[0][5] ,
     'cluster': assigned_cluster }
    data.append(temp,ignore_index=True)
    
    # Shortlisting people of same cluster
    c = data[ data['cluster'] == assigned_cluster ]
    
    # Finding top 10 people with mutual attributes
    dic = dict(c.corrwith(data.iloc[-1], axis=1))
    
    sim_peop=sorted(dic.items(),\
    key=lambda item: item[1],reverse=True)[:10]
    
    # Getting details of people with mutual attributes
    peop_dets=[]
    for i in sim_peop:
        peop_dets.append(profiles.iloc[i[0]])
    print(peop_dets)
    
    return render_template('userpage.html',result=peop_dets)


@app.route('/connections.html')
def connections():
    
    
     return render_template('connections.html')

@app.route('/conversation.html')
def conversation():
    return render_template('conversation.html')

'''end app routes'''


if __name__ == '__main__':
    app.run(debug = False, port=33507)
