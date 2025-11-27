
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, render_template, flash, send_from_directory, send_file
import time
import datetime
import sqlite3
import os
import math
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def gen_markup_edzo(search=False):
    keyboard = InlineKeyboardMarkup()
    if search:
        keyboard.add(InlineKeyboardButton('Скрыть меня из поиска', callback_data='deactivate'))
    keyboard.add(InlineKeyboardButton('Заполнить анкету заново', callback_data='start'))
    keyboard.add(InlineKeyboardButton('Моя информация', callback_data='my_info'))
    keyboard.add(InlineKeyboardButton('Мои спортсмены', callback_data='my_students'))
    return keyboard

def gen_markup(but_text, but_url):
    keyboard = InlineKeyboardMarkup()
    if not but_url:
        keyboard.add(InlineKeyboardButton(but_text, callback_data='check'))
    else:
        keyboard.add(InlineKeyboardButton(but_text, url=but_url))
    return keyboard

def my_factory(col,b):
    cols={}
    for i,name in enumerate(col.description):
        cols[name[0]]=b[i]
    return cols

TOKEN_EDZO = '5842386849:AAH2bNU6XS9u7VONZoI4gk7KMirf3oFYYGU'

IMG_PATH = "C:\\Users\\Aleks\\Desktop\\bot_gym\\IMG\\"

app = Flask(__name__)

app.config.update(dict(
    DATABASE_EDZO = os.path.join("C:\\Users\\Aleks\\Desktop\\bot_gym\\", 'main.db'),
    DEBUG = False,
    SECRET_KEY = 'development key',
    USERNAME = 'admin',
    PASSWORD = '123'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('edzo_login'))
    else:
        return redirect(url_for('coaches'))

@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory(IMG_PATH, filename)

@app.route('/coaches')
def coaches():
    if not session.get('edzo_logged_in'):
        return redirect(url_for('edzo_login'))
    conn = sqlite3.connect(app.config['DATABASE_EDZO'])
    conn.row_factory = my_factory
    cur = conn.cursor()
    cur.execute('SELECT * FROM coaches WHERE step == "" OR step IS NULL ORDER BY active_coach DESC, approve_coach')
    coaches = cur.fetchall()
##    for coach in coaches:
##        cur.execute('SELECT name FROM cities WHERE id = ?', [coach['city'], ])
##        data  = cur.fetchone()
##        if data:
##            coach['city'] = data['name']
    for coach in coaches:
        locations = coach['locations']
        locations_arr = []
        while locations != 0:
            pw = 1
            while 2 ** (pw + 1) <= locations:
                pw += 1
            locations -= 2 ** pw
            locations_arr.append(pw)
        locations_text = ''
        for location in locations_arr:
            cur.execute('SELECT text FROM locations WHERE id = ?', [location, ])
            locations_text += cur.fetchone()['text'] + ';'
        locations_text = locations_text[:-1]
        coach['locations'] = locations_text.split(';')
    conn.close()
    return render_template('coaches.html', coaches=coaches)

@app.route('/coach')
def coach():
    if not session.get('edzo_logged_in'):
        return redirect(url_for('edzo_login'))
    conn = sqlite3.connect(app.config['DATABASE_EDZO'])
    conn.row_factory = my_factory
    cur = conn.cursor()
    id = request.args.get('id')
    cur.execute('SELECT * FROM coaches WHERE id = ?', [id, ])
    user_data = cur.fetchone()
    targets = user_data['targets']
    targets_arr = []
    while targets != 0:
        pw = 1
        while 2 ** (pw + 1) <= targets:
            pw += 1
        targets -= 2 ** pw
        targets_arr.append(pw)
    targets_text = ''
    for target in targets_arr:
        cur.execute('SELECT text FROM targets WHERE id = ?', [target, ])
        targets_text += cur.fetchone()['text'] + ';'
    targets_text = targets_text[:-1]
    user_data['targets'] = targets_text.split(';')

    locations = user_data['locations']
    locations_arr = []
    while locations != 0:
        pw = 1
        while 2 ** (pw + 1) <= locations:
            pw += 1
        locations -= 2 ** pw
        locations_arr.append(pw)
    locations_text = ''
    for location in locations_arr:
        cur.execute('SELECT text FROM locations WHERE id = ?', [location, ])
        locations_text += cur.fetchone()['text'] + ';'
    locations_text = locations_text[:-1]
    user_data['locations'] = locations_text.split(';')
    
    if user_data['qual_photo']:
        user_data['qual_photo'] = user_data['qual_photo'].split(',')
    if user_data['self_photo']:
        user_data['self_photo'] = user_data['self_photo'].split(',')
    if user_data['self_link'] == None:
        user_data['self_link'] = 'Не указаны'
    conn.close()
    return render_template('coach.html', user_data=user_data)

@app.route('/students')
def students():
    if not session.get('edzo_logged_in'):
        return redirect(url_for('edzo_login'))
    conn = sqlite3.connect(app.config['DATABASE_EDZO'])
    conn.row_factory = my_factory
    cur = conn.cursor()
    cur.execute('SELECT * FROM students WHERE step == "" OR step IS NULL')
    students = cur.fetchall()
    for student in students:
        if student['give_contact'] == 1:
            student['give_contact'] = 'Да'
        else:
            student['give_contact'] = 'Нет'
##        cur.execute('SELECT text FROM ages WHERE id = ?', [student['age'], ])
##        age = cur.fetchone()
##        if age:
##            age = age['text']
##        else:
##            age = None
##        student['age'] = age
        target = int(math.sqrt(student['target']))
        cur.execute('SELECT text FROM targets WHERE id = ?', [target, ])
        data = cur.fetchone()
        if data:
            student['target'] = data['text']
        else:
            student['target'] = None
        cur.execute('SELECT text FROM students_levels WHERE id = ?', [student['level'], ])
        data = cur.fetchone()
        if data:
            level = data['text']
        else:
            level = None
        student['level'] = level
##        if student['how_train'] == -1:
##            student['how_train'] = 'Оффлайн'
##        elif student['how_train'] == 1:
##            student['how_train'] = 'Онлайн'
##        else:
##            student['how_train'] = 'Оффлайн и онлайн'
##        cur.execute('SELECT name FROM cities WHERE id = ?', [student['city'], ])
##        data = cur.fetchone()
##        if data:
##            student['city'] = data['name']
##        else:
##            student['city'] = None
        location = int(student['location'])
        cur.execute('SELECT text FROM locations WHERE id = ?', [location, ])
        student['location'] = cur.fetchone()['text']
        
        if student['search'] == 0:
            student['search'] = 'Нет'
        elif student['search'] == 1:
            student['search'] = 'Да'
        if student['coach'] == None:
            student['coach'] = 'Тренер не найден'
    conn.close()
    return render_template('students.html', students=students)

@app.route('/approve', methods=['GET', 'POST'])
def approve():
    if not session.get('edzo_logged_in'):
        return redirect(url_for('edzo_login'))
    id = request.args.get('id')
    approve = request.args.get('approve')
    coach = request.args.get('coach')
    conn = sqlite3.connect(app.config['DATABASE_EDZO'])
    cur = conn.cursor()
    cur.execute('UPDATE coaches SET approve_coach = 1, active_coach = 0 WHERE id = ?', [id, ])
    conn.commit()
    cur.execute('SELECT students_count FROM coaches WHERE id = ?', [id, ])
    students_count = cur.fetchone()[0]
    conn.close()
    text = 'Спасибо, мы проверили твою анкету, теперь мы можем смэтчить тебя со спортсменами.'
    bot = telebot.TeleBot(TOKEN_EDZO)
    bot.send_message(id, text, reply_markup=gen_markup_edzo(search=True), parse_mode='HTML')
    if coach:
        return redirect(url_for('coach', id=id))
    return redirect(url_for('coaches'))

@app.route('/deapprove', methods=['GET', 'POST'])
def deapprove():
    if not session.get('edzo_logged_in'):
        return redirect(url_for('edzo_login'))
    id = request.args.get('id')
    approve = request.args.get('approve')
    coach = request.args.get('coach')
    conn = sqlite3.connect(app.config['DATABASE_EDZO'])
    cur = conn.cursor()
    cur.execute('UPDATE coaches SET approve_coach = 0, active_coach = 0 WHERE id = ?', [id, ])
    conn.commit()
    conn.close()
    text = 'Квалификация не подтверждена\nПоиск учеников не доступен!'
    bot = telebot.TeleBot(TOKEN_EDZO)
    bot.send_message(id, text, reply_markup=gen_markup_edzo(search=False), parse_mode='HTML')
    if coach:
        return redirect(url_for('coach', id=id))
    return redirect(url_for('coaches'))



@app.route('/login', methods=['GET', 'POST'])
def edzo_login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin':
            error = 'Invalid username'
        elif request.form['password'] != '123':
            error = 'Invalid password'
        else:
            session['edzo_logged_in'] = True
            flash('Вы вошли в личный кабинет')
            return redirect(url_for('coaches'))

    return render_template('login_edzo.html', error=error)

@app.route('/logout')
def edzo_logout():
    session.pop('edzo_logged_in', None)
    flash('Вы вышли из личного кабинета')
    return redirect(url_for('edzo_login'))

app.run()
