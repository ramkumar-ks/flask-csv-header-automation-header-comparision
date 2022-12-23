from flask import Flask,render_template,request,redirect,url_for 
import pandas as pd
import boto3
import csv
import s3fs
app=Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
@app.route('/header_data', methods=['GET', 'POST'])
def data():
    if request.method=='POST':
        header_input=request.form.get('s3_csv_file')
        global header_len
        s3_header=[]
    if request.form['csv_submit_button']=='Get_CSV_Headers':
        df=pd.read_csv(header_input)
        header_list=list(df.columns.values)
        header_len=len(header_list)            
        for x in range(0,header_len):
            s3_header.append(header_list[x])   
        return render_template('index.html',s3_header=s3_header)
@app.route('/compare')
def compare():
    return render_template('compare.html')
@app.route('/compare_header', methods=['GET', 'POST'])
def compare_header():
    if request.method == 'POST':
        s3_header1=[]
        s3_header2=[]
        global header_len1
        global header_len2
        header_input1=request.form.get('s3_csv_file1')
        header_input2=request.form.get('s3_csv_file2')
        if request.form['csv_submit_button1']=='Compare_Headers':
            df=pd.read_csv(header_input1)
            header_list1=list(df.columns.values)
            header_len1=len(header_list1)
            for x in range(0,header_len1):
                s3_header1.append(header_list1[x])
            print(s3_header1)                       
            df=pd.read_csv(header_input2)
            header_list2=list(df.columns.values)
            header_len2=len(header_list2)
            for x in range(0,header_len2):
                s3_header2.append(header_list2[x])
            print(s3_header2)
            if(header_len1==header_len2):
                for x in range(0,header_len1):
                    if(s3_header1[x]==s3_header2[x]):
                        print(s3_header1[x],"=",s3_header2[x])
                        print("Headers Matched")
                    else:
                        print("Headers Not Matched")            
            return render_template('compare.html',s3_header1=s3_header1,s3_header2=s3_header2)

if __name__ == '__main__':
    app.run(debug=True)

