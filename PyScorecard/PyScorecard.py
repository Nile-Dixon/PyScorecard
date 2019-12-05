import requests
import csv

class PyScorecard:
	def __init__(self, api_key = None):
		self.api_key = api_key
		self.default_url = "https://api.data.gov/ed/collegescorecard/v1/schools"
		self.year = "latest"
		self.filters = []
		self.fields = []
		self.current_page = -1
		self.per_page = 20
		self.total_results = -1
		self.sort_by = None
		self.geofilter = {
			'zip_code' : None,
			'distance' : None
		}
	
	def set_api_key(self, api_key):
		'''
		This function sets the API key for the request.
		'''
		self.api_key = api_key

	def set_year(self, year):
		'''
		This function sets the year to filter data by.
		'''
		self.year = year
	
	def add_filter(self, field, operand = "=", values = []):
		'''
		This function allows you to add a filter you want to apply to a data request.
		'''
		if operand not in ['=','!=','>','<','..']:
			error_message = "This operand {} is not a valid operand. You must use '=', '!=', '>', '<', or '..'. ".format(operand)
			raise PyScorecardException(error_message)

		if (field not in ['id','ope6_id','ope8_id']) and (field[0:6] != "school") and (field[0:8] != "location"):
			field = "{}.{}".format(self.year, field)
		self.filters.append([field, operand, values])
	
	def add_field(self, field_name):
		'''
		This function allows you to add a field you want in the data request.
		'''
		if (field_name not in ['id','ope6_id','ope8_id']) and (field_name[0:6] != "school") and (field_name[0:8] != "location"):
			field_name = "{}.{}".format(self.year, field_name)
		self.fields.append(field_name)
	
	def add_fields(self, field_list):
		'''
		This function allows you to add multiple fields to a data request.
		'''
		for field_name in field_list:
			if (field_name not in ['id','ope6_id','ope8_id']) and (field_name[0:6] != "school") and (field_name[0:8] != "location"):
				field_name = "{}.{}".format(self.year, field_name)
			self.fields.append(field_name)

	def add_sort(self, field, order_by = "asc"):
		'''
		This function allows you to add a sort value to a data request.
		'''
		if field not in self.fields:
			error_message = "This field {} was not added. In order to sort, you must add the field using the add_field or add_fields method.".format(field)
			raise PyScorecardException(error_message)
		self.sort_by = "{}:{}".format(field, order_by)

	def add_geofilter(self, zip_code, distance, metric = "mi"):
		'''
		This function allows you to add a geo-filter to a data request.
		'''
		self.geofilter['zip_code'] = zip_code
		if distance != None:
			self.geofilter['distance'] = "{}{}".format(distance, metric)
	
	def fetch(self):
		'''
		This function allows you to fetch a specific row of data.
		'''
		if self.api_key == None:
			raise PyScorecardException("Missing API key. You can register for an API key at https://api.data.gov/signup/.")

		#Create the base url to make queries
		url = "{}?api_key={}".format(self.default_url, self.api_key)

		#Iterate through the filters and append them to the url
		for filter_param in self.filters:
			if filter_param[1] == "=":
				url += "&{}={}".format(filter_param[0], ",".join(filter_param[2]))
			elif filter_param[1] == ">":
				url += "&{}__range={}..".format(filter_param[0],filter_param[2][0])
			elif filter_param[1] == "<":
				url += "&{}__range=..{}".format(filter_param[0],filter_param[2][0])
			elif filter_param[1] == "..":
				url += "&{}__range={}..{}".format(filter_param[0],filter_param[2][0],filter_param[2][1])
			elif filter_param[1] == "!=":
				url += "&{}__not={}".format(filter_param[0], ",".join(filter_param[2]))

		#Iterate through field arguments and append them to the url
		if len(self.fields) >= 1:
			fields_arg = "&fields={}".format(",".join(self.fields))
			url += fields_arg

		#Set page parameter for url if self.current_page >= 0
		if self.current_page >= 0:
			url += "&page={}".format(self.current_page)

		#Set the per_page parameter for the url if the self.per_page != 20
		if self.per_page != 20:
			url += "&per_page={}".format(self.per_page)

		#Set the sort parameter for the url if the self.sort_by != None
		if self.sort_by != None:
			url += "&sort={}".format(self.sort_by)

		#Set the 
		if self.geofilter['zip_code'] != None:
			url += "&zip={}".format(self.geofilter['zip_code'])

		if self.geofilter['distance'] != None:
			url += "&distance={}".format(self.geofilter['distance'])

		#Make request to API
		resp = requests.get(url)
		data = resp.json()

		#Return errors to user if invalid search
		if 'errors' in data:
			error_message = "\n"
			for error in data['errors']:
				error_message += "{} \n".format(error['message'])
			
			raise PyScorecardException(error_message)

		#Set result values to metadata values
		if 'metadata' in data:
			self.current_page = int(data['metadata']['page'])
			self.total_results = int(data['metadata']['total'])
			self.per_page = int(data['metadata']['per_page'])

		return data['results']

	def fetch_all(self):
		'''
		This function allows you to fetch all data for a particular data request
		'''
		data = self.fetch()
		while self.has_next():
			self.current_page += 1
			data = data + self.fetch()

		return data
	
	def has_next(self):
		'''
		This function checks if there is another page that could be grabbed
		'''
		return self.per_page + self.current_page *  self.per_page < self.total_results

	def refresh(self):
		'''
		This function sets all properties to their default properties
		'''
		self.default_url = "https://api.data.gov/ed/collegescorecard/v1/schools"
		self.year = "latest"
		self.filters = []
		self.fields = []
		self.current_page = -1
		self.per_page = 20
		self.total_results = -1
		self.sort = None
		self.geofilter = {
			'zip_code' : None,
			'distance' : None
		}

	def export_csv(self, file_name = "data.csv"):
		'''
		This function fetches all results from a data request and exports it to a CSV file.
		'''
		data = self.fetch_all()

		headers = data[0].keys()

		with open(file_name, "w") as file_to_write:
			csv_to_write = csv.writer(file_to_write)
			csv_to_write.writerow(headers)
			for row in data:
				csv_to_write.writerow([row[header] for header in headers])
				


class PyScorecardException(Exception):
	def __init__(self, msg):
		super().__init__(msg)

