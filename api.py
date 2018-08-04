#!/usr/bin/env python
from lanbilling import LANBilling
from lanbilling.exceptions import LBAPIError
from flask import Flask
from flask import Response
import json

lbapi = LANBilling(manager='username', password='password', host='127.0.0.1', port=1502)

app = Flask(__name__)

keys = {
		"terminal1": "74234hfn2i378423uif2f34",
		"terminal2": "8932nfn39sama0948834892",
		"terminal3": "8809dh01083mckklaoisiak"
}

pay_classid = {"terminal1": 1, "terminal2": 2, "terminal3": 3}


@app.route('/check/terminal=<terminal_name>&authkey=<terminal_key>&uid=<userid>')
def check(terminal_name, terminal_key, userid):
	try:
		if terminal_key == keys[terminal_name]:
			try:
				resp_list = {"name": lbapi.getAgreements({'uid': int(userid)})[0]['user_name']}
				agrm_list = []
				for agreement in lbapi.getAgreements({'uid': int(userid)}):
					agrm_list.append({"agrm_name": agreement['agrm_num'], "agrm_id": agreement['agrm_id']})
				resp_list['agreements'] = agrm_list
				return Response(json.dumps(resp_list), status=200, mimetype='application/json')
			except IndexError as ieerr:
				if 'list index out of range' in str(ieerr):
					return Response(json.dumps({
						"error": 4,
						"error_message": "UID is invalid"
					}), status=404, mimetype='application/json')
			except ValueError:
				return Response(json.dumps({
					"error": 3,
					"error_message": "UID type should be number"
				}), status=403, mimetype='application/json')
		else:
			return Response(json.dumps({
				"error": 2,
				"error_message": "Authkey is invalid"
			}), status=403, mimetype='application/json')
	except KeyError as keeer:
		if terminal_name in keeer:
			return Response(json.dumps({
				"error": 1,
				"error_message": '{}{}{} is invalid terminal name'.format('\'', terminal_name, '\'')
			}), status=404, mimetype='application/json')

		
@app.route('/payment/terminal=<terminal_name>&authkey=<terminal_key>&agrm_id=<int:agreement_id>&amount=<amount_val>&receipt=<receipt_num>')
def payment(terminal_name, terminal_key, agreement_id, receipt_num, amount_val):
	try:
		if terminal_key == keys[terminal_name]:
			try:
				return Response(json.dumps({
					"record_id": (lbapi.Payment({
						'agrm_id': agreement_id,
						'receipt': receipt_num,
						'amount': float(amount_val),
						'class_id': pay_classid[terminal_name]
					}))}), status=200, mimetype='application/json')
			except LBAPIError as lberr:
				if 'Rate of default currency is not set' in str(lberr):
					return Response(json.dumps({
						"error": 3,
						"error_message": "agrm_id is invalid"
					}), status=404, mimetype='application/json')
				elif 'already used' in str(lberr):
					return Response(json.dumps({
						"error": 5,
						"error_message": "Receipt " + receipt_num + " already used"
					}), status=403, mimetype='application/json')
			except ValueError:
					return Response(json.dumps({
						"error": 4,
						"error_message": "amount type should be number"
					}), status=403, mimetype='application/json')
		else:
			return Response(json.dumps({
				"error": 2,
				"error_message": "Authkey is invalid"
			}), status=403, mimetype='application/json')
	except KeyError as keeer:
		if terminal_name in keeer:
			return Response(json.dumps({
				"error": 1,
				"error_message": '{}{}{} is invalid terminal name'.format('\'', terminal_name, '\'')
			}), status=404, mimetype='application/json')


@app.route('/status/terminal=<terminal_name>&authkey=<terminal_key>&record_id=<record_id_num>')
def status(terminal_name, terminal_key, record_id_num):
	try:
		if terminal_key == keys[terminal_name]:
			try:
				record_info = lbapi.getPayments({'record_id': int(record_id_num)})[0]
				if terminal_name == record_info['class_name'].lower():
					return Response(json.dumps({
						"uid": record_info['uid'],
						"agrm_id": record_info['agrm_id'],
						"amount": record_info['amount'],
						"receipt": record_info['receipt'],
						"terminal": record_info['class_name'],
						"pay_date": record_info['pay_date'],
						"timestamp": record_info['timestamp']
					}), status=200, mimetype='application/json')
				else:
					return Response(json.dumps({
						"error": 5,
						"error_message": "Payment was not created by {}{}{}".format('\'', terminal_name, '\'')
					}), status=403, mimetype='application/json')
			except IndexError as ieerr:
				if 'list index out of range' in str(ieerr):
					return Response(json.dumps({
						"error": 4,
						"error_message": "record_id is invalid"
					}), status=404, mimetype='application/json')
			except ValueError:
				return Response(json.dumps({
					"error": 3,
					"error_message": "record_id type should be number"
				}), status=403, mimetype='application/json')
		else:
			return Response(json.dumps({
				"error": 2,
				"error_message": "Authkey is invalid"
			}), status=403, mimetype='application/json')
	except KeyError as keeer:
		if terminal_name in keeer:
			return Response(json.dumps({
				"error": 1,
				"error_message": '{}{}{} is invalid terminal name'.format('\'', terminal_name, '\'')
			}), status=404, mimetype='application/json')


if __name__ == "__main__":
	app.run()
