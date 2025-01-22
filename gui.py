import PySimpleGUI as sg
import numpy as np

from fuzzy_topsis.main import fuzzy_topsis_do_gui
from RSM.RSM import RSM
from spcs.spcs import gui_spcs
from UTA.main import uta
from input_validation import validate
from ranking_comparision.compare import Spearman_s_Footrule
from loader import load_data

algos = {
    'FUZZY_TOPSIS': fuzzy_topsis_do_gui,
    'RSM': RSM,
    'SAFETY_PRINCIPAL': gui_spcs,
    'UTA': uta
}

list_k = [
    "Hotel_ID", 
    "Location", 
    "Price", 
    "Overall_Rating", 
    "Value_Rating", 
    "Rooms_Rating", 
    "Location_Rating", 
    "Cleanliness_Rating", 
    "Front_Desk_Rating", 
    "Service_Rating", 
    "Business_Service_Rating", 
    "Distance_From_Kraków"
]

result_headings = [
    "Hotel_ID",
    "Location",
    "Score"
]

weights_layout = [
    [sg.Text('Podaj wagi (1 - 9)', justification='center')],
    [sg.InputText(key=f'-WEIGHT{str(i)}-', size=(20, 1), default_text='  1') for i in range(len(list_k[2:]))],
    [sg.Text('')]
]

criteria_layout = [
    [sg.Text('Podaj kryteria (min/max)', justification='center')],
    [sg.Text(i, size=(20, 1)) for i in list_k[2:]],
    [sg.Combo(values=['min', 'max'], default_value='min', key=f'-CRIT{str(i)}-', size=(20, 1)) for i in range(len(list_k[2:]))],
    [sg.Text('')]
]

choose_algo_layout = [
    [sg.Text('Wybierz algorytm'), sg.Combo(key='-ALGO-', values=list(algos.keys()), default_value=list(algos.keys())[0], size=(50, 5))],
    [sg.Text('')]
]

create_rank_layout = [
    [sg.Button('Stwórz ranking',key='-BUTTON_RANKING-')]
]

alternatives_layout = [
    [sg.Text('Alternatywy z kryteriami', justification='center')],
    [sg.Table([], headings=list_k,key='-TABLE_KRYT-', num_rows=6, max_col_width = 5, auto_size_columns=True, vertical_scroll_only=False, justification='center', expand_x=True, expand_y=True)]
]

disp_ranking_layout = [
    [sg.Text('Ranking',justification='center')],
    [sg.Table([], result_headings, key='-TABLE_RANK-', num_rows=6, auto_size_columns=True)]
]

compare_layout = [
    [sg.Text('Wybierz algorytmy do porównania')],
    [sg.Combo(key='-ALGO1-', values=list(algos.keys()), default_value=list(algos.keys())[0], size=(20, 1)), sg.Combo(key='-ALGO2-', values=list(algos.keys()), default_value=list(algos.keys())[0], size=(20, 1))],
    [sg.Text('')],
    [sg.Button('Porównaj rankingi',key='-COMPARE_RANKING-')]
]

disp_comparision_layout = [
    [sg.Text('', justification='center', key='-OUT-')]
]

layout = [
    [criteria_layout],
    [weights_layout],
    [choose_algo_layout],
    [create_rank_layout],
    [sg.Col(alternatives_layout,vertical_alignment='top')],
    [disp_ranking_layout],
    [compare_layout],
    [disp_comparision_layout]
]

window = sg.Window(
    'OW_projekt',
    layout,
    finalize=True,
    resizable=True,
    size=(1000,800),
    element_justification='center'
)


def read_additional_params() -> dict:
    
    weights = np.array([str.lstrip(values[f'-WEIGHT{i}-']) for i in range(len(list_k[2:]))])
    criteria = np.array([values[f'-CRIT{i}-'] for i in range(len(list_k[2:]))])

    regex = "^[+-]?([1-9])?$"
    
    if validate(weights, regex):
        
        weights = [int(i) for i in weights]
        additional_params = {
                    'FUZZY_TOPSIS': (weights, criteria), #checked
                    'RSM': criteria, #checked
                    'SAFETY_PRINCIPAL': None, #checked
                    'UTA': criteria #checked
                }
        
        return additional_params, weights, criteria
    
    else:
        sg.popup('Wprowadzone dane są niepoprawne\nSpróbuj ponownie')
        return None, None, None


while True:
    
    event, values = window.read(timeout=200)
    
    if event == sg.WIN_CLOSED:
        break
    
    # Obliczenie rankingu pojedyńczą metodą
    if event == '-BUTTON_RANKING-':
        
        additional_params, weights, criteria = read_additional_params()
        
        if additional_params is not None:
            # Load database
            db = load_data("./datasets/reviews.dat")
            window['-TABLE_KRYT-'].update(values=list(map(tuple, db.values)))
            
            # Call algorithm if not called before
            if f"{values['-ALGO-']}_score" not in db.columns:
                db = algos[values['-ALGO-']](db, additional_params[values['-ALGO-']])

            window['-TABLE_RANK-'].update(values=list(map(tuple, db.sort_values(by=[f"{values['-ALGO-']}_score"], ascending=False)[result_headings[:-1] + [f"{values['-ALGO-']}_score"]].values)))
            
    # Porównanie rankingów
    if event == '-COMPARE_RANKING-':
        
        additional_params, weights, criteria = read_additional_params()
          
        if additional_params is not None:  
            db = load_data("./datasets/reviews.dat")
            window['-TABLE_KRYT-'].update(values=list(map(tuple, db.values)))
        
            if f"{values['-ALGO1-']}_score" not in db.columns:
                db = algos[values['-ALGO1-']](db, additional_params[values['-ALGO1-']])

            if f"{values['-ALGO2-']}_score" not in db.columns:
                db = algos[values['-ALGO2-']](db, additional_params[values['-ALGO2-']])
                
            rank_1 = [idx for idx in db.sort_values(by=[f"{values['-ALGO1-']}_score"], ascending=False).index]
            rank_2 = [idx for idx in db.sort_values(by=[f"{values['-ALGO2-']}_score"], ascending=False).index]
            compare_result = Spearman_s_Footrule(rank_1, rank_2)
            window['-OUT-'].update(value=str(compare_result))
        
window.close()