from math import trunc

import pandas as pd
from flask import Flask, request, render_template
from sklearn.neighbors import NearestNeighbors
import random

app = Flask(__name__)
knn_model=NearestNeighbors(metric='cosine',algorithm='brute')
dataset = pd.read_csv('dataset1.csv')
x = dataset[['Exam (JEE/MHT- CET)', 'Type', 'Seat Type', 'score']]
m = dataset['Course Name']
score_m=dataset['score']
institue_name=dataset['Institute']

from sklearn.preprocessing import LabelEncoder
for i in range(len(x.columns)):
        if(type(x.iloc[1,i])==str):
            x.iloc[:,i]=LabelEncoder().fit_transform(x.iloc[:,i])
    #creating a dictionary for the form input
knn_model = knn_model.fit(x, m)

@app.route('/')
def home():
    dataset = pd.read_csv('dataset1.csv')
    datas=dataset.columns
    y = dataset['Course Name']

    x=dataset[['Exam (JEE/MHT- CET)', 'Type', 'Seat Type', 'score']]
    exam_type=pd.unique(x['Exam (JEE/MHT- CET)'])
    type=pd.unique(x['Type'])
    seat_type = pd.unique(x['Seat Type'])
    course_name=pd.unique(y)
    score=x['score'].name



    return render_template('index.html',exam=exam_type,exa_len=len(exam_type),type=type,
                           ltype=len(type),seat_type=seat_type,lseat_type=len(seat_type),course_name=course_name,lcourse=len(course_name),
                           score=score)


@app.route('/predict', methods=['POST'])
def predict():
    result = request.form
    #creating a copy of non-encoded x
    no_encode=dataset[['Exam (JEE/MHT- CET)', 'Type', 'Seat Type', 'score']]
    y = {}
    for key, value in request.form.items():
        y[key] = value

    d=pd.DataFrame([y])
    #removing the course name column from the dataframe
    t_course_name=d['Course Name']
    d=d.drop(columns=['Course Name'])
    t=pd.DataFrame([y])
    #def
    for i in range(len(d.columns)):
        # d = d.drop(columns=['Course Name'])
        k = d.iloc[0, i]

        c = d.iloc[:, i].name
        #print(k, c)
        typ = type(no_encode[d.iloc[:, i].name][0])
        #print(typ)

        if (typ == str):
            g = no_encode[no_encode[c] == k].index
            #print("this is ", g)
            if (len(g) > 1):
                g = g[1]
            else:
                g = g
            j = x[c][g]
            j=int(j)
            d[c] = j
            #print(j)
            #print(d[c])
        else:
            k=int(k)
            d[c]=k


    d[c]=int(d[c])
    #if(d['score']>=15):

    #print(d.columns)
    #if(d['Exam (JEE/MHT- CET)'][0]=='JEE'):
    jam=x.groupby('Exam (JEE/MHT- CET)')
    jam=jam.get_group(d['Exam (JEE/MHT- CET)'][0])
    sam=jam['score']
    sam=min(sam)
    #sam=min(x['score'])
    tame = jam[jam['score'] <= d['score'][0]].index
    tame=jam['score'][tame].sort_values(ascending=True).index
    kak=tame

    if (d['score'].values > 15):
        bg=1
        if(len(tame) > 1):
            k="yes it is"
            tame=tame[len(tame)-1]
        else:
            tame = min(jam['score'])
            tame = jam[jam['score'] == tame].index
            #tame = jam['score'][tame].sort_values(ascending=True).index
            #tame1=min(jam['score'][tame])
            #print('this is min',min(jam['score'][tame]))
            #tame=jam[jam['score'] ==tame].index
    else:
        bg=0
        tame=1116
        ''''
        if (d['Exam (JEE/MHT- CET)'].values == 'JEE'):
            sam = min(jam['score'])
            tame = jam[jam['score'] == sam].index

            if(len(tame)>1):
                tame = tame[len(tame)-1]
            else:
                sam = min(jam['score'])
                tame = jam[jam['score'] == sam].index
                
        if(d['Exam (JEE/MHT- CET)'][0]=="CET"):
            if (len(tame) > 1):
                tame = tame[len(tame) - 1]
                '''


    distance, indices = knn_model.kneighbors(x.iloc[tame].values.reshape(1, -1), n_neighbors=15)
    dist = distance.flatten()
    indi = indices.flatten()
    #print("the scores are ",d['score'].values)
    print(m)
    v = {}
    insti = {}
    socrei = {}
    course_df = pd.DataFrame()
    insti_df = pd.DataFrame()
    score_df = pd.DataFrame()
    for i in range(len(indices.flatten())):
        q = indices.flatten()[i]
        #print(q)
        v = m[q]
        scorei = score_m[q]
        import math
        print(" ",(dist.flatten()[i]))
        #print('the accuraccy is :')
       # print(scorei)
        q = indi.flatten()[i]
        #print(q)

        insti = institue_name[q]

        #print(v)
        course_df = course_df.append([v], ignore_index=True)

        insti_df = insti_df.append([insti], ignore_index=True)

        score_df = score_df.append([scorei], ignore_index=True)
        for i in range(len(course_df)):
            if (t_course_name[0] == course_df.iloc[i][0]):
                course_available = 1
                break
            else:
                course_available = 0


    else:
        bg=0

    #if(d['Exam (JEE/MHT- CET)'][0]=='JEE'):

    #print(tame)







    #print(course_df)
    print(insti_df)



    if(d['score'].values>15):
        bg=1
    else:
        bg=0
    if (((d['score'][0] > 200) and (t['Exam (JEE/MHT- CET)'][0] == "CET")) or (
            ((d['score'].values > 300) and (t['Exam (JEE/MHT- CET)'][0] == "JEE")))):
        invalid_score = 1
    else:
        invalid_score = 0

    return render_template('result.html', result=result,d=d,len=len(d.columns),g=g,k=k,j=j,t=t,typ=typ,f=d.iloc[:,3].name,
                           dist=dist,indi=indi,t1=t_course_name,lenindi=len(indi),course_df=course_df.iloc,
                           course_available=course_available,insti_df=insti_df.iloc,len_insit=len(insti_df),score_df=score_df.iloc,bg=bg,
                           dim=d.values.reshape(1,-1),score=score_df,tame=tame,d_score=d['score'].values,sam=sam,invalid_score=invalid_score)



if __name__=="__main__":
    app.run(debug=True)
