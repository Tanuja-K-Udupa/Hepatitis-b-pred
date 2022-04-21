from flask import Flask,render_template,request,session
import pandas as pd
from sklearn.model_selection import train_test_split

global x_train, x_test, y_train, y_test, acc1 , acc2 ,acc3,acc4,acc5,acc6
import joblib

app = Flask(__name__)

@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

@app.route('/Uploadfile', methods=['POST', 'GET'])
def upload1():
    if request.method == "POST":
        dataset = request.files['file']
        filename = dataset.filename
        file = "dataset\\" + filename
        session['dataset'] = file
        return render_template('upload.html', msg="success")
    return render_template('upload.html')

@app.route('/view')
def viewdata():
    datafile = session["dataset"]
    df = pd.read_csv(datafile)

    return render_template('viewdata.html',data=df.to_html())


@app.route('/splitdataset',methods=['POST','GET'])
def splitdataset():
    global x_train,x_test,y_train,y_test
    if request.method == 'POST':
        testsize = request.form['test_size']
        testsize = float(testsize)
        datafile = session.get('dataset')
        df = pd.read_csv(datafile)
        x = df.iloc[:,1:]
        y = df.iloc[:,0]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=testsize)

        lentr = len(x_train)
        lentes = len(x_test)
        return render_template('splitdata.html', msg1="done",tr1 =lentr,te1 = lentes)
    return render_template('splitdata.html')



@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

@app.route('/predict',methods = ['POST','GET'])
def prediction1():
    a = []
    try:
        if request.method == "POST":
            values = []
            name = request.form['name']
            values.append(name)
            sex = 1 if request.form['sex']=="Male" else 0
            values.append(request.form['sex'])
            age = int(request.form['age'])
            values.insert(1,age)
            steroid = 1 if request.form['steroid']=="High" else 0
            values.append(request.form['steroid'])
            fatigue = 1 if request.form['fatigue']=="High" else 0
            values.append(request.form['fatigue'])
            antivirals = 1 if request.form['antivirals']=="High" else 0
            values.append(request.form['antivirals'])
            alk_phosphate = float(request.form['alk_phosphate'])
            values.append(alk_phosphate)
            malaise = 1 if request.form['malaise']=="Yes" else 0
            values.append(request.form['malaise'])
            liver_big = 1 if request.form['liver_big']=="Yes" else 0
            values.append(request.form['liver_big'])
            liver_firm = 1 if liver_big==0 else 0
            anorexia = 1 if request.form['anorexia']=="Yes" else 0
            values.append(request.form['anorexia'])
            spiders = 1 if request.form['spiders']=="Yes" else 0
            values.append(request.form['spiders'])
            ascites = 1 if request.form['ascites']=="High" else 0
            values.append(request.form['ascites'])
            bilirubin = float(request.form['bilirubin'])
            values.append(bilirubin)
            histology = 1 if request.form['histology']=="Yes" else 0
            values.append(request.form['histology'])
            sgot = float(request.form['sgot'])
            values.append(sgot)
            albumin = float(request.form['albumin'])
            values.append(albumin)
            a.extend([age,sex,steroid,antivirals,fatigue,malaise,anorexia,liver_big,liver_firm,0,spiders,ascites,0,bilirubin,alk_phosphate,sgot,albumin,62,histology])
            model = joblib.load("SVCMODEL.pkl")
            y_pred = model.predict([a])
            values.append(y_pred[0])
            createFile(values)
            return render_template('prediction.html',msg = "done",op=y_pred,name=name,age=age,sex="Male" if sex==1 else "Female")
    except Exception:
        print("Error")
        return render_template('prediction.html')

def createFile(value):
    value.insert(0,"limegreen" if value[-1]==0 else "red")
    value.insert(4,"Healthy.png" if value[-1]==0 else "Infected.png")

    file = open('reportFormat.txt','r')
    data = "".join(file.readlines())
    data = data.split("{}")
    finalData = data[0]
    for i in range(1,len(data)):
        finalData += str(value[i-1])
        finalData += data[i]

    file = open("./templates/Report.html",'w')
    file.write(finalData)
    file.close()
    print(value)

if __name__ == '__main__':
    app.run(debug=True)
