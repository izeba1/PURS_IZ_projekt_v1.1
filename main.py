from flask import Flask, request,  make_response, render_template, Response, session, redirect, url_for, g, json, jsonify
import MySQLdb
import jinja2
import requests

app = Flask("Prva flask aplikacija")

app.secret_key = 'jisa8{@}][2`°˙saaw123454-we234--.234]'


@app.before_request
def before_request_func():
    g.connection = MySQLdb.connect(host='localhost', user='app', password='1234', db='projektdb')
    g.cursor = g.connection.cursor()

    if request.path == '/login' or request.path.startswith('/static') or request.path == '/pocetna' or request.path == '/gas_sens':
        return
    if session.get('username') is None:
        return redirect(url_for('login_page'))

@app.after_request
def after_request_func(response):
    g.connection.commit()
    g.connection.close()
    return response

@app.get('/')
def home_page():
   id = request.args.get('id')
   if id == '1' or id == None:
       g.cursor.execute(render_template('get_co.sql'))
       co_vrijednosti = g.cursor.fetchall()
       return render_template('index.html', naslov='Početna stranica', username=session.get('username'), d = 1, data = co_vrijednosti, ovlasti = session.get('ovlasti')), 200
   if id == '2':
       g.cursor.execute(render_template('get_korisnik.sql'))
       korisnici = g.cursor.fetchall()
       return render_template('index.html', naslov='Korisnici', username=session.get('username'), d = 2, data = korisnici, ovlasti = session.get('ovlasti')), 200  


@app.get('/login')
def login_page():
    response = render_template('login.html', title='Login stranica')

    return response, 200


@app.get('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('login_page'))


@app.post('/login')
def login():
    g.cursor.execute(render_template('get_user.sql', username = request.form.get('username'), password = request.form.get('password')))
    user = g.cursor.fetchone()

    if user:
        session['id'] = user[0] 
        session['username'] = user[1]
        session['ovlasti'] = user[2]
        return redirect(url_for('home_page'))
    
    else:
        return render_template('login.html', title='Stranica za login', poruka='Uneseni su krivi podatci za prijavu!')
    

@app.post('/zadana_vrijednost')
def put_co_vrijednosti():
    
    co_vrijednost = request.form.get('zadana_vrijednost')

    if co_vrijednost:
        zadana_vrijednost = int(co_vrijednost)
        # Spremanje u tablicu zadana_vrijednost za nadogradnju projekta
        g.cursor.execute(render_template('zadana_vrijednost.sql', vrijednost = zadana_vrijednost)) 
        return redirect('/?id=1')


@app.post('/obrisi_korisnika')
def deleteUser():
    userid = request.form.get('id')
    g.cursor.execute(render_template('obrisi_korisnika.sql', id=userid))
    return redirect('/?id=2')

@app.post('/dodaj_korisnika')
def addUser():
    ime = request.form.get('ime')
    prezime = request.form.get('prezime')
    username = request.form.get('username')
    password = request.form.get('password')
    id_ovlasti = request.form.get('ovlast')
    g.cursor.execute(render_template('dodaj_korisnika.sql', ime = ime, prezime = prezime, username = username, password = password, id_ovlasti = id_ovlasti))
    return redirect('/?id=2')




#MIKROKONTROLER
@app.post('/gas_sens')
def put_gas_sens():
    global gas

    response = make_response()
    gas_data = json.loads(request.data)
    print(gas_data)
    gas_value = gas_data.get('gas') # Izdvajanje vrijednosti iz json poruke
    gas = int(gas_value) # Pretvaranje vrijednosti u int
    # Spremanje vrijednosti u bazu podataka (gas_vrijednost)
    g.cursor.execute(render_template('upis_co.sql', vrijednost = gas))
    response.status_code = 201


    # Dohvaćanje zadnje zadane vrijednost 
    g.cursor.execute(render_template('get_zadana_vrijednost.sql'))
    zadana = g.cursor.fetchone() [0]

    if gas > zadana:
        status_code = postesp32_server("ON")
        if status_code == 200:
            return jsonify({'poruka': 'Ventilator je upaljen!'}), 200
        else:
            return jsonify({'error': 'Greška pri slanju zahtjeva na esp server!'}), 200
    else:
        status_code = postesp32_server("OFF")
        if status_code == 200:
            return jsonify({'message': 'Ventilator je ugašen!'}), 200
        else:
            return jsonify({'error': 'Greška pri slanju zahtjeva na esp server!'}), 200




@app.get('/zadnja_vrijednost')
def get_zadnja_vrijednost():
    try:
        # Izvršavanje SQL upita za dohvaćanje zadnje vrijednosti CO
        g.cursor.execute(render_template('zadnja_vrijednost.sql'))
        zadnja_i = g.cursor.fetchone() [0]  # Dohvaćanje prvog stupca rezultata upita

        # Vraćanje zadnje vrijednosti CO kao JSON objekt
        zadnja = str(zadnja_i)
        return jsonify({'zadnja_vrijednost': zadnja})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

######################################

def postesp32_server(action):
    esp_ip = "http://192.168.183.59"
    endpoint = f"/{action}"
    url = esp_ip + endpoint
    response = requests.post(url)
    return response.status_code


#######################################

    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)