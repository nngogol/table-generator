#!/usr/bin/python3

'''
    Made at 2020-02-14 12:32:48
    by nngogol
'''

'''
python script ->
    ✔ table html
    ✔ qlabel
    ✔ raw tabular-text-table
    ✔ QTableWidget
'''

# =========================
# =========================
# =========================
import PySimpleGUI as sg
from textwrap import *
indent1 = lambda x: indent(x, '  ')
indent2 = lambda x: indent(x, '    ')


def render_ui_xml(lines:str, delim='~', use_T=False):
    '''
    Рендер "vbox" з "qlabel" в них.

    Формат переменной lines
    lines = 
    q1 ~ w1 ~ e1
    q2 ~ w2 ~ e2
    q3 ~ w3 ~ e3
    '''

    pure_lines = lines.strip().split('\n')
    used_items = [ [i.strip() for i in line.split(delim) if i.strip()] for line in pure_lines]
    if use_T: used_items = list(map(list, zip(*used_items)))

    vboxs = []
    part_template = '''<item> <widget class="QLabel" name="label_{1}"> <property name="text"> <string>{0}</string> </property> </widget> </item>'''
    for index1, line in enumerate(used_items):
        items_xml = ''.join([part_template.format(i, f'{index2}_{index1}') for index2, i in enumerate(line)])

        vbox = '''<widget class="QWidget" name="verticalLayoutWidget_{0}">
            <property name="geometry">
                <rect>
                    <x>{2}</x>
                    <y>50</y>
                    <width>160</width>
                    <height>80</height>
                </rect>
            </property>
            <layout class="QVBoxLayout" name="verticalLayout_{0}">
                {1}
            </layout>
        </widget>'''.format(index1, items_xml, index1*80)
        vboxs.append(vbox)

    return '''<?xml version="1.0" encoding="UTF-8"?>
    <ui version="4.0">
        <class>MainWindow</class>
        <widget class="QMainWindow" name="MainWindow">
            <property name="geometry">
                <rect>
                    <x>0</x>
                    <y>0</y>
                    <width>561</width>
                    <height>282</height>
                </rect>
            </property>
            <property name="windowTitle">
                <string>MainWindow</string>
            </property>
            <widget class="QWidget" name="centralwidget">
                {items}
            </widget>
        </widget>
        <resources />
        <connections />
    </ui>'''.format(items=''.join(vboxs))

def render_q_grid_layout(rows:list=[], cols:list=[], lines:str='', delim='~', use_T=False):
    '''
    Рендер в QTableWidget
    rows = ['guy1', 'guy2', 'guy3']
    cols = ['name', 'city', 'ajob']
    lines = \'\'\'bla~bla~bla
    bla~bla~bla
    bla~bla~bla\'\'\'
    '''

    pure_lines = lines.strip().split('\n')
    used_items = [ [i.strip() for i in line.split(delim) if i.strip()] for line in pure_lines]
    if use_T: used_items = list(map(list, zip(*used_items)))

    rows_cols = [f'<row>    <property name="text"> <string>{row_name}</string> </property> </row>' for row_name in rows] +\
                [f'<column> <property name="text"> <string>{col_name}</string> </property> </column>' for col_name in cols]
    items = []
    for row, i in enumerate(used_items):
        items.extend([f'<item row="{row}" column="{column}"> <property name="text"> <string>{val}</string> </property> </item>' for column, val in enumerate(i)])

    table = '''<widget class="QTableWidget" name="tableWidget"> <property name="geometry">
         <rect>
            <x>80</x> <y>40</y> <width>321</width> <height>151</height>
         </rect> </property>
         {rows_cols} {items} </widget>'''.format(rows_cols=''.join(rows_cols), items=''.join(items))

    return '''<?xml version="1.0" encoding="UTF-8"?> <ui version="4.0"> <class>MainWindow</class> <widget class="QMainWindow" name="MainWindow"> <property name="geometry">
       <rect>
        <x>0</x> <y>0</y>
        <width>561</width> <height>282</height>
       </rect> </property> <property name="windowTitle"> <string>MainWindow</string> </property>
      <widget class="QWidget" name="centralwidget">
        {items}
      </widget> </widget> <resources/> <connections/> </ui>
    '''.format(items=table)

def render_raw_tabular_text_table(col_names:list=[], lines:str='', delim='~', use_T=False):
    '''
    рендер в обычный текст 
    col_names = ['name',  'city', 'job' ...]
    '''

    # items
    pure_lines = lines.strip().split('\n')
    used_items = [ [i.strip() for i in line.split(delim) if i.strip()] for line in pure_lines]
    if use_T: used_items = list(map(list, zip(*used_items)))

    width = max([len(i) for i in pure_lines])
    width = (width/(len(col_names))) + 10

    temp = ('{:<{width}} '*len(col_names)).strip()
    # temp = ' '.join([ '{' + str(i) + ':<{width}} ' for i in range(len(col_names))])

    res = temp.format(*col_names, width=width).strip() + '\n'
    res += '----------------------------\n'
    for name, city, job in used_items: 
        res += '{0:<{width}} {1:<{width}} {2:<{width}}'.format(name, city, job, width=width).strip() + '\n'
    return res

def render_table_html(col_names:list=[], lines:str='', delim='~', use_T=False):
    '''
    рендер в обычный текст 
    col_names = ['name',  'city', 'job' ...]

    exmaple
        a = 'name city job'.split()
        b = 'Alice~Kiev~Singer\nBob~New-York~Programmer\nFrank~London~Driver'
        res = render_table_html(a, b, use_T=True)
        print(f'res = {res}')

    '''

    # items
    pure_lines = lines.strip().split('\n')
    used_items = [ [i.strip() for i in line.split(delim) if i.strip()] for line in pure_lines]
    if use_T: used_items = list(map(list, zip(*used_items)))

    # <table>
    #     <tr><th>name</th><th>city</th><th>job</th></tr>
    #     <tr>0</tr><tr>0</tr><tr>0</tr>
    # </table>

    trs = [indent2('\n<tr>' + ''.join([indent2(f'\n<td>{i}</td>') for i in row]) + '\n</tr>') for row in used_items]

    ths = '\n'.join([indent2(f'<th>{i}</th>') for i in col_names])
    ths = indent2(f'<tr>\n{ths}\n</tr>')

    return '''<table>\n{th}{rows}\n</table>'''.format(
                th=ths,
                rows=''.join(trs))

window = sg.Window('make table', [
    [
        sg.Frame('Много qlabel (друг за другом)', [
            [sg.Button('render', key='render'), sg.Button('render transpose', key='render T')]
            ,[sg.Text('* =none=')]
        ])
        ,sg.Frame('HTML table', [
            [sg.Button('render', key='render3'), sg.Button('render transpose', key='render3 T')]
            ,[sg.Text('* cols')]
        ])
        ,sg.Frame('Raw Text', [
            [sg.Button('render', key='render4'), sg.Button('render transpose', key='render4 T')]
            ,[sg.Text('* cols')]
        ])
        ,sg.Frame('QTableWidget', [
            [sg.Button('render', key='render2'), sg.Button('render transpose', key='render2 T')]
            ,[sg.Text('* rows cols')]
        ])
    ]
    ,[sg.Text('cols:', size=(10, 1)), sg.Input('name city job', key='cols')]
    ,[sg.Text('rows:', size=(10, 1)), sg.Input('guy1 guy2 guy3', key='rows')]
    ,[sg.Text('delim', size=(10, 1)), sg.Input('~', key='delim', size=(1, 5))]
    
    
    ,[sg.Column([
        [sg.Text('vals:'), sg.ML('Alice~Kiev~Singer\nBob~New-York~Programmer\nFrank~London~Driver', key='vals', size=(40, 10))
        ,sg.Text('<==>')
        ,sg.ML('', key='out', size=(40, 10)), sg.Text(':out')]
        ])]

    ,[sg.T(' '*100), sg.Button('Copy to buffer', key='copy buffer')]
])
out = window['out']

while True:
    event, values = window()
    if event in ('Exit', None): break

    print(event)

    #======
    # click
    #======
    if event == 'copy buffer':
        import pyperclip
        pyperclip.copy(values['out'])

    #=============
    # render click
    #=============

    vals, delim = values['vals'], values['delim']
    use_T = 'T' in event

    # # 1
    if event == 'render':
        out(render_ui_xml(vals, delim, use_T=use_T))

    # # 2
    rows = values['rows'].strip().split(' ')
    cols = values['cols'].strip().split(' ')
    if event == 'render2':
        out(render_q_grid_layout(rows, cols, vals, delim, use_T=use_T))

    # # 3
    cols = values['cols'].strip().split(' ')
    if event == 'render3':
        out(render_table_html(cols, vals, delim, use_T=use_T))

    # # 4
    cols = values['cols'].strip().split(' ')
    if event == 'render4':
        out(render_raw_tabular_text_table(cols, vals, delim, use_T=use_T))


window.close()










