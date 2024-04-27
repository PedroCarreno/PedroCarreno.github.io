import webbrowser

import dash
from dash import dcc, html, Input, Output, State
from dash import dash_table
import os
import sys
# Obtener la ruta absoluta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construir la ruta al directorio site-packages
site_packages_dir = os.path.join(current_dir, '.venv', 'Lib', 'site-packages')
# Agregar la ruta al directorio de site-packages al sys.path
sys.path.append(site_packages_dir)
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from calculos import simular_ausentismo

# Crear la aplicación Dash
app = dash.Dash(__name__)
server = app.server
# Definir la lista de nombres para los campos de entrada
nombres_input = ['0', '1', '2', '3', '4', '5 o más']

# Definir la lista de IDs para los campos de entrada
ids_input = [f'input-{i}-operarios' for i in range(6)]


# Crear los campos de entrada para los datos de ausentismo de operarios
def crear_campos_ausentismo():
    valor_predeterminado = [36, 38, 19, 6, 1, 0]
    campos_ausentismo = []
    for i, (nombre, id_input, valor) in enumerate(zip(nombres_input, ids_input, valor_predeterminado)):
        valor_ingresado = dcc.Input(id=id_input, type='number', placeholder='', min=0, step=1, style={'width': '50px'},
                                    value=valor)
        frec_acum = html.Div(id=f'frec-acum-{i}')
        frec_rel = html.Div(id=f'frec-rel-{i}')
        frec_rel_acum = html.Div(id=f'frec-rel-acum-{i}')
        campos_ausentismo.append(html.Tr([
            html.Td(nombre),
            html.Td(valor_ingresado),
            html.Td(frec_acum, style={'padding-left': '1cm'}),
            html.Td(frec_rel, style={'padding-left': '1cm'}),
            html.Td(frec_rel_acum, style={'padding-left': '1cm'})
        ]))

        @app.callback(
            Output(f'frec-acum-{i}', 'children'),
            Output(f'frec-rel-{i}', 'children'),
            Output(f'frec-rel-acum-{i}', 'children'),
            [Input(id_input, 'value')] + [Input(f'input-{j}-operarios', 'value') for j in range(i)]
        )
        def calcular_frecuencias(valor_ingresado, *valores_ingresados):
            if valor_ingresado is not None and all(v is not None for v in valores_ingresados):
                frecuencia_acumulada_actual = int(valor_ingresado) + sum(valores_ingresados)
                frecuencia_relativa = int(valor_ingresado) / 100
                frecuencia_relativa_acumulada = frecuencia_acumulada_actual / 100
                return frecuencia_acumulada_actual, round(frecuencia_relativa,4), round(frecuencia_relativa_acumulada,4)
            else:
                return '-', '-', '-'

    return campos_ausentismo


# Usar la función para crear campos de ausentismo
campos_ausentismo = crear_campos_ausentismo()

# Definir el diseño de la aplicación
app.layout = html.Div([
    html.H1('Simulador de Ausentismo en Industria Automotriz',
            style={'text-align': 'center', 'font-family': 'Arial, sans-serif', 'color': '#333', 'font-size': '36px',
                   'margin-bottom': '20px'}),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.P('Datos de Ausentismo', style={'font-weight': 'bold','margin': 'auto', 'margin-bottom': '20px', 'text-align': 'center'}),
                html.Table([
                    html.Tr([
                        html.Td('Xi', style={'font-weight': 'bold'}),
                        html.Td('fi', style={'font-weight': 'bold'}),
                        html.Td('Fi', style={'font-weight': 'bold'}),
                        html.Td('fri', style={'font-weight': 'bold'}),
                        html.Td('Fri', style={'font-weight': 'bold'})
                    ]),
                    *campos_ausentismo
                ], style={'margin': 'auto', 'margin-bottom': '20px', 'text-align': 'center'}),
            ]),
            html.Div([
                html.P('Ventas ($)', style={'font-weight': 'bold'}),
                dcc.Input(id='input-venta', type='number', placeholder='', min=0, step=1, value=4000),
                html.P('Costos Variables ($)', style={'font-weight': 'bold'}),
                dcc.Input(id='input-costos', type='number', placeholder='', min=0, step=1, value=2400),
                html.P('SLECCIONAR Nomina de obreros:', style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='nomina-obreros',
                    options=[
                        {'label': '21', 'value': 21},
                        {'label': '22', 'value': 22},
                        {'label': '23', 'value': 23},
                        {'label': '24', 'value': 24}
                    ],
                    style={'width': '100px', 'margin': 'auto'},  # Ajusta el ancho aquí
                    value=24  # Valor predeterminado
                ),

                html.P('Remuneración/Obrero ($)', style={'font-weight': 'bold'}),
                dcc.Input(id='input-remuneracion', type='number', placeholder='', min=0, step=1, value=30),
                html.P('Valor de i', style={'font-weight': 'bold'}),
                dcc.Input(id='input-i', type='number', placeholder='', min=0, step=1, value=1),
                html.P('Valor de j', style={'font-weight': 'bold'}),
                dcc.Input(id='input-j', type='number', placeholder='', min=0, step=1, value=5),
                html.P('Cantidad de Días a Simular', style={'font-weight': 'bold'}),
                dcc.Input(id='input-total-dias', type='number', placeholder='', min=0, step=1, value=10),
                html.Button('Simular', id='button-simular', n_clicks=0, disabled=True, className='btn btn-primary',
                            style={'margin-left': '10px'}),
                html.Div(id='error-message', style={'color': 'red', 'margin': 'auto', 'text-align': 'center'}),
            ], style={'margin': 'auto', 'text-align': 'center'}),
            html.Div(id='resultado-simulacion', style={'text-align': 'center', 'margin-top': '10px'}),
        ], md=6),  # Tamaño medio en dispositivos medianos y grandes
        # Tercer bloque de resultados: Tabla de Resultados de la Simulación
        dbc.Col([
            dbc.Row([
                html.H3('    Resultados de la Simulación')
            ],style={'margin': 'auto','text-align': 'center'}),
            dbc.Row([
                dbc.Col([
                    dash_table.DataTable(
                        columns=[
                            {'name': 'Reloj Diario', 'id': 'reloj', 'type': 'numeric'},
                            {'name': 'RND U[0;1)', 'id': 'rnd', 'type': 'numeric'},
                            {'name': 'Cant. Ausentes', 'id': 'CantObrerosAusentes', 'type': 'numeric'},
                            {'name': 'Cant. Presentes', 'id': 'CantOperadores', 'type': 'numeric'},
                            {'name': 'Beneficio por dia ($)', 'id': 'Beneficio', 'type': 'numeric'},
                            {'name': 'Beneficio Total ($)', 'id': 'BeneficioAcum', 'type': 'numeric'},
                            {'name': 'Beneficio Promedio ($)', 'id': 'BeneficioPromedio', 'type': 'numeric'}
                        ],
                        data=[{}],
                        id='tabla-resultados',  # ID de la DataTable
                        fixed_rows={'headers': True, 'data': 0}, # Encabezados fijos
                        style_table={'overflowX': 'auto'}  # Configuración de ancho automático
                    )
                ])
            ]),
        ], id='pantalla-resultados', style={'margin-right': '20px', 'text-align': 'center', 'display': 'none'}),
    ], justify="center"),  # Centrar el contenido

])


@app.callback(
    [Output('button-simular', 'disabled'),
     Output('error-message', 'children')],
    [Input(f'input-{i}-operarios', 'value') for i in range(6)] +
    [Input('input-i', 'value'),
     Input('input-j', 'value')] +
    [Input('input-total-dias', 'value')] +
    [Input('input-venta', 'value'),
     Input('input-costos', 'value'),
     Input('input-remuneracion', 'value')],
     Input('nomina-obreros', 'value'),
     prevent_initial_call=False
)
def habilitar_simular(*args):
    i, j, total_dias, venta, costos, remuneracion, nomina = args[-7:]

    for arg in args[:-7]:  # Excluyendo los últimos 6 valores
        if arg is None or not isinstance(arg, int):
            return True, "Todos los campos, excepto los de ventas, costos, remuneración, i y j, deben contener valores numéricos."

    for arg in args[-7:]:  # Comprobando los últimos 6 valores
        if arg is None or not isinstance(arg, (int, float)):
            return True, "Los campos de ventas, costos, remuneración, i y j deben contener valores numéricos."

    if not isinstance(venta, (int, float)) or not isinstance(costos, (int, float)) or not isinstance(remuneracion,
                                                                                                     (int, float)):
        return True, "Los campos de ventas, costos y remuneración deben contener valores numéricos."

    if venta <= 0:
        return True, "El valor de ventas debe ser mayor que 0."
    if venta < costos:
        return True, "El valor de ventas debe ser mayor o igual que los costos."
    if (remuneracion * nomina) > (venta - costos):
        return True, "La remuneración diaria multiplicada por la nomina no debe ser mayor que la diferencia entre ventas y costos."

    suma_frecuencias = sum(args[:-7])  # Excluyendo el total de días a simular, i y j
    if suma_frecuencias != 100:
        return True, "La suma total de las frecuencias observadas debe ser igual a 100."

    if not isinstance(total_dias, int) or total_dias <= 0:
        return True, "La cantidad de días a simular debe ser un número entero mayor que 0."

    if not isinstance(i, int) or not isinstance(j, int) or i < 1 or j < 1 or j <= i:
        return True, "i y j deben ser números enteros positivos y j debe ser mayor que i."
    if isinstance(j, int) and j > total_dias:
        return True, "j deben ser menor o igual que la cantidad de dias a simular"
    if not isinstance(nomina, int) or nomina > 24 or nomina < 21:
        return True, "Valores validos de nomina: 21 - 22 - 23 - 24"
    return False, None  # No hay errores

@app.callback(
    [Output('pantalla-resultados', 'style'),
     Output('tabla-resultados', 'data'),
     Output('tabla-resultados', 'style_cell_conditional'),
     Output('tabla-resultados', 'style_table')],
    Input('button-simular', 'n_clicks'),
    [[State(f'input-{i}-operarios', 'value') for i in range(6)],
     State('input-total-dias', 'value'),
     State('input-venta', 'value'),
     State('input-costos', 'value'),
     State('input-remuneracion', 'value'),
     State('input-i', 'value'),
     State('input-j', 'value'),
     State('nomina-obreros', 'value')],
    prevent_initial_call=True
)
def mostrar_simulacion(_, valores_observados, total_dias, venta, costos, remuneracion, i, j, nomina):
    valores_tabla_ausentados = valores_observados[:6]  # Tomar los valores observados del primer al sexto
    resultados_simulacion, indice_productividad = simular_ausentismo(total_dias, valores_tabla_ausentados, venta, costos, remuneracion, i, j, nomina)

    return ({'display': 'block'}, resultados_simulacion,
             [
                {'if': {'column_id': 'reloj'},
                 'width': '10%'},
                {'if': {'column_id': 'rnd'},
                 'width': '8%'},
                 {'if': {'column_id': 'CantObrerosAusentes'},
                  'width': '11%'},
                 {'if': {'column_id': 'CantOperadores'},
                  'width': '12%'},
                 {'if': {'column_id': 'Beneficio'},
                 'width': '16%'},
                {'if': {'column_id': 'BeneficioAcum'},
                 'width': '25%'},
                 {'if': {'column_id': 'BeneficioPromedio'},
                 'width': '18%'},
             ],
            {'overflowX': 'auto', 'maxWidth': '95%', 'margin': 'auto'})

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
    
