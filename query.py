from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import re

def getEnv(env):
    return os.getenv(env)

def cnpj(cnpj):
    load_dotenv()
    company = {}
    user=getEnv('DB_USER')
    passw=getEnv('DB_PASSWORD')
    host=getEnv('DB_HOST')
    port=getEnv('DB_PORT')
    database=getEnv('DB_NAME')

    engine = create_engine('mysql://'+user+':'+passw+'@'+host+':'+port+'/'+database)

    with engine.connect() as conn:
        result = conn.execute(text("""
        select estabelecimento.cnpj_basico,
            estabelecimento.cnpj_ordem,
            estabelecimento.cnpj_dv,
            socios.nome_socio_razao_social ,
            estabelecimento.uf,
            estabelecimento.bairro,
            estabelecimento.logradouro,
            estabelecimento.numero,
            estabelecimento.cep,
            munic.descricao,
            estabelecimento.situacao_cadastral,
            empresa.razao_social,
            estabelecimento.nome_fantasia,
            estabelecimento.tipo_logradouro 
            from estabelecimento 
            inner join empresa 
                on estabelecimento.cnpj_basico = empresa.cnpj_basico
            inner join munic
                on estabelecimento.municipio = munic.codigo 
            left outer join socios 
                on empresa.cnpj_basico = socios.cnpj_basico
            where estabelecimento.cnpj_basico = '{}'
            limit 1
        """.format(cnpj)))
    
    for row in result:
        company['nome'] = str(row[11])
        company['nome-fantasia'] = str(row[12])
        company['cnpj'] = row[0] + str(row[1]) + str(row[2])
        
        if row[3] == None:
            # uses regex to remove all non-alphabetical characters from the string, keeping spaces
            associate = re.search('[-a-zA-Z.]+(\s+[-a-zA-Z.]+)*', str(row[11]))
            associate = associate.group(0)
            company['socio'] = associate
        else:
            company['socio'] = str(row[3])
        
        company['estado'] = row[4]
        company['bairro'] = row[5]
        company['logradouro'] = str(row[13]) + " " + str(row[6])
        company['numero'] = row[7]
        company['cep'] = row[8]
        company['municipio'] = row[9]
        break
    return company

def filial(cnpj):
    load_dotenv()
    company = {}
    return_value = []
    user=getEnv('DB_USER')
    passw=getEnv('DB_PASSWORD')
    host=getEnv('DB_HOST')
    port=getEnv('DB_PORT')
    database=getEnv('DB_NAME')

    engine = create_engine('mysql://'+user+':'+passw+'@'+host+':'+port+'/'+database)

    with engine.connect() as conn:
        result = conn.execute(text("""
        select  estabelecimento.uf,
        estabelecimento.bairro,
        estabelecimento.logradouro,
        estabelecimento.numero,
        estabelecimento.cep,
        munic.descricao,
        estabelecimento.situacao_cadastral,
        empresa.razao_social,
        estabelecimento.nome_fantasia,
        estabelecimento.tipo_logradouro 
        from estabelecimento 
        inner join empresa 
            on estabelecimento.cnpj_basico = empresa.cnpj_basico
        inner join munic
            on estabelecimento.municipio = munic.codigo 
        where estabelecimento.cnpj_basico = '{}' and estabelecimento.identificador_matriz_filial = '2'
        """.format(cnpj)))
    
    for row in result:
        company['nome-fantasia'] = str(row[8])       
        company['estado'] = row[0]
        company['bairro'] = row[1]
        company['logradouro'] = str(row[9]) + " " + str(row[2])
        company['numero'] = row[3]
        company['cep'] = row[4]
        company['municipio'] = row[5]
        return_value.append(company)
    return return_value

def cnae():
    load_dotenv()
    user=getEnv('DB_USER')
    passw=getEnv('DB_PASSWORD')
    host=getEnv('DB_HOST')
    port=getEnv('DB_PORT')
    database=getEnv('DB_NAME')
    return_value = []
    engine = create_engine('mysql://'+user+':'+passw+'@'+host+':'+port+'/'+database)

    with engine.connect() as conn:
        result = conn.execute(text("""
        select * from cnae
        """))
    
    for row in result:
        cnae_dict = {}
        cnae_dict['codigo'] = row[0]
        cnae_dict['descricao'] = row[1]
        return_value.append(cnae_dict)
    
    return return_value

def active_companies():
    load_dotenv()
    company = {}
    return_value = []
    user=getEnv('DB_USER')
    passw=getEnv('DB_PASSWORD')
    host=getEnv('DB_HOST')
    port=getEnv('DB_PORT')
    database=getEnv('DB_NAME')

    engine = create_engine('mysql://'+user+':'+passw+'@'+host+':'+port+'/'+database)

    with engine.connect() as conn:
        result = conn.execute(text("""select count(*) from estabelecimento where situacao_cadastral = '02'"""))

    for row in result:
        return row[0]

def oldest_company():
    load_dotenv()
    company = {}
    return_value = []
    user=getEnv('DB_USER')
    passw=getEnv('DB_PASSWORD')
    host=getEnv('DB_HOST')
    port=getEnv('DB_PORT')
    database=getEnv('DB_NAME')

    engine = create_engine('mysql://'+user+':'+passw+'@'+host+':'+port+'/'+database)

    with engine.connect() as conn:
        result = conn.execute(text("""
        select * from estabelecimento where data_inicio_atividade in
        (select min(data_inicio_atividade) from estabelecimento where data_inicio_atividade > 18000101)
        """))
    
    for row in result:
        for item in row:
            return_value.append(item)
    
    return return_value

def number_of_richest_companies():
    load_dotenv()

    user=getEnv('DB_USER')
    passw=getEnv('DB_PASSWORD')
    host=getEnv('DB_HOST')
    port=getEnv('DB_PORT')
    database=getEnv('DB_NAME')
    
    engine = create_engine('mysql://'+user+':'+passw+'@'+host+':'+port+'/'+database)

    with engine.connect() as conn:
        result = conn.execute(text("""
        select count(*) from empresa where capital_social > 1000000000.0"""))

    for row in result:
        return row[0]

def count_state_companies(uf):
    load_dotenv()

    user=getEnv('DB_USER')
    passw=getEnv('DB_PASSWORD')
    host=getEnv('DB_HOST')
    port=getEnv('DB_PORT')
    database=getEnv('DB_NAME')

    engine = create_engine('mysql://'+user+':'+passw+'@'+host+':'+port+'/'+database)

    with engine.connect() as conn:
        result = conn.execute(text("""
        select count(*) from estabelecimento where uf = '{}'""".format(uf)))

    for row in result:
        return row[0]

def total_companies():
    load_dotenv()

    user=getEnv('DB_USER')
    passw=getEnv('DB_PASSWORD')
    host=getEnv('DB_HOST')
    port=getEnv('DB_PORT')
    database=getEnv('DB_NAME')

    engine = create_engine('mysql://'+user+':'+passw+'@'+host+':'+port+'/'+database)

    with engine.connect() as conn:
        result = conn.execute(text("""
        select count(*) from estabelecimento"""))
    
    for row in result:
        return row[0]