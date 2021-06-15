from flask import jsonify

def success(data, status_code = 200):
     return jsonify({
         "status":"success",
         "data":data
     }), status_code

def error(data, status_code=500):
     return jsonify({
         "status":"failure",
         "data":data
     }), status_code

