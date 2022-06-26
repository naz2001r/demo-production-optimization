import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from ortools.linear_solver import pywraplp


if 'init' not in st.session_state: st.session_state['init']=False
if 'load_file' not in st.session_state: st.session_state['load_file']=False
if 'submited_file' not in st.session_state: st.session_state['submited_file']=False
if 'store' not in st.session_state: st.session_state['store']={}
if 'store_df' not in st.session_state: st.session_state['store_df']={}
if 'edit' not in st.session_state: st.session_state['edit']=False
if 'edit_label' not in st.session_state: st.session_state['edit_label']='lock'

if st.session_state.init == False:
    st.session_state.store_df = {}
    st.session_state.init = True


@st.cache(allow_output_mutation=True)
def fetch_store_data():
    return pd.DataFrame(st.session_state.store_df)


def saveDefault():
    st.session_state.submited_file = True
    st.session_state.store_df = st.session_state.store
    return


def lock_unlock():
    if st.session_state.edit_label == 'lock':
        st.session_state.edit_label = 'unlock'
    else:
        st.session_state.edit_label = 'lock'

    return saveDefault()


def sidebar():

    data = st.sidebar.file_uploader('Upload production optimization data',type=["xlsx","xls"])
    st.sidebar.button('submit load data', key='submmit', on_click=saveDefault)
    st.sidebar.text('Edit production optimization data')
    st.sidebar.button(st.session_state.edit_label, key='lock/unlock', on_click=lock_unlock)

    if st.session_state.edit_label == 'lock': 
        st.session_state.edit = False
    
    elif st.session_state.edit_label == 'unlock': 
        st.session_state.edit = True

    return data


def init_model(df: pd.DataFrame):
    solver = pywraplp.Solver.CreateSolver('SCIP')

    df =df.set_index('resources')

    b_values = df.Count.values[:-1]
    df = df.drop(columns=['Count'])

    variables = [ solver.IntVar(0, solver.infinity(), item) 
                for item in df.columns]

    if 'Profit'in df.index:
        objective_type = 'Profit'
    elif 'Cost'in df.index:
        objective_type = 'Cost'
    profit_cost = df.loc[objective_type].values
    df = df.drop(objective_type,axis=0)

    if objective_type == 'Profit':
        solver.Maximize(sum(profit_cost*variables))

        # added constraines
        for i in range(len(df)):
            solver.Add(sum(df.values[i]*variables)<=b_values[i])

    else:
        solver.Minimize(sum(profit_cost*variables))

        # added constraines
        for i in range(len(df)):
            solver.Add(sum(df.values[i]*variables)>=b_values[i])

    return (solver, 
            df, 
            variables,
            objective_type)

def objective_type_string(objective_type):
    if objective_type == 'Profit':
        return 'Maximum profit'
    return 'Minimum cost'


def app():
    st.subheader('Production Optimization')
    data = sidebar()
    if not st.session_state.load_file and data != None:
        st.session_state.load_file = True
        try:
            df = pd.read_excel(data)
        except:
            raise TypeError('Unexpected file type.')
    else:
        df = fetch_store_data()

    # viz input tables
    if st.session_state.submited_file:
        ag = AgGrid(df, editable=st.session_state.edit, height=200, theme = 'streamlit')
        df=ag['data']

    st.session_state.store=df.to_dict()

    # optimization step
    if st.button('Optimize', key='optimize'):
        solver, df, variables, objective_type = init_model(df)

        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            st.header('Solution:')
            st.subheader(f'{objective_type_string(objective_type)} = {round(solver.Objective().Value(),2)}')
            for i,item in enumerate(df.columns):
                st.markdown(f'**{item} =** {variables[i].solution_value()}')
        else:
            st.markdown('**The problem does not have an optimal solution.**')


if __name__ == '__main__':
    app()