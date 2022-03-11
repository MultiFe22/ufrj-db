from crypt import methods
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from query import cnpj, filial, cnae, active_companies, oldest_company, total_companies, number_of_richest_companies, count_state_companies

#create a flask app
app = Flask(__name__)

@app.route('/')
#create a home with a button and a form to gather the data
def home():
    return redirect(url_for('result'))

@app.route('/queries', methods=['POST', 'GET'])
#receive the cnpj and return the result
def result():
    if request.method == 'POST':
        if request.form['cnp'] == "CNPJ":
            cnpj = request.form['nm']
            return redirect(url_for('cnpj_query', cnpj_base=cnpj))
        elif request.form['cnp'] == "Filial":
            cnpj = request.form['nm']
            return redirect(url_for('cnpj_filial', cnpj_base=cnpj))
        elif request.form['cnp'] == "cnae":
            return redirect(url_for('cnae_query'))
        elif request.form['cnp'] == "active companies":
            return redirect(url_for('active_companies_query'))
        elif request.form['cnp'] == "oldest company":
            return redirect(url_for('oldest_company_query'))
        elif request.form['cnp'] == "richest companies":
            return redirect(url_for('richest_companies_query'))
        elif request.form['cnp'] == "companies by state":
            uf = request.form['nm']
            return redirect(url_for('state_companies_query', uf=uf))
        elif request.form['cnp'] == "total companies":
            return redirect(url_for('total_companies_query'))
        else:
            return render_template('queries.html')
    else:
        return render_template('queries.html')

@app.route('/query/<cnpj_base>')
def cnpj_query(cnpj_base):
    data = cnpj(cnpj_base)
    return render_template('cnpj.html', cnpj_completo=data['cnpj'], nome=data['nome'], nome_fantasia=data['nome-fantasia'], socio=data['socio'], estado=data['estado'], bairro=data['bairro'], logradouro=data['logradouro'], numero=data['numero'], cep=data['cep'], municipio=data['municipio'])

@app.route('/query/<cnpj_base>/filial')
def cnpj_filial(cnpj_base):
    data = filial(cnpj_base)
    return render_template('filial.html', result=data)

@app.route('/query/cnae')
def cnae_query():
    data = cnae()
    return render_template('cnae.html', result=data)

@app.route('/query/active_companies')
def active_companies_query():
    data = active_companies()
    return render_template('active_companies.html', result=data)

@app.route('/query/oldest_company')
def oldest_company_query():
    data = oldest_company()
    return render_template('oldest_company.html', result=data)

@app.route('/query/richest_companies')
def richest_companies_query():
    data = number_of_richest_companies()
    return render_template('richest_companies.html', result=data)

@app.route('/query/companies_by_state/<uf>')
def state_companies_query(uf):
    data = count_state_companies(uf)
    return render_template('state_companies.html', result=data, uf=uf)

@app.route('/query/companies_by_state')
def total_companies_query():
    data = total_companies()
    return render_template('total_companies.html', result=data)


if __name__ == '__main__':
    app.run(debug=True)
