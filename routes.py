import os
from flask import Flask, render_template, jsonify, request, send_file, redirect, url_for, flash, session
import json
import pandas as pd
from app import app, db
import io
from auth import auth_manager, login_required
from flask_migrate import Migrate
from datetime import datetime

# Initialize Migration
migrate = Migrate(app, db)



# Load crop data
def load_crop_data():
    try:
        with open('data/crop_data_static.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Arquivo crop_data_static.json não encontrado")
        return {}
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return {}

# Load fertilizer data
def load_fertilizer_data():
    try:
        with open('data/fertilizer_data_static_corrigido.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Arquivo fertilizer_data_static_corrigido.json não encontrado")
        return {}
    except Exception as e:
        print(f"Erro ao carregar dados de fertilizantes: {e}")
        return {}

# Load static data files
try:
    with open('data/crop_data_static.json', 'r', encoding='utf-8') as f:
        CROP_DATA = json.load(f)
    print(f"Loaded crop data with {len(CROP_DATA)} crops")
except Exception as e:
    print(f"Error loading crop data: {e}")
    CROP_DATA = {}

try:
    with open('data/fertilizer_data_static_corrigido.json', 'r', encoding='utf-8') as f:
        FERTILIZER_DATA = json.load(f)
    print(f"Loaded fertilizer data with {len(FERTILIZER_DATA)} categories")
except Exception as e:
    print(f"Error loading fertilizer data: {e}")
    FERTILIZER_DATA = {}

try:
    with open('data/agrotoxico_data_static.json', 'r', encoding='utf-8') as f:
        AGROTOXICO_DATA = json.load(f)
    print(f"Loaded agrotoxico data with {len(AGROTOXICO_DATA)} categories")
except Exception as e:
    print(f"Error loading agrotoxico data: {e}")
    AGROTOXICO_DATA = {}

try:
    with open('data/consultoria_tecnica_data_static.json', 'r', encoding='utf-8') as f:
        CONSULTORIA_DATA = json.load(f)
    print(f"Loaded consultoria tecnica data with {len(CONSULTORIA_DATA)} categories")
except Exception as e:
    print(f"Error loading consultoria tecnica data: {e}")
    CONSULTORIA_DATA = {}

try:
    with open('data/corretivos_data_static.json', 'r', encoding='utf-8') as f:
        CORRETIVOS_DATA = json.load(f)
    print(f"Loaded corretivos data with {len(CORRETIVOS_DATA)} categories")
except Exception as e:
    print(f"Error loading corretivos data: {e}")
    CORRETIVOS_DATA = {}

try:
    with open('data/despesa_data_static.json', 'r', encoding='utf-8') as f:
        DESPESA_DATA = json.load(f)
    print(f"Loaded despesa data with {len(DESPESA_DATA)} categories")
except Exception as e:
    print(f"Error loading despesa data: {e}")
    DESPESA_DATA = {}

try:
    with open('data/escolaridade_data_static.json', 'r', encoding='utf-8') as f:
        ESCOLARIDADE_DATA = json.load(f)
    print(f"Loaded escolaridade data with {len(ESCOLARIDADE_DATA)} categories")
except Exception as e:
    print(f"Error loading escolaridade data: {e}")
    ESCOLARIDADE_DATA = {}

try:
    with open('data/receita_data_static.json', 'r', encoding='utf-8') as f:
        RECEITA_DATA = json.load(f)
    print(f"Loaded receita data with {len(RECEITA_DATA)} categories")
except Exception as e:
    print(f"Error loading receita data: {e}")
    RECEITA_DATA = {}

@app.route('/')
@login_required
def index():
    user = auth_manager.get_current_user()
    return render_template('index.html', user=user)

@app.route('/analysis')
@login_required
def analysis():
    user = auth_manager.get_current_user()
    return render_template('analysis.html', user=user)

@app.route('/api/brazilian-states')
def get_states():
    try:
        # Brazilian states
        states = [
            {'code': 'AC', 'name': 'Acre'},
            {'code': 'AL', 'name': 'Alagoas'},
            {'code': 'AP', 'name': 'Amapá'},
            {'code': 'AM', 'name': 'Amazonas'},
            {'code': 'BA', 'name': 'Bahia'},
            {'code': 'CE', 'name': 'Ceará'},
            {'code': 'DF', 'name': 'Distrito Federal'},
            {'code': 'ES', 'name': 'Espírito Santo'},
            {'code': 'GO', 'name': 'Goiás'},
            {'code': 'MA', 'name': 'Maranhão'},
            {'code': 'MT', 'name': 'Mato Grosso'},
            {'code': 'MS', 'name': 'Mato Grosso do Sul'},
            {'code': 'MG', 'name': 'Minas Gerais'},
            {'code': 'PA', 'name': 'Pará'},
            {'code': 'PB', 'name': 'Paraíba'},
            {'code': 'PR', 'name': 'Paraná'},
            {'code': 'PE', 'name': 'Pernambuco'},
            {'code': 'PI', 'name': 'Piauí'},
            {'code': 'RJ', 'name': 'Rio de Janeiro'},
            {'code': 'RN', 'name': 'Rio Grande do Norte'},
            {'code': 'RS', 'name': 'Rio Grande do Sul'},
            {'code': 'RO', 'name': 'Rondônia'},
            {'code': 'RR', 'name': 'Roraima'},
            {'code': 'SC', 'name': 'Santa Catarina'},
            {'code': 'SP', 'name': 'São Paulo'},
            {'code': 'SE', 'name': 'Sergipe'},
            {'code': 'TO', 'name': 'Tocantins'}
        ]

        return jsonify({
            'success': True,
            'states': states
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/statistics')
def get_statistics():
    try:
        # CROP_DATA structure: {crop_name: {municipality_code: {data}}}
        total_crops = len(CROP_DATA)
        total_fertilizer_categories = len(FERTILIZER_DATA)
        total_agrotoxico_categories = len(AGROTOXICO_DATA)
        total_consultoria_categories = len(CONSULTORIA_DATA)
        total_corretivos_categories = len(CORRETIVOS_DATA)
        total_despesa_categories = len(DESPESA_DATA)
        total_escolaridade_categories = len(ESCOLARIDADE_DATA)
        total_receita_categories = len(RECEITA_DATA)

        # Count unique municipalities across all crops
        all_municipalities = set()
        for crop_data in CROP_DATA.values():
            all_municipalities.update(crop_data.keys())

        # Count unique municipalities across all fertilizer categories
        all_fertilizer_municipalities = set()
        for fertilizer_data in FERTILIZER_DATA.values():
            all_fertilizer_municipalities.update(fertilizer_data.keys())

        total_municipalities = len(all_municipalities)
        total_fertilizer_municipalities = len(all_fertilizer_municipalities)

        # Calculate total establishments for fertilizer data
        total_establishments = 0
        if 'Total Estabelecimentos' in FERTILIZER_DATA:
            for municipality_data in FERTILIZER_DATA['Total Estabelecimentos'].values():
                if isinstance(municipality_data, dict) and 'value' in municipality_data:
                    total_establishments += municipality_data.get('value', 0)

        return jsonify({
            'success': True,
            'statistics': {
                'total_crops': total_crops,
                'total_municipalities': total_municipalities,
                'total_fertilizer_categories': total_fertilizer_categories,
                'total_agrotoxico_categories': total_agrotoxico_categories,
                'total_consultoria_categories': total_consultoria_categories,
                'total_corretivos_categories': total_corretivos_categories,
                'total_despesa_categories': total_despesa_categories,
                'total_escolaridade_categories': total_escolaridade_categories,
                'total_receita_categories': total_receita_categories,
                'total_establishments': total_establishments,
                'data_sources': {
                    'culturas': total_crops,
                    'fertilizantes': total_fertilizer_categories,
                    'agrotoxicos': total_agrotoxico_categories,
                    'consultoria_tecnica': total_consultoria_categories,
                    'corretivos': total_corretivos_categories,
                    'despesas': total_despesa_categories,
                    'escolaridade': total_escolaridade_categories,
                    'receitas': total_receita_categories
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/crops')
def get_crops():
    try:
        # CROP_DATA structure: {crop_name: {municipality_code: {data}}}
        sorted_crops = sorted(list(CROP_DATA.keys()))
        return jsonify({
            'success': True,
            'crops': sorted_crops
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/fertilizer-categories')
def get_fertilizer_categories():
    try:
        # FERTILIZER_DATA structure: {category_name: {municipality_code: {data}}}
        categories = sorted(list(FERTILIZER_DATA.keys()))
        return jsonify({
            'success': True,
            'categories': categories
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/agrotoxico/categories')
def get_agrotoxico_categories():
    try:
        categories = list(AGROTOXICO_DATA.keys())
        return jsonify({
            "success": True,
            "categories": categories,
            "total": len(categories)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/consultoria/categories')
def get_consultoria_categories():
    try:
        categories = list(CONSULTORIA_DATA.keys())
        return jsonify({
            "success": True,
            "categories": categories,
            "total": len(categories)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/corretivos/categories')
def get_corretivos_categories():
    try:
        categories = list(CORRETIVOS_DATA.keys())
        return jsonify({
            "success": True,
            "categories": categories,
            "total": len(categories)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/despesa/categories')
def get_despesa_categories():
    try:
        categories = list(DESPESA_DATA.keys())
        return jsonify({
            "success": True,
            "categories": categories,
            "total": len(categories)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/escolaridade/categories')
def get_escolaridade_categories():
    try:
        categories = list(ESCOLARIDADE_DATA.keys())
        return jsonify({
            "success": True,
            "categories": categories,
            "total": len(categories)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/receita/categories')
def get_receita_categories():
    try:
        categories = list(RECEITA_DATA.keys())
        return jsonify({
            "success": True,
            "categories": categories,
            "total": len(categories)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/fertilizer-data/<category_name>')
def get_fertilizer_data(category_name):
    try:
        # Busca exata primeiro
        if category_name in FERTILIZER_DATA:
            all_fertilizer_data = FERTILIZER_DATA[category_name]

            # Filtrar apenas municípios válidos (códigos IBGE reais de municípios)
            fertilizer_municipalities = {}
            for municipality_code, municipality_data in all_fertilizer_data.items():
                municipality_code_str = str(municipality_code)
                municipality_name = municipality_data.get('municipality_name', '').lower()

                # Verificar se é um código de município válido
                if (len(municipality_code_str) == 7 and 
                    municipality_code_str.isdigit() and
                    municipality_code_str[0] in '12345' and  # Códigos reais começam com 1-5
                    municipality_data.get('municipality_name') and
                    # Excluir nomes que indicam regiões/agregações
                    not any(keyword in municipality_name for keyword in [
                        'região', 'mesorregião', 'microrregião', 'nordeste', 'norte', 'sul', 
                        'centro', 'oeste', 'leste', 'sudeste', 'noroeste', 'sudoeste',
                        'alto ', 'baixo ', 'médio ', '-grossense', 'parecis', 'araguaia',
                        'pantanal', 'cerrado', 'amazônia', 'caatinga', 'mata atlântica'
                    ])):
                    # Padronizar o nome do campo para compatibilidade
                    fertilizer_data = {
                        'municipality_name': municipality_data.get('municipality_name'),
                        'state_code': municipality_data.get('state_code'),
                        'harvested_area': municipality_data.get('value', 0),  # Mapear 'value' para 'harvested_area'
                        'unit': municipality_data.get('unit', 'un')
                    }
                    fertilizer_municipalities[municipality_code] = fertilizer_data

            return jsonify({
                'success': True,
                'data': fertilizer_municipalities,
                'data_type': 'fertilizer'
            })

        return jsonify({'success': False, 'error': 'Categoria de fertilizantes não encontrada'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/agrotoxico/<category>')
def get_agrotoxico_data(category):
    try:
        if category in AGROTOXICO_DATA:
            return jsonify({
                'success': True,
                'data': AGROTOXICO_DATA[category],
                'type': 'agrotoxico'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Categoria de agrotóxico "{category}" não encontrada'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/consultoria/<category>')
def get_consultoria_data(category):
    try:
        if category in CONSULTORIA_DATA:
            return jsonify({
                'success': True,
                'data': CONSULTORIA_DATA[category],
                'category': category
            })
        else:
            return jsonify({
                'success': False,
                'error': f"Categoria '{category}' não encontrada"
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/corretivos/<category>')
def get_corretivos_data(category):
    try:
        if category in CORRETIVOS_DATA:
            return jsonify({
                'success': True,
                'data': CORRETIVOS_DATA[category],
                'category': category
            })
        else:
            return jsonify({
                'success': False,
                'error': f"Categoria '{category}' não encontrada"
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/despesa/<category>')
def get_despesa_data(category):
    try:
        if category in DESPESA_DATA:
            return jsonify({
                'success': True,
                'data': DESPESA_DATA[category],
                'type': 'despesa'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Categoria de despesa "{category}" não encontrada'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/escolaridade/<category>')
def get_escolaridade_data(category):
    try:
        if category in ESCOLARIDADE_DATA:
            return jsonify({
                'success': True,
                'data': ESCOLARIDADE_DATA[category],
                'category': category
            })
        else:
            return jsonify({
                'success': False,
                'error': f"Categoria '{category}' não encontrada"
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/receita/<category>')
def get_receita_data(category):
    try:
        if category in RECEITA_DATA:
            return jsonify({
                'success': True,
                'data': RECEITA_DATA[category],
                'type': 'receita'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Categoria de receita "{category}" não encontrada'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/crop-data/<crop_name>')
def get_crop_data(crop_name):
    try:
        # Busca exata primeiro
        if crop_name in CROP_DATA:
            all_crop_data = CROP_DATA[crop_name]

            # Filtrar apenas municípios válidos (códigos IBGE reais de municípios)
            crop_municipalities = {}
            for municipality_code, municipality_data in all_crop_data.items():
                municipality_code_str = str(municipality_code)
                municipality_name = municipality_data.get('municipality_name', '').lower()

                # Verificar se é um código de município válido
                # Códigos de município IBGE começam com 1-5 e têm 7 dígitos
                # Excluir códigos que começam com 0 (são agregações regionais)
                if (len(municipality_code_str) == 7 and 
                    municipality_code_str.isdigit() and
                    municipality_code_str[0] in '12345' and  # Códigos reais começam com 1-5
                    municipality_data.get('municipality_name') and
                    # Excluir nomes que indicam regiões/agregações
                    not any(keyword in municipality_name for keyword in [
                        'região', 'mesorregião', 'microrregião', 'nordeste', 'norte', 'sul', 
                        'centro', 'oeste', 'leste', 'sudeste', 'noroeste', 'sudoeste',
                        'alto ', 'baixo ', 'médio ', '-grossense', 'parecis', 'araguaia',
                        'pantanal', 'cerrado', 'amazônia', 'caatinga', 'mata atlântica'
                    ]) and
                    # Excluir nomes muito genéricos ou que são claramente regiões
                    municipality_name not in [
                        'alto teles pires', 'sudeste mato-grossense', 'parecis', 'barreiras',
                        'dourados', 'norte mato-grossense', 'portal da amazônia'
                    ]):
                    crop_municipalities[municipality_code] = municipality_data

            # Debug: Encontrar o maior produtor para verificação
            if crop_municipalities:
                # Ordenar por área colhida para debug
                sorted_municipalities = sorted(crop_municipalities.items(), 
                                             key=lambda x: float(x[1].get('harvested_area', 0)), 
                                             reverse=True)
                max_municipality = sorted_municipalities[0]
                print(f"Debug - Maior produtor de {crop_name} (apenas municípios): {max_municipality[1].get('municipality_name')} ({max_municipality[1].get('state_code')}) - {max_municipality[1].get('harvested_area')} hectares")

                # Mostrar top 5 municípios para verificação
                print(f"Debug - Top 5 municípios produtores de {crop_name}:")
                for i, (code, data) in enumerate(sorted_municipalities[:5]):
                    print(f"  {i+1}. {data.get('municipality_name')} ({data.get('state_code')}): {data.get('harvested_area')} ha - Código: {code}")
            else:
                print(f"Debug - Nenhum município válido encontrado para {crop_name}")

            return jsonify({
                'success': True,
                'data': crop_municipalities
            })

        # Busca similar se não encontrar exata
        crop_name_lower = crop_name.lower()
        similar_crops = []

        for available_crop in CROP_DATA.keys():
            if crop_name_lower in available_crop.lower() or available_crop.lower() in crop_name_lower:
                similar_crops.append(available_crop)

        if similar_crops:
            # Usar a primeira cultura similar encontrada
            best_match = similar_crops[0]
            all_crop_data = CROP_DATA[best_match]

            # Filtrar apenas municípios válidos (códigos IBGE reais de municípios)
            crop_municipalities = {}
            for municipality_code, municipality_data in all_crop_data.items():
                municipality_code_str = str(municipality_code)
                municipality_name = municipality_data.get('municipality_name', '').lower()

                # Verificar se é um código de município válido
                # Códigos de município IBGE começam com 1-5 e têm 7 dígitos
                # Excluir códigos que começam com 0 (são agregações regionais)
                if (len(municipality_code_str) == 7 and 
                    municipality_code_str.isdigit() and
                    municipality_code_str[0] in '12345' and  # Códigos reais começam com 1-5
                    municipality_data.get('municipality_name') and
                    # Excluir nomes que indicam regiões/agregações
                    not any(keyword in municipality_name for keyword in [
                        'região', 'mesorregião', 'microrregião', 'nordeste', 'norte', 'sul', 
                        'centro', 'oeste', 'leste', 'sudeste', 'noroeste', 'sudoeste',
                        'alto ', 'baixo ', 'médio ', '-grossense', 'parecis', 'araguaia',
                        'pantanal', 'cerrado', 'amazônia', 'caatinga', 'mata atlântica'
                    ]) and
                    # Excluir nomes muito genéricos ou que são claramente regiões
                    municipality_name not in [
                        'alto teles pires', 'sudeste mato-grossense', 'parecis', 'barreiras',
                        'dourados', 'norte mato-grossense', 'portal da amazônia'
                    ]):
                    crop_municipalities[municipality_code] = municipality_data

            # Debug: Encontrar o maior produtor para verificação
            if crop_municipalities:
                # Ordenar por área colhida para debug
                sorted_municipalities = sorted(crop_municipalities.items(), 
                                             key=lambda x: float(x[1].get('harvested_area', 0)), 
                                             reverse=True)
                max_municipality = sorted_municipalities[0]
                print(f"Debug - Maior produtor de {best_match} (apenas municípios): {max_municipality[1].get('municipality_name')} ({max_municipality[1].get('state_code')}) - {max_municipality[1].get('harvested_area')} hectares")

                # Mostrar top 5 municípios para verificação
                print(f"Debug - Top 5 municípios produtores de {best_match}:")
                for i, (code, data) in enumerate(sorted_municipalities[:5]):
                    print(f"  {i+1}. {data.get('municipality_name')} ({data.get('state_code')}): {data.get('harvested_area')} ha - Código: {code}")
            else:
                print(f"Debug - Nenhum município válido encontrado para {best_match}")

            return jsonify({
                'success': True,
                'data': crop_municipalities,
                'matched_crop': best_match
            })

        return jsonify({'success': False, 'error': 'Cultura não encontrada'})

    except Exception as e:
        print(f"Erro crítico em get_crop_data: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/crop-chart-data/<crop_name>')
def get_crop_chart_data(crop_name):
    try:
        if crop_name not in CROP_DATA:
            return jsonify({'success': False, 'error': 'Cultura não encontrada'})

        crop_municipalities = []
        for municipality_code, municipality_data in CROP_DATA[crop_name].items():
            # Filtrar apenas municípios válidos (códigos IBGE reais de municípios)
            municipality_code_str = str(municipality_code)
            municipality_name = municipality_data.get('municipality_name', '').lower()

            # Verificar se é um código de município válido
            # Códigos de município IBGE começam com 1-5 e têm 7 dígitos
            # Excluir códigos que começam com 0 (são agregações regionais)
            if (len(municipality_code_str) == 7 and 
                municipality_code_str.isdigit() and
                municipality_code_str[0] in '12345' and  # Códigos reais começam com 1-5
                municipality_data.get('municipality_name') and
                # Excluir nomes que indicam regiões/agregações
                not any(keyword in municipality_name for keyword in [
                    'região', 'mesorregião', 'microrregião', 'nordeste', 'norte', 'sul', 
                    'centro', 'oeste', 'leste', 'sudeste', 'noroeste', 'sudoeste',
                    'alto ', 'baixo ', 'médio ', '-grossense', 'parecis', 'araguaia',
                    'pantanal', 'cerrado', 'amazônia', 'caatinga', 'mata atlântica'
                ]) and
                # Excluir nomes muito genéricos ou que são claramente regiões
                municipality_name not in [
                    'alto teles pires', 'sudeste mato-grossense', 'parecis', 'barreiras',
                    'dourados', 'norte mato-grossense', 'portal da amazônia'
                ]):
                crop_municipalities.append({
                    'municipality_name': municipality_data.get('municipality_name', 'Desconhecido'),
                    'state_code': municipality_data.get('state_code', 'XX'),
                    'harvested_area': municipality_data.get('harvested_area', 0)
                })

        # Sort by harvested area and take top 20
        crop_municipalities.sort(key=lambda x: x['harvested_area'], reverse=True)
        top_20 = crop_municipalities[:20]

        chart_data = {
            'labels': [f"{muni['municipality_name']} ({muni['state_code']})" for muni in top_20],
            'data': [muni['harvested_area'] for muni in top_20]
        }

        return jsonify({
            'success': True,
            'chart_data': chart_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/analysis/statistical-summary/<crop_name>')
def get_statistical_summary(crop_name):
    try:
        if crop_name not in CROP_DATA:
            return jsonify({'success': False, 'error': 'Cultura não encontrada'})

        # Filtrar apenas municípios válidos (códigos IBGE reais de municípios)
        values = []
        for municipality_code, data in CROP_DATA[crop_name].items():
            municipality_code_str = str(municipality_code)
            municipality_name = data.get('municipality_name', '').lower()

            # Verificar se é um código de município válido
            # Códigos de município IBGE começam com 1-5 e têm 7 dígitos
            # Excluir códigos que começam com 0 (são agregações regionais)
            if (len(municipality_code_str) == 7 and 
                municipality_code_str.isdigit() and
                municipality_code_str[0] in '12345' and  # Códigos reais começam com 1-5
                data.get('municipality_name') and
                # Excluir nomes que indicam regiões/agregações
                not any(keyword in municipality_name for keyword in [
                    'região', 'mesorregião', 'microrregião', 'nordeste', 'norte', 'sul', 
                    'centro', 'oeste', 'leste', 'sudeste', 'noroeste', 'sudoeste',
                    'alto ', 'baixo ', 'médio ', '-grossense', 'parecis', 'araguaia',
                    'pantanal', 'cerrado', 'amazônia', 'caatinga', 'mata atlântica'
                ]) and
                # Excluir nomes muito genéricos ou que são claramente regiões
                municipality_name not in [
                    'alto teles pires', 'sudeste mato-grossense', 'parecis', 'barreiras',
                    'dourados', 'norte mato-grossense', 'portal da amazônia'
                ]):
                values.append(data['harvested_area'])

        if not values:
            return jsonify({'success': False, 'error': 'Nenhum município válido encontrado para esta cultura'})

        import statistics
        summary = {
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'mode': statistics.mode(values) if len(set(values)) < len(values) else None,
            'std_dev': statistics.stdev(values) if len(values) > 1 else 0,
            'min': min(values),
            'max': max(values),
            'q1': statistics.quantiles(values, n=4)[0] if len(values) >= 4 else None,
            'q3': statistics.quantiles(values, n=4)[2] if len(values) >= 4 else None,
            'total': sum(values),
            'count': len(values)
        }

        return jsonify({
            'success': True,
            'summary': summary
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/analysis/by-state/<crop_name>')
def get_analysis_by_state(crop_name):
    try:
        if crop_name not in CROP_DATA:
            return jsonify({'success': False, 'error': 'Cultura não encontrada'})

        states_data = {}
        for municipality_code, municipality_data in CROP_DATA[crop_name].items():
            # Filtrar apenas municípios válidos (códigos IBGE reais de municípios)
            municipality_code_str = str(municipality_code)
            municipality_name = municipality_data.get('municipality_name', '').lower()

            # Verificar se é um código de município válido
            # Códigos de município IBGE começam com 1-5 e têm 7 dígitos
            # Excluir códigos que começam com 0 (são agregações regionais)
            if (len(municipality_code_str) == 7 and 
                municipality_code_str.isdigit() and
                municipality_code_str[0] in '12345' and  # Códigos reais começam com 1-5
                municipality_data.get('municipality_name') and
                # Excluir nomes que indicam regiões/agregações
                not any(keyword in municipality_name for keyword in [
                    'região', 'mesorregião', 'microrregião', 'nordeste', 'norte', 'sul', 
                    'centro', 'oeste', 'leste', 'sudeste', 'noroeste', 'sudoeste',
                    'alto ', 'baixo ', 'médio ', '-grossense', 'parecis', 'araguaia',
                    'pantanal', 'cerrado', 'amazônia', 'caatinga', 'mata atlântica'
                ]) and
                # Excluir nomes muito genéricos ou que são claramente regiões
                municipality_name not in [
                    'alto teles pires', 'sudeste mato-grossense', 'parecis', 'barreiras',
                    'dourados', 'norte mato-grossense', 'portal da amazônia'
                ]):

                state = municipality_data.get('state_code', 'XX')
                area = municipality_data.get('harvested_area', 0)

                if state not in states_data:
                    states_data[state] = {
                        'total_area': 0,
                        'municipalities_count': 0,
                        'max_area': 0,
                        'municipalities': []
                    }

                states_data[state]['total_area'] += area
                states_data[state]['municipalities_count'] += 1
                states_data[state]['max_area'] = max(states_data[state]['max_area'], area)
                states_data[state]['municipalities'].append({
                    'name': municipality_data.get('municipality_name'),
                    'area': area
                })

        # Calculate averages
        for state_data in states_data.values():
            state_data['average_area'] = state_data['total_area'] / state_data['municipalities_count']

        return jsonify({
            'success': True,
            'states_data': states_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/analysis/comparison/<crop1>/<crop2>')
def get_crop_comparison(crop1, crop2):
    try:
        if crop1 not in CROP_DATA or crop2 not in CROP_DATA:
            return jsonify({'success': False, 'error': 'Uma ou ambas culturas não encontradas'})

        # Get common municipalities
        common_municipalities = set(CROP_DATA[crop1].keys()) & set(CROP_DATA[crop2].keys())

        comparison_data = []
        for muni_code in common_municipalities:
            data1 = CROP_DATA[crop1][muni_code]
            data2 = CROP_DATA[crop2][muni_code]

            comparison_data.append({
                'municipality_code': muni_code,
                'municipality_name': data1.get('municipality_name'),
                'state_code': data1.get('state_code'),
                'crop1_area': data1.get('harvested_area', 0),
                'crop2_area': data2.get('harvested_area', 0),
                'ratio': data1.get('harvested_area', 0) / max(data2.get('harvested_area', 1), 1)
            })

        return jsonify({
            'success': True,
            'crop1': crop1,
            'crop2': crop2,
            'comparison_data': comparison_data,
            'common_municipalities': len(common_municipalities)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/brazilian-states')
def get_brazilian_states():
    """Get list of Brazilian states"""
    try:
        states = [
            {'code': 'AC', 'name': 'Acre'},
            {'code': 'AL', 'name': 'Alagoas'},
            {'code': 'AP', 'name': 'Amapá'},
            {'code': 'AM', 'name': 'Amazonas'},
            {'code': 'BA', 'name': 'Bahia'},
            {'code': 'CE', 'name': 'Ceará'},
            {'code': 'DF', 'name': 'Distrito Federal'},
            {'code': 'ES', 'name': 'Espírito Santo'},
            {'code': 'GO', 'name': 'Goiás'},
            {'code': 'MA', 'name': 'Maranhão'},
            {'code': 'MT', 'name': 'Mato Grosso'},
            {'code': 'MS', 'name': 'Mato Grosso do Sul'},
            {'code': 'MG', 'name': 'Minas Gerais'},
            {'code': 'PA', 'name': 'Pará'},
            {'code': 'PB', 'name': 'Paraíba'},
            {'code': 'PR', 'name': 'Paraná'},
            {'code': 'PE', 'name': 'Pernambuco'},
            {'code': 'PI', 'name': 'Piauí'},
            {'code': 'RJ', 'name': 'Rio de Janeiro'},
            {'code': 'RN', 'name': 'Rio Grande do Norte'},
            {'code': 'RS', 'name': 'Rio Grande do Sul'},
            {'code': 'RO', 'name': 'Rondônia'},
            {'code': 'RR', 'name': 'Roraima'},
            {'code': 'SC', 'name': 'Santa Catarina'},
            {'code': 'SP', 'name': 'São Paulo'},
            {'code': 'SE', 'name': 'Sergipe'},
            {'code': 'TO', 'name': 'Tocantins'}
        ]

        return jsonify({
            'success': True,
            'states': states
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/export/crops')
def export_crops_data():
    """Export complete crop database as Excel file"""
    return export_complete_data()

@app.route('/api/export/fertilizers')
def export_fertilizers_data():
    """Export complete fertilizer database as Excel file"""
    return export_complete_fertilizer_data()

@app.route('/api/export/complete-data')
def export_complete_data():
    """Export complete crop data as Excel file"""
    try:
        # Load the original Excel file
        excel_path = os.path.join('data', 'ibge_2023_hectares_colhidos.xlsx')

        if not os.path.exists(excel_path):
            # Try alternative path
            excel_path = os.path.join('attached_assets', 'IBGE - 2023 - BRASIL HECTARES COLHIDOS_1752980032040.xlsx')

        if not os.path.exists(excel_path):
            return jsonify({'success': False, 'error': 'Arquivo de dados não encontrado'}), 404

        # Read the Excel file
        df = pd.read_excel(excel_path)

        # Create a BytesIO object to store the Excel file
        output = io.BytesIO()

        # Write to Excel
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Culturas IBGE 2023', index=False)

        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='base_completa_culturas_ibge_2023.xlsx'
        )

    except Exception as e:
        print(f"Erro ao exportar dados: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export/complete-fertilizer-data')
def export_complete_fertilizer_data():
    """Export complete fertilizer database as Excel file"""
    try:
        # Preparar todos os dados de fertilizantes para exportação
        all_fertilizer_data = []

        for category_name, category_data in FERTILIZER_DATA.items():
            for municipality_code, municipality_data in category_data.items():
                # Filtrar apenas municípios válidos
                municipality_code_str = str(municipality_code)
                municipality_name = municipality_data.get('municipality_name', '').lower()

                if (len(municipality_code_str) == 7 and 
                    municipality_code_str.isdigit() and
                    municipality_code_str[0] in '12345' and
                    municipality_data.get('municipality_name') and
                    not any(keyword in municipality_name for keyword in [
                        'região', 'mesorregião', 'microrregião', 'nordeste', 'norte', 'sul', 
                        'centro', 'oeste', 'leste', 'sudeste', 'noroeste', 'sudoeste',
                        'alto ', 'baixo ', 'médio ', '-grossense', 'parecis', 'araguaia',
                        'pantanal', 'cerrado', 'amazônia', 'caatinga', 'mata atlântica'
                    ])):

                    all_fertilizer_data.append({
                        'Código IBGE': municipality_code,
                        'Município': municipality_data.get('municipality_name', 'Desconhecido'),
                        'UF': municipality_data.get('state_code', 'XX'),
                        'Categoria': category_name,
                        'Valor': municipality_data.get('value', 0),
                        'Unidade': 'estabelecimentos',
                        'Ano': 2023
                    })

        # Ordenar por categoria e depois por valor
        all_fertilizer_data.sort(key=lambda x: (x['Categoria'], -x['Valor']))

        # Criar DataFrame principal
        df_main = pd.DataFrame(all_fertilizer_data)

        # Criar resumo por categoria
        category_summary = df_main.groupby('Categoria').agg({
            'Valor': ['sum', 'count', 'mean', 'max', 'min']
        }).round(2)
        category_summary.columns = ['Valor Total', 'Nº Municípios', 'Valor Médio', 'Valor Máximo', 'Valor Mínimo']
        category_summary = category_summary.sort_values('Valor Total', ascending=False)
        category_summary.reset_index(inplace=True)

        # Criar resumo por estado
        state_summary = df_main.groupby('UF').agg({
            'Valor': ['sum', 'count', 'mean']
        }).round(2)
        state_summary.columns = ['Valor Total', 'Nº Municípios', 'Valor Médio']
        state_summary = state_summary.sort_values('Valor Total', ascending=False)
        state_summary.reset_index(inplace=True)

        # Criar dados de resumo geral
        total_categories = df_main['Categoria'].nunique()
        total_municipalities = df_main['Código IBGE'].nunique()
        total_records = len(df_main)
        total_value = df_main['Valor'].sum()
        avg_value = df_main['Valor'].mean()

        general_summary = pd.DataFrame([
            ['Estatística', 'Valor'],
            ['Base de Dados', 'Fertilizantes - Censo Agropecuário 2017'],
            ['Ano de Referência', 2023],
            ['Total de Categorias', total_categories],
            ['Total de Municípios', total_municipalities],
            ['Total de Registros', total_records],
            ['Valor Total Geral', f'{total_value:,.0f}'],
            ['Valor Médio Geral', f'{avg_value:,.2f}'],
            ['Data da Exportação', pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')]
        ])

        # Criar arquivo Excel
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Planilha principal com todos os dados
            df_main.to_excel(writer, sheet_name='Dados Completos', index=False)

            # Planilha de resumo geral
            general_summary.to_excel(writer, sheet_name='Resumo Geral', index=False, header=False)

            # Planilha de resumo por categoria
            category_summary.to_excel(writer, sheet_name='Resumo por Categoria', index=False)

            # Planilha de resumo por estado
            state_summary.to_excel(writer, sheet_name='Resumo por Estado', index=False)

            # Criar planilhas separadas para cada categoria (máximo 10 categorias principais)
            top_categories = category_summary.head(10)
            for _, category_row in top_categories.iterrows():
                category_name = category_row['Categoria']
                safe_name = category_name.replace('/', '_').replace('\\', '_').replace(':', '_')[:30]

                category_df = df_main[df_main['Categoria'] == category_name].copy()
                category_df = category_df.sort_values('Valor', ascending=False)

                try:
                    category_df.to_excel(writer, sheet_name=safe_name, index=False)
                except Exception as e:
                    print(f"Erro ao criar planilha para categoria {category_name}: {e}")

        output.seek(0)

        # Nome do arquivo
        filename = f'base_completa_fertilizantes_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        print(f"Erro ao exportar base completa de fertilizantes: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export/fertilizer-analysis/<category_name>')
def export_fertilizer_analysis(category_name):
    """Export fertilizer analysis data as Excel file"""
    try:
        # Obter parâmetro de estado opcional
        state_filter = request.args.get('state')

        if category_name not in FERTILIZER_DATA:
            return jsonify({'success': False, 'error': 'Categoria de fertilizantes não encontrada'}), 404

        # Preparar dados para exportação
        analysis_data = []
        for municipality_code, municipality_data in FERTILIZER_DATA[category_name].items():
            # Filtrar apenas municípios válidos
            municipality_code_str = str(municipality_code)
            municipality_name = municipality_data.get('municipality_name', '').lower()

            if (len(municipality_code_str) == 7 and 
                municipality_code_str.isdigit() and
                municipality_code_str[0] in '12345' and
                municipality_data.get('municipality_name') and
                not any(keyword in municipality_name for keyword in [
                    'região', 'mesorregião', 'microrregião', 'nordeste', 'norte', 'sul', 
                    'centro', 'oeste', 'leste', 'sudeste', 'noroeste', 'sudoeste',
                    'alto ', 'baixo ', 'médio ', '-grossense', 'parecis', 'araguaia',
                    'pantanal', 'cerrado', 'amazônia', 'caatinga', 'mata atlântica'
                ])):

                # Aplicar filtro de estado se especificado
                if state_filter and municipality_data.get('state_code') != state_filter:
                    continue

                analysis_data.append({
                    'Código IBGE': municipality_code,
                    'Município': municipality_data.get('municipality_name', 'Desconhecido'),
                    'UF': municipality_data.get('state_code', 'XX'),
                    'Categoria': category_name,
                    'Valor': municipality_data.get('value', 0),
                    'Unidade': 'estabelecimentos',
                    'Ano': 2023
                })

        # Ordenar por valor (maior para menor)
        analysis_data.sort(key=lambda x: x['Valor'], reverse=True)

        # Criar DataFrame
        df = pd.DataFrame(analysis_data)

        # Calcular estatísticas resumidas
        total_value = df['Valor'].sum()
        total_municipalities = len(df)
        average_value = df['Valor'].mean()
        max_value = df['Valor'].max()
        min_value = df['Valor'].min()

        # Criar dados de resumo estatístico
        summary_data = [
            ['Estatística', 'Valor'],
            ['Categoria Analisada', category_name],
            ['Filtro de Estado', state_filter if state_filter else 'Nacional (Todos os Estados)'],
            ['Ano de Referência', 2023],
            ['Total de Municípios', total_municipalities],
            ['Valor Total', f'{total_value:,.0f}'],
            ['Valor Médio por Município', f'{average_value:,.2f}'],
            ['Maior Valor Municipal', f'{max_value:,.0f}'],
            ['Menor Valor Municipal', f'{min_value:,.0f}'],
            ['Data da Exportação', pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')]
        ]

        # Criar resumo por estado
        state_summary = df.groupby('UF').agg({
            'Valor': ['sum', 'count', 'mean']
        }).round(2)
        state_summary.columns = ['Valor Total', 'Nº Municípios', 'Valor Médio']
        state_summary = state_summary.sort_values('Valor Total', ascending=False)
        state_summary.reset_index(inplace=True)

        # Criar arquivo Excel
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Planilha principal com dados detalhados
            df.to_excel(writer, sheet_name='Dados Detalhados', index=False)

            # Planilha de resumo estatístico
            summary_df = pd.DataFrame(summary_data[1:], columns=summary_data[0])
            summary_df.to_excel(writer, sheet_name='Resumo Estatístico', index=False)

            # Planilha de resumo por estado
            state_summary.to_excel(writer, sheet_name='Resumo por Estado', index=False)

            # Top 20 maiores estabelecimentos
            top_20 = df.head(20).copy()
            top_20['Ranking'] = range(1, len(top_20) + 1)
            top_20 = top_20[['Ranking', 'Município', 'UF', 'Valor', 'Unidade']]
            top_20.to_excel(writer, sheet_name='Top 20', index=False)

        output.seek(0)

        # Nome do arquivo
        safe_category_name = category_name.replace('/', '_').replace('\\', '_').replace(':', '_')
        state_suffix = f'_{state_filter}' if state_filter else '_Nacional'
        filename = f'analise_{safe_category_name}{state_suffix}_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        print(f"Erro ao exportar análise de fertilizantes: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export/crop-analysis/<crop_name>')
def export_crop_analysis(crop_name):
    """Export crop analysis data as Excel file"""
    try:
        # Obter parâmetro de estado opcional
        state_filter = request.args.get('state')

        if crop_name not in CROP_DATA:
            return jsonify({'success': False, 'error': 'Cultura não encontrada'}), 404

        # Preparar dados para exportação
        analysis_data = []
        for municipality_code, municipality_data in CROP_DATA[crop_name].items():
            # Filtrar apenas municípios válidos
            municipality_code_str = str(municipality_code)
            municipality_name = municipality_data.get('municipality_name', '').lower()

            if (len(municipality_code_str) == 7 and 
                municipality_code_str.isdigit() and
                municipality_code_str[0] in '12345' and
                municipality_data.get('municipality_name') and
                not any(keyword in municipality_name for keyword in [
                    'região', 'mesorregião', 'microrregião', 'nordeste', 'norte', 'sul', 
                    'centro', 'oeste', 'leste', 'sudeste', 'noroeste', 'sudoeste',
                    'alto ', 'baixo ', 'médio ', '-grossense', 'parecis', 'araguaia',
                    'pantanal', 'cerrado', 'amazônia', 'caatinga', 'mata atlântica'
                ]) and
                municipality_name not in [
                    'alto teles pires', 'sudeste mato-grossense', 'parecis', 'barreiras',
                    'dourados', 'norte mato-grossense', 'portal da amazônia'
                ]):

                # Aplicar filtro de estado se especificado
                if state_filter and municipality_data.get('state_code') != state_filter:
                    continue

                analysis_data.append({
                    'Código IBGE': municipality_code,
                    'Município': municipality_data.get('municipality_name', 'Desconhecido'),
                    'UF': municipality_data.get('state_code', 'XX'),
                    'Cultura': crop_name,
                    'Área Colhida (hectares)': municipality_data.get('harvested_area', 0),
                    'Ano': 2023
                })

        # Ordenar por área colhida (maior para menor)
        analysis_data.sort(key=lambda x: x['Área Colhida (hectares)'], reverse=True)

        # Criar DataFrame
        df = pd.DataFrame(analysis_data)

        # Calcular estatísticas resumidas
        total_area = df['Área Colhida (hectares)'].sum()
        total_municipalities = len(df)
        average_area = df['Área Colhida (hectares)'].mean()
        max_area = df['Área Colhida (hectares)'].max()
        min_area = df['Área Colhida (hectares)'].min()

        # Criar dados de resumo estatístico
        summary_data = [
            ['Estatística', 'Valor'],
            ['Cultura Analisada', crop_name],
            ['Filtro de Estado', state_filter if state_filter else 'Nacional (Todos os Estados)'],
            ['Ano de Referência', 2023],
            ['Total de Municípios', total_municipalities],
            ['Área Total Colhida (ha)', f'{total_area:,.2f}'],
            ['Área Média por Município (ha)', f'{average_area:,.2f}'],
            ['Maior Área Municipal (ha)', f'{max_area:,.2f}'],
            ['Menor Área Municipal (ha)', f'{min_area:,.2f}'],
            ['Data da Exportação', pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')]
        ]

        # Criar resumo por estado
        state_summary = df.groupby('UF').agg({
            'Área Colhida (hectares)': ['sum', 'count', 'mean']
        }).round(2)
        state_summary.columns = ['Área Total (ha)', 'Nº Municípios', 'Área Média (ha)']
        state_summary = state_summary.sort_values('Área Total (ha)', ascending=False)
        state_summary.reset_index(inplace=True)

        # Criar arquivo Excel
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Planilha principal com dados detalhados
            df.to_excel(writer, sheet_name='Dados Detalhados', index=False)

            # Planilha de resumo estatístico
            summary_df = pd.DataFrame(summary_data[1:], columns=summary_data[0])
            summary_df.to_excel(writer, sheet_name='Resumo Estatístico', index=False)

            # Planilha de resumo por estado
            state_summary.to_excel(writer, sheet_name='Resumo por Estado', index=False)

            # Top 20 maiores produtores
            top_20 = df.head(20).copy()
            top_20['Ranking'] = range(1, len(top_20) + 1)
            top_20 = top_20[['Ranking', 'Município', 'UF', 'Área Colhida (hectares)']]
            top_20.to_excel(writer, sheet_name='Top 20 Produtores', index=False)

        output.seek(0)

        # Nome do arquivo
        safe_crop_name = crop_name.replace('/', '_').replace('\\', '_').replace(':', '_')
        state_suffix = f'_{state_filter}' if state_filter else '_Nacional'
        filename = f'analise_{safe_crop_name}{state_suffix}_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        print(f"Erro ao exportar análise: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export/agrotoxico-analysis/<category>')
def export_agrotoxico_analysis(category):
    """Export agrotóxico analysis data as Excel file"""
    try:
        state_filter = request.args.get('state')

        if category not in AGROTOXICO_DATA:
            return jsonify({'success': False, 'error': 'Categoria de agrotóxico não encontrada'}), 404

        analysis_data = []
        for municipality_code, municipality_data in AGROTOXICO_DATA[category].items():
            municipality_code_str = str(municipality_code)
            municipality_name = municipality_data.get('municipality_name', '').lower()

            if (len(municipality_code_str) == 7 and 
                municipality_code_str.isdigit() and
                municipality_code_str[0] in '12345' and
                municipality_data.get('municipality_name')):

                if state_filter and municipality_data.get('state_code') != state_filter:
                    continue

                analysis_data.append({
                    'Código IBGE': municipality_code,
                    'Município': municipality_data.get('municipality_name', 'Desconhecido'),
                    'UF': municipality_data.get('state_code', 'XX'),
                    'Categoria': category,
                    'Valor': municipality_data.get('value', 0),
                    'Unidade': municipality_data.get('unit', 'un'),
                    'Ano': 2023
                })

        analysis_data.sort(key=lambda x: x['Valor'], reverse=True)
        df = pd.DataFrame(analysis_data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Dados Detalhados', index=False)

        output.seek(0)
        safe_category_name = category.replace('/', '_').replace('\\', '_').replace(':', '_')
        state_suffix = f'_{state_filter}' if state_filter else '_Nacional'
        filename = f'analise_agrotoxico_{safe_category_name}{state_suffix}_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        print(f"Erro ao exportar análise de agrotóxico: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export/consultoria-analysis/<category>')
def export_consultoria_analysis(category):
    """Export consultoria analysis data as Excel file"""
    try:
        state_filter = request.args.get('state')

        if category not in CONSULTORIA_DATA:
            return jsonify({'success': False, 'error': 'Categoria de consultoria não encontrada'}), 404

        analysis_data = []
        for municipality_code, municipality_data in CONSULTORIA_DATA[category].items():
            municipality_code_str = str(municipality_code)

            if (len(municipality_code_str) == 7 and 
                municipality_code_str.isdigit() and
                municipality_code_str[0] in '12345' and
                municipality_data.get('municipality_name')):

                if state_filter and municipality_data.get('state_code') != state_filter:
                    continue

                analysis_data.append({
                    'Código IBGE': municipality_code,
                    'Município': municipality_data.get('municipality_name', 'Desconhecido'),
                    'UF': municipality_data.get('state_code', 'XX'),
                    'Categoria': category,
                    'Valor': municipality_data.get('value', 0),
                    'Unidade': municipality_data.get('unit', 'un'),
                    'Ano': 2023
                })

        analysis_data.sort(key=lambda x: x['Valor'], reverse=True)
        df = pd.DataFrame(analysis_data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Dados Detalhados', index=False)

        output.seek(0)
        safe_category_name = category.replace('/', '_').replace('\\', '_').replace(':', '_')
        state_suffix = f'_{state_filter}' if state_filter else '_Nacional'
        filename = f'analise_consultoria_{safe_category_name}{state_suffix}_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        print(f"Erro ao exportar análise de consultoria: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export/corretivos-analysis/<category>')
def export_corretivos_analysis(category):
    """Export corretivos analysis data as Excel file"""
    try:
        state_filter = request.args.get('state')

        if category not in CORRETIVOS_DATA:
            return jsonify({'success': False, 'error': 'Categoria de corretivo não encontrada'}), 404

        analysis_data = []
        for municipality_code, municipality_data in CORRETIVOS_DATA[category].items():
            municipality_code_str = str(municipality_code)

            if (len(municipality_code_str) == 7 and 
                municipality_code_str.isdigit() and
                municipality_code_str[0] in '12345' and
                municipality_data.get('municipality_name')):

                if state_filter and municipality_data.get('state_code') != state_filter:
                    continue

                analysis_data.append({
                    'Código IBGE': municipality_code,
                    'Município': municipality_data.get('municipality_name', 'Desconhecido'),
                    'UF': municipality_data.get('state_code', 'XX'),
                    'Categoria': category,
                    'Valor': municipality_data.get('value', 0),
                    'Unidade': municipality_data.get('unit', 'un'),
                    'Ano': 2023
                })

        analysis_data.sort(key=lambda x: x['Valor'], reverse=True)
        df = pd.DataFrame(analysis_data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Dados Detalhados', index=False)

        output.seek(0)
        safe_category_name = category.replace('/', '_').replace('\\', '_').replace(':', '_')
        state_suffix = f'_{state_filter}' if state_filter else '_Nacional'
        filename = f'analise_corretivo_{safe_category_name}{state_suffix}_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        print(f"Erro ao exportar análise de corretivo: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export/despesa-analysis/<category>')
def export_despesa_analysis(category):
    """Export despesa analysis data as Excel file"""
    try:
        state_filter = request.args.get('state')

        if category not in DESPESA_DATA:
            return jsonify({'success': False, 'error': 'Categoria de despesa não encontrada'}), 404

        analysis_data = []
        for municipality_code, municipality_data in DESPESA_DATA[category].items():
            municipality_code_str = str(municipality_code)

            if (len(municipality_code_str) == 7 and 
                municipality_code_str.isdigit() and
                municipality_code_str[0] in '12345' and
                municipality_data.get('municipality_name')):

                if state_filter and municipality_data.get('state_code') != state_filter:
                    continue

                analysis_data.append({
                    'Código IBGE': municipality_code,
                    'Município': municipality_data.get('municipality_name', 'Desconhecido'),
                    'UF': municipality_data.get('state_code', 'XX'),
                    'Categoria': category,
                    'Valor': municipality_data.get('value', 0),
                    'Unidade': municipality_data.get('unit', 'R$'),
                    'Ano': 2023
                })

        analysis_data.sort(key=lambda x: x['Valor'], reverse=True)
        df = pd.DataFrame(analysis_data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Dados Detalhados', index=False)

        output.seek(0)
        safe_category_name = category.replace('/', '_').replace('\\', '_').replace(':', '_')
        state_suffix = f'_{state_filter}' if state_filter else '_Nacional'
        filename = f'analise_despesa_{safe_category_name}{state_suffix}_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        print(f"Erro ao exportar análise de despesa: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export/escolaridade-analysis/<category>')
def export_escolaridade_analysis(category):
    """Export escolaridade analysis data as Excel file"""
    try:
        state_filter = request.args.get('state')

        if category not in ESCOLARIDADE_DATA:
            return jsonify({'success': False, 'error': 'Categoria de escolaridade não encontrada'}), 404

        analysis_data = []
        for municipality_code, municipality_data in ESCOLARIDADE_DATA[category].items():
            municipality_code_str = str(municipality_code)

            if (len(municipality_code_str) == 7 and 
                municipality_code_str.isdigit() and
                municipality_code_str[0] in '12345' and
                municipality_data.get('municipality_name')):

                if state_filter and municipality_data.get('state_code') != state_filter:
                    continue

                analysis_data.append({
                    'Código IBGE': municipality_code,
                    'Município': municipality_data.get('municipality_name', 'Desconhecido'),
                    'UF': municipality_data.get('state_code', 'XX'),
                    'Categoria': category,
                    'Valor': municipality_data.get('value', 0),
                    'Unidade': municipality_data.get('unit', 'un'),
                    'Ano': 2023
                })

        analysis_data.sort(key=lambda x: x['Valor'], reverse=True)
        df = pd.DataFrame(analysis_data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Dados Detalhados', index=False)

        output.seek(0)
        safe_category_name = category.replace('/', '_').replace('\\', '_').replace(':', '_')
        state_suffix = f'_{state_filter}' if state_filter else '_Nacional'
        filename = f'analise_escolaridade_{safe_category_name}{state_suffix}_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        print(f"Erro ao exportar análise de escolaridade: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export/receita-analysis/<category>')
def export_receita_analysis(category):
    """Export receita analysis data as Excel file"""
    try:
        state_filter = request.args.get('state')

        if category not in RECEITA_DATA:
            return jsonify({'success': False, 'error': 'Categoria de receita não encontrada'}), 404

        analysis_data = []
        for municipality_code, municipality_data in RECEITA_DATA[category].items():
            municipality_code_str = str(municipality_code)

            if (len(municipality_code_str) == 7 and 
                municipality_code_str.isdigit() and
                municipality_code_str[0] in '12345' and
                municipality_data.get('municipality_name')):

                if state_filter and municipality_data.get('state_code') != state_filter:
                    continue

                analysis_data.append({
                    'Código IBGE': municipality_code,
                    'Município': municipality_data.get('municipality_name', 'Desconhecido'),
                    'UF': municipality_data.get('state_code', 'XX'),
                    'Categoria': category,
                    'Valor': municipality_data.get('value', 0),
                    'Unidade': municipality_data.get('unit', 'R$'),
                    'Ano': 2023
                })

        analysis_data.sort(key=lambda x: x['Valor'], reverse=True)
        df = pd.DataFrame(analysis_data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Dados Detalhados', index=False)

        output.seek(0)
        safe_category_name = category.replace('/', '_').replace('\\', '_').replace(':', '_')
        state_suffix = f'_{state_filter}' if state_filter else '_Nacional'
        filename = f'analise_receita_{safe_category_name}{state_suffix}_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        print(f"Erro ao exportar análise de receita: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Rotas de Autenticação
@app.route('/login')
def login_page():
    if auth_manager.is_authenticated():
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register')
def register_page():
    if auth_manager.is_authenticated():
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    try:
        data = request.get_json()

        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        full_name = data.get('full_name', '').strip()
        confirm_password = data.get('confirm_password', '')

        if password != confirm_password:
            return jsonify({'success': False, 'error': 'Senhas não coincidem'})

        result = auth_manager.register_user(username, email, password, full_name)
        return jsonify(result)

    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro interno: {str(e)}'})

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json()

        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not username or not password:
            return jsonify({'success': False, 'error': 'Username e senha são obrigatórios'})

        result = auth_manager.login_user(username, password)
        return jsonify(result)

    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro interno: {str(e)}'})

@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    try:
        result = auth_manager.logout_user()
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro interno: {str(e)}'})

@app.route('/api/auth/profile')
@login_required
def api_profile():
    try:
        user = auth_manager.get_current_user()
        return jsonify({'success': True, 'user': user})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro interno: {str(e)}'})

@app.route('/api/auth/change-password', methods=['POST'])
@login_required
def api_change_password():
    try:
        data = request.get_json()
        username = session.get('username')

        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')
        confirm_password = data.get('confirm_password', '')

        if new_password != confirm_password:
            return jsonify({'success': False, 'error': 'Senhas não coincidem'})

        result = auth_manager.change_password(username, old_password, new_password)
        return jsonify(result)

    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro interno: {str(e)}'})

@app.route('/logout')
def logout():
    auth_manager.logout_user()
    return redirect(url_for('login_page'))

@app.route('/profile')
@login_required
def profile_page():
    user = auth_manager.get_current_user()
    return render_template('profile.html', user=user)

# Rotas para Revendas
@app.route('/revendas')
@login_required
def revendas_page():
    user = auth_manager.get_current_user()
    return render_template('revendas.html', user=user)

# API endpoints para Revendas
@app.route('/api/revendas', methods=['GET'])
@login_required
def get_revendas():
    try:
        # Ensure tables exist
        with app.app_context():
            db.create_all()
        
        revendas = Revenda.query.filter_by(ativo=True).all()
        
        revendas_list = []
        for revenda in revendas:
            revendas_list.append({
                'id': revenda.id,
                'nome': revenda.nome,
                'cnpj': revenda.cnpj,
                'cnae': revenda.cnae,
                'cor': revenda.cor,
                'municipios': revenda.get_municipios_list(),
                'municipios_count': len(revenda.get_municipios_list()),
                'created_at': revenda.created_at.strftime('%d/%m/%Y')
            })
        
        return jsonify({
            'success': True,
            'revendas': revendas_list
        })
    except Exception as e:
        print(f"Erro ao carregar revendas: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/revendas', methods=['POST'])
@login_required
def create_revenda():
    try:
        data = request.get_json()
        print(f"Creating revenda with data: {data}")
        
        # Validar dados obrigatórios
        if not data.get('nome') or not data.get('cnpj') or not data.get('cnae'):
            return jsonify({'success': False, 'error': 'Nome, CNPJ e CNAE são obrigatórios'}), 400
        
        if not data.get('municipios') or len(data.get('municipios', [])) == 0:
            return jsonify({'success': False, 'error': 'Pelo menos um município deve ser selecionado'}), 400
        
        print(f"Municipalities to save: {data['municipios']}")
        
        # Verificar se CNPJ já existe
        existing_revenda = Revenda.query.filter_by(cnpj=data['cnpj']).first()
        if existing_revenda:
            return jsonify({'success': False, 'error': 'CNPJ já cadastrado'}), 400
        
        # Criar nova revenda
        revenda = Revenda(
            nome=data['nome'],
            cnpj=data['cnpj'],
            cnae=data['cnae'],
            cor=data.get('cor', '#4CAF50')
        )
        revenda.set_municipios_list(data['municipios'])
        
        print(f"Revenda created with municipalities: {revenda.get_municipios_list()}")
        
        db.session.add(revenda)
        db.session.commit()
        
        print(f"Revenda saved with ID: {revenda.id}")
        
        return jsonify({
            'success': True,
            'message': 'Revenda cadastrada com sucesso!',
            'revenda_id': revenda.id
        })
        
    except Exception as e:
        print(f"Error creating revenda: {str(e)}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/revendas/<int:revenda_id>', methods=['PUT'])
@login_required
def update_revenda(revenda_id):
    try:
        data = request.get_json()
        
        revenda = Revenda.query.get_or_404(revenda_id)
        
        # Atualizar campos
        if 'nome' in data:
            revenda.nome = data['nome']
        if 'cnae' in data:
            revenda.cnae = data['cnae']
        if 'cor' in data:
            revenda.cor = data['cor']
        if 'municipios' in data:
            revenda.set_municipios_list(data['municipios'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Revenda atualizada com sucesso!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/revendas/<int:revenda_id>', methods=['DELETE'])
@login_required
def delete_revenda(revenda_id):
    try:
        revenda = Revenda.query.get_or_404(revenda_id)
        
        # Soft delete - marcar como inativo
        revenda.ativo = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Revenda removida com sucesso!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/municipios/search')
@login_required
def search_municipios():
    try:
        query = request.args.get('q', '').lower()
        if len(query) < 2:
            return jsonify({'success': False, 'error': 'Query muito curta'}), 400
        
        # Buscar municípios nos dados de culturas para obter nomes reais
        municipios_found = []
        municipios_set = set()  # Para evitar duplicatas
        
        # Buscar nos dados de culturas
        for crop_name, crop_data in CROP_DATA.items():
            for municipality_code, municipality_data in crop_data.items():
                municipality_code_str = str(municipality_code)
                municipality_name = municipality_data.get('municipality_name', '').lower()
                state_code = municipality_data.get('state_code', 'XX')
                
                # Verificar se é um código de município válido e se contém a query
                if (len(municipality_code_str) == 7 and 
                    municipality_code_str.isdigit() and
                    municipality_code_str[0] in '12345' and
                    municipality_data.get('municipality_name') and
                    municipality_code not in municipios_set and
                    (query in municipality_name or query in state_code.lower())):
                    
                    municipios_found.append({
                        'code': municipality_code,
                        'name': municipality_data.get('municipality_name'),
                        'state': state_code,
                        'full_name': f"{municipality_data.get('municipality_name')} ({state_code})"
                    })
                    municipios_set.add(municipality_code)
                    
                    # Limitar a 50 resultados para performance
                    if len(municipios_found) >= 50:
                        break
            
            if len(municipios_found) >= 50:
                break
        
        # Ordenar por nome
        municipios_found.sort(key=lambda x: x['name'])
        
        return jsonify({
            'success': True,
            'municipios': municipios_found[:20]  # Limitar a 20 resultados
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/revendas/data/<int:revenda_id>')
@login_required
def get_revenda_territory_data(revenda_id):
    try:
        # Ensure tables exist
        with app.app_context():
            db.create_all()
            
        revenda = Revenda.query.get_or_404(revenda_id)
        print(f"Loading territory data for revenda: {revenda.nome} (ID: {revenda_id})")
        
        # Obter lista de municípios da revenda
        municipios_codes = revenda.get_municipios_list()
        print(f"Municipality codes from revenda: {municipios_codes}")
        
        if not municipios_codes:
            print("No municipalities found for this revenda")
            return jsonify({'success': False, 'error': 'Nenhum município cadastrado para esta revenda'}), 400
        
        # Buscar dados reais dos municípios nos dados de culturas
        territory_data = {}
        municipalities_found = 0
        
        for code in municipios_codes:
            code_str = str(code)
            # Buscar informações do município nos dados disponíveis
            municipality_name = f"Município {code}"
            state_code = "XX"
            found = False
            
            # Procurar nos dados de culturas para obter nomes reais
            for crop_name, crop_data in CROP_DATA.items():
                if code_str in crop_data:
                    municipality_data = crop_data[code_str]
                    municipality_name = municipality_data.get('municipality_name', municipality_name)
                    state_code = municipality_data.get('state_code', state_code)
                    found = True
                    municipalities_found += 1
                    print(f"Found municipality {code}: {municipality_name} ({state_code}) in crop {crop_name}")
                    break
            
            if not found:
                print(f"Municipality {code} not found in crop data, using default name")
            
            territory_data[code_str] = {
                'municipality_name': municipality_name,
                'state_code': state_code,
                'harvested_area': 1,  # Valor fixo compatível com outros dados
                'unit': 'território'
            }
        
        print(f"Territory data created for {len(territory_data)} municipalities ({municipalities_found} found in crop data)")
        print(f"Territory data keys: {list(territory_data.keys())}")
        
        return jsonify({
            'success': True,
            'data': territory_data,
            'type': 'revendas'
        })
        
    except Exception as e:
        print(f"Erro ao carregar dados de território da revenda {revenda_id}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

# Definir todas as tabelas antes de importar routes
class Revenda(db.Model):
    __tablename__ = 'revenda'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    cnpj = db.Column(db.String(18), nullable=False, unique=True)
    cnae = db.Column(db.String(10), nullable=False)
    municipios = db.Column(db.Text, nullable=False)  # JSON string com lista de códigos de municípios
    cor = db.Column(db.String(7), nullable=False, default='#4CAF50')  # Cor hex para visualização
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Revenda {self.nome}>'

    def get_municipios_list(self):
        """Retorna lista de códigos de municípios"""
        import json
        try:
            return json.loads(self.municipios) if self.municipios else []
        except:
            return []

    def set_municipios_list(self, municipios_list):
        """Define lista de códigos de municípios"""
        import json
        self.municipios = json.dumps(municipios_list)

# Create tables
with app.app_context():
    db.create_all()
    print("Tabelas criadas com sucesso!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)