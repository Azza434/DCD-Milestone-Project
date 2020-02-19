import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'vehicle_log'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)


#-----------------------------Initial Webpage------------------------
@app.route('/')
@app.route('/get_data')
def get_data():
    return render_template("data.html", info=mongo.db.info.find())


#-----------------------------Add Info-------------------------------
@app.route('/add_info')
def add_info():
    return render_template('addinfo.html',
                           manufacturer=mongo.db.manufacturer.find())


#-----------------------------Insert Info----------------------------
@app.route('/insert_info', methods=['POST'])
def insert_info():
    info = mongo.db.info
    info.insert_one(request.form.to_dict())
    return redirect(url_for('get_data'))


#-----------------------------Edit Info------------------------------
@app.route('/edit_info/<info_id>')
def edit_info(info_id):
    the_info = mongo.db.info.find_one({"_id": ObjectId(info_id)})
    all_manufacturer = mongo.db.manufacturer.find()
    return render_template('editinfo.html', info=the_info,
                           manufacturer=all_manufacturer)


#-----------------------------Update Info----------------------------
@app.route('/update_info/<info_id>', methods=["POST"])
def update_info(info_id):
    info = mongo.db.info
    info.update({'_id': ObjectId(info_id)},
                {
        'manufacturer_name': request.form.get('manufacturer_name'),
        'vehicle_model': request.form.get('vehicle_model'),
        'vehicle_hp': request.form.get('vehicle_hp'),
        'vehicle_year': request.form.get('vehicle_year'),
        'engine_size': request.form.get('engine_size'),
        'reg_number': request.form.get('reg_number')
    })
    return redirect(url_for('get_data'))


#-----------------------------Delete Info---------------------------
@app.route('/delete_info/<info_id>')
def delete_info(info_id):
    mongo.db.info.remove({'_id': ObjectId(info_id)})
    return redirect(url_for('get_data'))


#-----------------------------Get Manufacturer----------------------
@app.route('/get_manufacturer')
def get_manufacturer():
    return render_template('manufacturer.html',
                           manufacturer=mongo.db.manufacturer.find())


#-----------------------------Edit Manufacturer---------------------
@app.route('/edit_manufacturer/<manufacturer_id>')
def edit_manufacturer(manufacturer_id):
    return render_template('editmanufacturer.html',
                           manufacturer=mongo.db.manufacturer.find_one(
                               {'_id': ObjectId(manufacturer_id)}))


#-----------------------------Update Manufacturer-------------------
@app.route('/update_manufacturer/<manufacturer_id>', methods=['POST'])
def update_manufacturer(manufacturer_id):
    mongo.db.manufacturer.update(
        {'_id': ObjectId(manufacturer_id)},
        {'manufacturer_name': request.form.get('manufacturer_name')})
    return redirect(url_for('get_manufacturer'))


#-----------------------------Delete Manufacturer-------------------
@app.route('/delete_manufacturer/<manufacturer_id>')
def delete_manufacturer(manufacturer_id):
    mongo.db.manufacturer.remove({'_id': ObjectId(manufacturer_id)})
    return redirect(url_for('get_manufacturer'))


#-----------------------------Insert Manufacturer-------------------
@app.route('/insert_manufacturer', methods=['POST'])
def insert_manufacturer():
    manufacturer_doc = {
        'manufacturer_name': request.form.get('manufacturer_name')}
    mongo.db.manufacturer.insert_one(manufacturer_doc)
    return redirect(url_for('get_manufacturer'))


#-----------------------------Add Manufacturer----------------------
@app.route('/add_manufacturer')
def add_manufacturer():
    return render_template('addmanufacturer.html')


app.run(host=os.getenv("IP", "0.0.0.0"),
        port=(os.getenv("PORT", "5000")), debug=True)
