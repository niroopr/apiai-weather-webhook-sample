#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

import suds
from suds.client import Client
from suds.sudsobject import asdict

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
#def webhook():
req = request.get_json(silent=True, force=True)
print("Request:")
print(json.dumps(req, indent=4))
res = processRequest(req)
res = json.dumps(res, indent=4)
# print(res)
r = make_response(res)
r.headers['Content-Type'] = 'application/json'
return r 
def processRequest(req):
    if req.get("result").get("action") != "finance.stocks":
        return {}
    url = 'http://nhclteas1.hclt.corp.hcl.in:8000/sap/bc/srt/wsdl/flv_10002A111AD1/srvc_url/sap/bc/srt/rfc/sap/zws_cb_chk_prod_stock_status/800/zws_cb_chk_prod_stock_status/zws_cb_bnd_stk_stat?sap-client=800'
    client = Client( url,username = 'COMM_USER', password = 'welcome')
    client.set_options(retxml=True)
    client.set_options(prettyxml=True)
    data = client.service.ZWS_CB_CHK_PROD_STOCK_STATUS(PLANT = "1000", PRODUCT="1300-520")
    res = makeWebhookResult(data)
    return res

def makeWebhookResult(data):
    
    #speech = data[225:232]+": "+data[233:241]+", "+data[252:257]+": "+data[258:262]+", "+data[
    #271:275]+": "+data[281:285]+", "+data[337:359]+": "+data[382:399]
    
    speech = "Niroop is a good guy"
    
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "niroop's webhook"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

