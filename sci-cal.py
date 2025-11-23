import streamlit as st
import math
import numpy as np

# Page config
st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="🔬",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .calculator-container {
        background: linear-gradient(145deg, #1f2937, #111827);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    .display {
        background: linear-gradient(145deg, #000000, #1a1a1a);
        padding: 1.5rem;
        border-radius: 15px;
        font-size: 2.5rem;
        text-align: right;
        color: white;
        font-family: monospace;
        margin-bottom: 1.5rem;
        min-height: 80px;
    }
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'display' not in st.session_state:
    st.session_state.display = '0'
if 'equation' not in st.session_state:
    st.session_state.equation = ''
if 'is_radian' not in st.session_state:
    st.session_state.is_radian = True

def handle_number(num):
    if st.session_state.display == '0':
        st.session_state.display = str(num)
    else:
        st.session_state.display += str(num)

def handle_operator(op):
    st.session_state.equation = st.session_state.display + ' ' + op + ' '
    st.session_state.display = '0'

def handle_function(func):
    try:
        num = float(st.session_state.display)
        
        if func == 'sin':
            result = math.sin(num) if st.session_state.is_radian else math.sin(math.radians(num))
        elif func == 'cos':
            result = math.cos(num) if st.session_state.is_radian else math.cos(math.radians(num))
        elif func == 'tan':
            result = math.tan(num) if st.session_state.is_radian else math.tan(math.radians(num))
        elif func == 'ln':
            result = math.log(num)
        elif func == 'log':
            result = math.log10(num)
        elif func == 'sqrt':
            result = math.sqrt(num)
        elif func == 'x²':
            result = num ** 2
        elif func == 'x³':
            result = num ** 3
        elif func == '1/x':
            result = 1 / num
        elif func == 'e^x':
            result = math.exp(num)
        elif func == '|x|':
            result = abs(num)
        
        st.session_state.display = str(result)
    except Exception as e:
        st.session_state.display = 'Error'

def calculate():
    try:
        equation = st.session_state.equation + st.session_state.display
        equation = equation.replace('×', '*').replace('÷', '/').replace('^', '**')
        result = eval(equation)
        st.session_state.display = str(result)
        st.session_state.equation = ''
    except:
        st.session_state.display = 'Error'

def clear():
    st.session_state.display = '0'
    st.session_state.equation = ''

def backspace():
    if len(st.session_state.display) > 1:
        st.session_state.display = st.session_state.display[:-1]
    else:
        st.session_state.display = '0'

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🔬 Scientific Calculator")
with col2:
    mode = st.button("RAD" if st.session_state.is_radian else "DEG")
    if mode:
        st.session_state.is_radian = not st.session_state.is_radian
        st.rerun()

# Display
st.markdown(f"""
<div class="display">
    <div style="font-size: 1rem; color: #a78bfa; margin-bottom: 0.5rem;">{st.session_state.equation}</div>
    <div>{st.session_state.display}</div>
</div>
""", unsafe_allow_html=True)

# Function buttons row 1
cols = st.columns(5)
functions_1 = ['sin', 'cos', 'tan', 'ln', 'log']
for i, func in enumerate(functions_1):
    with cols[i]:
        if st.button(func, key=f'func1_{i}'):
            handle_function(func)
            st.rerun()

# Function buttons row 2
cols = st.columns(5)
functions_2 = ['√', 'x²', 'x³', '1/x', 'e^x']
func_map_2 = ['sqrt', 'x²', 'x³', '1/x', 'e^x']
for i, func in enumerate(functions_2):
    with cols[i]:
        if st.button(func, key=f'func2_{i}'):
            handle_function(func_map_2[i])
            st.rerun()

# Function buttons row 3
cols = st.columns(5)
with cols[0]:
    if st.button('π'):
        st.session_state.display = str(math.pi)
        st.rerun()
with cols[1]:
    if st.button('e'):
        st.session_state.display = str(math.e)
        st.rerun()
with cols[2]:
    if st.button('|x|'):
        handle_function('|x|')
        st.rerun()
with cols[3]:
    if st.button('( )'):
        pass
with cols[4]:
    if st.button('C'):
        clear()
        st.rerun()

# Number pad
for row in [[7,8,9,'÷','⌫'], [4,5,6,'×','%'], [1,2,3,'-','^']]:
    cols = st.columns(5)
    for i, btn in enumerate(row):
        with cols[i]:
            if isinstance(btn, int):
                if st.button(str(btn), key=f'num_{btn}'):
                    handle_number(btn)
                    st.rerun()
            elif btn == '⌫':
                if st.button(btn):
                    backspace()
                    st.rerun()
            else:
                if st.button(btn, key=f'op_{btn}'):
                    handle_operator(btn)
                    st.rerun()

# Last row
cols = st.columns(5)
with cols[0]:
    if st.button('0', key='num_0'):
        handle_number(0)
        st.rerun()
with cols[1]:
    if st.button('.'):
        if '.' not in st.session_state.display:
            st.session_state.display += '.'
        st.rerun()
with cols[2]:
    if st.button('+'):
        handle_operator('+')
        st.rerun()
with cols[3]:
    if st.button('='):
        calculate()
        st.rerun()
