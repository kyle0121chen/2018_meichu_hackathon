import requests
import json
import datetime
import DAN.DAN as DAN
import IoT

'''
output_data={
	'on':None,
	'id':None,
	'location_school':None,
	'status_school':None,
	'object_school':None,
	'temperature':None,
	'number':None
	}
'''
#input_data={"responseId":"5158ae6c-1b7c-4923-8222-c3739f5e0af8","queryResult":{"queryText":"turn on the light","parameters":{"action_on-off":"On","object_311onoff":"Ceiling Light"},"allRequiredParamsPresent":True,"fulfillmentText":"test action is On and object is Ceiling Light","fulfillmentMessages":[{"text":{"text":["test action is On and object is Ceiling Light"]}}],"intent":{"name":"projects/hackathon-d7acf/agent/intents/c6d1e8d3-7dbf-4161-9833-1b73c4990f20","displayName":"On-Off-Control"},"intentDetectionConfidence":1,"languageCode":"en"},"originalDetectIntentRequest":{"payload":{}},"session":"projects/hackathon-d7acf/agent/sessions/857367ac-2676-f41b-fab8-0ffad0878914"}

output_data={
	'on':None,
	'id':None,
	'location_school':None,
	'status_school':None,
	'object_school':None,
	'temperature':None,
	'number':None
}

locat= [	
	"SecondRestaurant",
	"FirstRestaurant",
	"GirlsSecondRestuarant",
	"ED202",
	"MIRC311",
	"McD",
	"KFC",
	"BK"
]

def parse(input_data):
	global output_data
	try:
		if input_data['queryResult']['outputContexts'][0]['lifespanCount'] != None:
			return 1
	except:
		pass
	
	output_data.fromkeys(output_data,None)

	for i in range(len(input_data['queryResult']['parameters'].keys())):
		#print(i)
		if input_data['queryResult']['parameters'].keys()[i] == "object_311onoff":
			output_data['id'] = input_data['queryResult']['parameters']['object_311onoff']
		elif input_data['queryResult']['parameters'].keys()[i] == "action_on-off":
			output_data['on'] = input_data['queryResult']['parameters']['action_on-off']
		elif input_data['queryResult']['parameters'].keys()[i] == "location_school":
			output_data['location_school'] = input_data['queryResult']['parameters']['location_school']
		elif input_data['queryResult']['parameters'].keys()[i] == "status_school":
			output_data['status_school'] = input_data['queryResult']['parameters']['status_school']
		elif input_data['queryResult']['parameters'].keys()[i] == "object_school":
			output_data['object_school'] = input_data['queryResult']['parameters']['object_school']
		elif input_data['queryResult']['parameters'].keys()[i] == "number":
			output_data['number'] = input_data['queryResult']['parameters']['number']
		elif input_data['queryResult']['parameters'].keys()[i] == "temperature":
			output_data['temperature'] = input_data['queryResult']['parameters']['temperature']
	msg = SendParse(output_data)
	print(msg)
			

def SendParse(output_data):
	request_headers={
		"CK": "DKR95B0TT0XT2K5PF9",
		"Content-Type": "application/json"
	}
	if output_data['id'] != None and output_data['on']!= None:
		send_dict = {'id':output_data['id'], 'on':output_data['on']}
		DAN.push_data_to_IoTtalk(send_dict,"JsonReceiver")
		msg = "311 device OK!"
		responseMsg={
			'fulfillmentText':msg
		}
	elif output_data['object_school']!= None and output_data['temperature']!= None and output_data['location_school']!= None and output_data['number']!= None:
		send_dict= {'id': output_data['location_school']+"_"+output_data['object_school']+"_"+"controller"+"_"+str(output_data['number']), 'time':datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'), 'lat':"", 'lon':"", 'save': "true", 'value': [str(output_data['temperature']['amount'])]}
		test = [send_dict]
		print (test)
		r=requests.post('https://iot.cht.com.tw/iot/v1/device/10722883951/rawdata', data = json.dumps(test), headers = request_headers)
		if r.status_code == requests.codes.ok:
			msg= "Your %s has been set!" % output_data['object_school']
			responseMsg={
				'fulfillmentText':msg
			}
		else:
			msg = "Something Error!"
			responseMsg={
				'fulfillmentText':msg
			}	
		
	elif output_data['location_school']!=None and output_data['location_school']!="" and output_data['status_school']!=None:
		try:
			locatIndex=locat.index(output_data['location_school'])
			locatTemp=IoT.temperature(locatIndex)
			print locatTemp
			responseMsg={
				'fulfillmentText': "The Temperature of "+locat[locatIndex]+" is "+locatTemp+" degress"
			}
			print (responseMsg)
		except:
			print("It's not in Location List")	
			responseMsg={
				'fulfillmentText':"It's not in Location List"
			}

	else:
		responseMsg={
			"fulfillmentText": "Something Error, please try again"
		}
		print ("Error")
		
		
	return responseMsg


while True:
	parse(input_data)
