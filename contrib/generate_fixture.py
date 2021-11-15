# coding:utf-8
import json
import re

MODEL_POSTO = 'vacina.posto'
MODEL_TELEFONE = 'vacina.telefoneposto'
MODEL_COORDENADA = 'vacina.coordenadasposto'

with open('ubs.json', encoding='utf-8') as data_file:
	data = json.load(data_file)
	fixtures_posto = []
	fixtures_telefones = []
	fixtures_coordenadas = []
	posto_pk = 0
	telefone_pk = 0
	coordenada_pk = 0

	for posto in data:
		posto_pk += 1
		match = re.search('[^\d]+', posto['informacoesIdentificacaoUBS'])
		nome = match.group()

		fixture_posto = {
			"model": MODEL_POSTO,
			"pk": posto_pk,
			"fields": {
				# "nome": posto['informacoesIdentificacaoUBS'].title(),
				"nome": nome.title().strip(),
				"logradouro": posto['enderecoUBS'].title(),
				"ender_num": posto['numeroEnderecoUBS'],
				"bairro": posto['bairroEnderecoUBS'].title(),
				"cidade": 'São Paulo',
				"estado": 'SP',
				"pais": 'Brasil',
				"cep": posto['cepUBS']
			}
		}
		for i in range(2):


			if i == 0:
				telefone = 'telefone1UBS'
				principal = True
			else:
				telefone = 'telefone2UBS'
				principal = False
			if posto[telefone] != '':
				telefone_pk += 1
				fixture_telefone = {
					"model": MODEL_TELEFONE,
					"pk": telefone_pk,
					"fields": {
						"posto": posto_pk,
						"numero": f'(11){posto[telefone]}',
						"principal": principal,
					}
				}
				fixtures_telefones.append(fixture_telefone)

		coordenada_pk += 1
		fixture_coordenada = {
			"model": MODEL_COORDENADA,
			"pk": coordenada_pk,
			"fields": {
				"posto": posto_pk,
				"latitude": posto['geoLocalizacaoUSB'][0]['latitude'],
				"longitude": posto['geoLocalizacaoUSB'][0]['longitude'],
			}
		}
		fixtures_coordenadas.append(fixture_coordenada)

		fixtures_posto.append(fixture_posto)

	fixture_data_posto = json.dumps(fixtures_posto)
	fixture_data_telefone = json.dumps(fixtures_telefones)
	fixture_data_coordenadas = json.dumps(fixtures_coordenadas)

	fixtures_file = open("ubs_models.json", "w")
	fixtures_file.write(fixture_data_posto)
	fixtures_file.close()
	fixtures_file = open("ubs_telefones.json", "w")
	fixtures_file.write(fixture_data_telefone)
	fixtures_file.close()
	fixtures_file = open("ubs_coordenadas.json", "w")
	fixtures_file.write(fixture_data_coordenadas)
	fixtures_file.close()
