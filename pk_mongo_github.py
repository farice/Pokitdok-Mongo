import sys
import csv 
import os
import zipfile 
import argparse
#Pokitdok API
import pokitdok
# REST & JSON
import json
import urllib.request
import requests
import jsonpickle
# DOB parsing
from datetime import datetime 
import dateparser
# mongoDB
from pymongo import MongoClient

class PokitDotConnector():
	
	def __init__(self):
		# initialize api connection -- replace token and secret with you authorized credentials
		self.pd = pokitdok.api.connect('[TOKEN]', '[SECRET]')


	def get_eligibility(self, num):
		# get vars from import_claims method
		self.import_claims(num)
		# api eligibility call -- replace /eligibility/ with different endpoint for other calls
		return self.pd.request('/eligibility/', method = 'post', data = {
			"member": {
				"birth_date": str(self.dob),
				"last_name": str(self.lname),
				"first_name": str(self.fname),
				"id": str(self.id)
			},
			"provider": {
				# add your credentials
				"organization_name": "[YOUR ORG]",
				"npi": "[YOUR ORG'S NPI"
			},
			"trading_partner_id": str(self.partner)
}		)

	# this is our mechanism of retrieving patient data for the API calls -- we have previously stored it in a MongoDB database
	# of course you may replace this function to import the data for the API call from wherever you have it stored
	def import_claims(self, num):
		#retrieve data from mongoDB db "Claim" -- adjust this to the name of your database where data is stored if importing from MongoDB
		client = MongoClient()
		db = client.Claim
		
		#store to vars
		cursor = db.claim_info.find()
		
		document = cursor[num]

		self.id = document["_id"]
		self.fname = document["First Name"]
		self.lname = document["Last Name"]
		dob = document["Patient DOB"]
		self.partner = document["Trading Partner"]
		dob = (dateparser.parse(dob))
		self.dob = dob.date()
	
	def export_sample(self, output_directory, num):
		# use elig mongodb database
		client = MongoClient()
		db = client.elig
		
		"""
		Export eligibility info to a CSV file
	
		:param output_directory: directory where eligibility data will be exported in a zip file
		"""
	
		if not os.path.exists(output_directory):
			os.makedirs(output_directory)
			
		response = self.get_eligibility(num)
		#serialize response as JSON
		db_entry = json.dumps(response.get('data'))
		#deserialize as python object
		db_entry = json.loads(db_entry)
		#add to elig collection in mongoDB
		stored = db.elig.insert(db_entry)
		#TODO: Fix (optional)
		#print(stored.inserted_id)
		
		#write to txt file (for testing purposes)
		
		#api_data_file = os.path.join(output_directory, 'elig.txt')
		#with open(api_data_file, 'w') as api_data_file:
		#	json.dump(response.get('data', {}), api_data_file, sort_keys = True, indent = 4)
			
def main(argv):
	def pokit_call():
		#connect to api
		pc = PokitDotConnector()
		#optional args
		parser = argparse.ArgumentParser(description= 'Export eligibility data')
		parser.add_argument('--output-dir', type=str, dest='output_directory', default = 'EligibilityData',
		help = 'eligibility data output directory (default: EligibilityData)' )
		args = parser.parse_args()
		# show progress in cmd
		print('Processing iteration number:')
		#run iteratively over specified range -- replace [n] with your contstraint of interest
		# print by skipping a line every 15 prints 
		for i in range(0 , [n]):
			pc.export_sample(args.output_directory, i)
			if (i % 15) != 0:  
				print('%d' % i, end = ' ')
			else:
				print(i)
	#run!		
	pokit_call()
	
if __name__ == "__main__":
	main(sys.argv)
 
