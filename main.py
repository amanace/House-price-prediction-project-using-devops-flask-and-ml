from flask import Flask, render_template,request
import numpy as np
import pickle

app= Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

def valuepred(data_list):
    if len(data_list) != 8:
        raise ValueError("Data list must have exactly 8 elements.")
    to_predict = np.array(data_list).reshape(1, 8)
    loaded_model = pickle.load(open("house_price.pkl", "rb"))
    result = loaded_model.predict(to_predict)
    return result

@app.route('/result',methods=['POST'])
def result():
    if request.method =='POST':
        data= request.form.to_dict()
        #print(data)
        data_list = list(data.values())
        data_list = list(map(int,data_list))
        #print(data_list)
        try:
            data_list = list(map(int, data_list))
        except ValueError:
            return render_template("result.html", data="Invalid input. Please enter numbers only.")

        # Check the length of data_list before proceeding
        if len(data_list) != 8:
            return render_template("result.html", data="Please provide exactly 8 values.")

        res = valuepred(data_list)

        return render_template("result.html" , data = res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)