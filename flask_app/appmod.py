from flask import Flask, render_template,request,url_for
from flask_bootstrap import Bootstrap 
 # NLP Packages
from textblob import TextBlob,Word 
import random 
import time
import string
import re

import warnings
warnings.filterwarnings("ignore")

import pickle
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)
Bootstrap(app)
@app.route('/')
def index():
	return render_template('index.html')
@app.route('/analyse',methods=['POST'])

#Get the url and pull text
def analyse():
	start = time.time()
	if request.method == 'POST':
		url = request.form['rawtext']
		response = requests.get(url)
		html = response.text
		soup = BeautifulSoup(html, 'lxml')
	#Pull text from the url
		text=[]
		for n in soup.findAll('p', {"class": "description"}):
			text.append(n.text)

		for n in soup.findAll('div', {"class": "story-content"}):
			text.append(n.text)
		data = ' '.join(text)
	############################################
		# Loading the saved model pickle
		pipeline_mod_pkl = open('balanced_pipeline.pkl', 'rb')
		balance_pipline_model = pickle.load(pipeline_mod_pkl)
		main_cat=balance_pipline_model.predict([data])[0]
		cat_id='No Sub-Category'
		#Labels for home-loan clusters
		label_ref={0:'First-Home',
		           1:'Investment-Property',
		           2:'Repayment/Offset',
		           3:'Refinancing',
		           4:'Low/Fixed/Variable'}                                                                                     

		#Section for 2nd level within home-loans
		if main_cat=='home-loans':
			pipeline_mod_pkl = open('second_level_pipeline.pkl', 'rb')
			loan_cluster_model = pickle.load(pipeline_mod_pkl)
			#Predict the cluster for test-article
			cat_id =label_ref.get(loan_cluster_model.predict([data])[0])
		end = time.time()
		final_time = end-start
		return render_template('index.html',received_text = data,blob_sentiment=main_cat,second_cat=cat_id,final_time=final_time)

if __name__ == '__main__':
	app.run(debug=True)                                                                                                                                                                                                                                                                                                                                                                     