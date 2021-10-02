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

@app.route('/prediction1',methods = ['POST','GET'])
def prediction1():
    a = []
    try:
        if request.method == "POST":
            sex = int(request.form['sex'])
            age = int(request.form['age'])
            steroid = int(request.form['steroid'])
            fatigue = int(request.form['fatigue'])
            antivirals = int(request.form['antivirals'])
            alk_phosphate = int(request.form['alk_phosphate'])
            malaise = int(request.form['malaise'])
            liver_big = int(request.form['liver_big'])
            liver_firm = int(request.form['liver_firm'])
            anorexia = int(request.form['anorexia'])
            spiders = int(request.form['spiders'])
            ascites = int(request.form['ascites'])
            bilirubin = float(request.form['bilirubin'])
            histology = int(request.form['histology'])
            sgot = float(request.form['sgot'])
            albumin = int(request.form['albumin'])
            a.extend([age,sex,steroid,antivirals,fatigue,malaise,anorexia,liver_big,liver_firm,0,spiders,ascites,0,bilirubin,alk_phosphate,sgot,albumin,62,histology])
            model = joblib.load("SVCMODEL.pkl")
            y_pred = model.predict([a])
            return render_template('prediction.html',msg = "done",op=y_pred)
    except ValueError:
        return render_template('prediction.html')

    #return render_template("prediction.html")





if __name__ == '__main__':
    app.run(debug=True)


