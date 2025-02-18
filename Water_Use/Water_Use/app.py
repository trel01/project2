from flask import Flask,request, url_for, redirect, render_template
import pickle
import numpy as np

app = Flask(__name__)

model=pickle.load(open("C:\AppServ\www\ML\Water_Management\Water_Use/model-30.pkl", 'rb') )##+

@app.route('/')
def hello_world():
    return render_template("Water_Use.html")


@app.route('/predict',methods=['POST','GET'])
def predict():
    int_features=[int(x) for x in request.form.values()]
    final=[np.array(int_features)]
    print(int_features)
    print(final)
    prediction=model.predict(final)
    #output='{0:.{1}f}'.format(prediction[0][1], 2)
    output=prediction

    # show the inputs and predicted outputs
    for i in range( len( final ) ):
        print( "X=%s, Predicted=%s" % (final[i], prediction[i]) )

    #return   render_template( 'Loan_status.html',
            #         pred=' {}'.format( output ),
           #          bhai="" )
    if output==0:
        return render_template('Water_Use.html',
                            word='ความเป็นไปได้สำหรับความเพียงพอของน้ำในชุมชน: ',
                            answer='ข้อมูลที่กรอก: ',
                            a0=int_features[0], a1=int_features[1], a2=int_features[2],
                            pred='มีน้ำใช้ไม่เพียงพอ'.format(prediction[0], 1).format(output),bhai="")
    else:
       return render_template('Water_Use.html',
                            word='ความเป็นไปได้สำหรับความเพียงพอของน้ำในชุมชน: ',
                            answer='ข้อมูลที่กรอก: ',
                            a0=int_features[0], a1=int_features[1], a2=int_features[2],
                            pred='มีน้ำใช้เพียงพอตลอดปี'.format(prediction[0], 1).format(output),bhai="")

 #elif output == 6:
  #      return render_template('forest_fire.html',
   #                            pred='detention, abduction.\nCommunity conflict problem {}'.format(prediction[0], 1)
    #                           .format(output), bhai="'")
if __name__ == '__main__':
    app.run(debug=True,port=5030)
