import streamlit as st
import math

# Page Configuration
st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS with Beautiful Gradients and Animations
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        animation: gradientShift 15s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Calculator container */
    .calculator-box {
        background: linear-gradient(145deg, rgba(31, 41, 55, 0.95), rgba(17, 24, 39, 0.95));
        backdrop-filter: blur(10px);
        padding: 2.5rem;
        border-radius: 30px;
        box-shadow: 0 30px 80px rgba(0, 0, 0, 0.5),
                    0 0 50px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 2rem auto;
        max-width: 600px;
    }
    
    /* Header styling */
    .calc-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid rgba(147, 51, 234, 0.3);
    }
    
    .calc-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Display area */
    .display-container {
        background: linear-gradient(145deg, #0a0a0a, #1a1a2e);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: inset 0 4px 20px rgba(0, 0, 0, 0.5),
                    0 0 30px rgba(147, 51, 234, 0.2);
        border: 2px solid rgba(147, 51, 234, 0.3);
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .equation-display {
        font-size: 1.2rem;
        color: #a78bfa;
        font-family: 'Courier New', monospace;
        margin-bottom: 0.5rem;
        min-height: 30px;
        text-align: right;
        opacity: 0.8;
    }
    
    .main-display {
        font-size: 3rem;
        color: #ffffff;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        text-align: right;
        word-wrap: break-word;
        text-shadow: 0 0 20px rgba(167, 139, 250, 0.5);
    }
    
    /* Button styling */
    div.stButton > button {
        width: 100%;
        height: 65px;
        font-size: 1.3rem;
        font-weight: 700;
        border-radius: 15px;
        border: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        cursor: pointer;
    }
    
    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
    }
    
    div.stButton > button:active {
        transform: translateY(0px) scale(0.98);
    }
    
    /* Number buttons */
    div.stButton > button[kind="secondary"] {
        background: linear-gradient(145deg, #4b5563, #374151);
        color: white;
    }
    
    div.stButton > button[kind="secondary"]:hover {
        background: linear-gradient(145deg, #6b7280, #4b5563);
    }
    
    /* Operator buttons */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(145deg, #3b82f6, #2563eb);
        color: white;
    }
    
    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(145deg, #60a5fa, #3b82f6);
    }
    
    /* Function buttons - use data-testid to target specific buttons */
    .element-container:has(button:not([kind])) button {
        background: linear-gradient(145deg, #9333ea, #7c3aed) !important;
        color: white !important;
    }
    
    .element-container:has(button:not([kind])) button:hover {
        background: linear-gradient(145deg, #a855f7, #9333ea) !important;
    }
    
    /* Mode toggle button */
    .mode-button {
        background: linear-gradient(145deg, #ec4899, #db2777);
        color: white;
        padding: 0.7rem 1.5rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.1rem;
        border: none;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(236, 72, 153, 0.4);
    }
    
    .mode-button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(236, 72, 153, 0.6);
    }
    
    /* Remove default Streamlit spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 700px;
    }
    
    /* Column gap adjustment */
    div[data-testid="column"] {
        padding: 0.2rem;
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
    if st.session_state.display == '0' or st.session_state.display == 'Error':
        st.session_state.display = str(num)
    else:
        st.session_state.display += str(num)

def handle_operator(op):
    if st.session_state.display != 'Error':
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
        elif func == 'x!':
            result = math.factorial(int(num))
        else:
            return
        
        st.session_state.display = str(result)
    except Exception as e:
        st.session_state.display = 'Error'

def calculate():
    try:
        equation = st.session_state.equation + st.session_state.display
        equation = equation.replace('×', '*').replace('÷', '/').replace('^', '**').replace('mod', '%')
        result = eval(equation)
        st.session_state.display = str(result)
        st.session_state.equation = ''
    except:
        st.session_state.display = 'Error'

def clear():
    st.session_state.display = '0'
    st.session_state.equation = ''

def backspace():
    if st.session_state.display != 'Error':
        if len(st.session_state.display) > 1:
            st.session_state.display = st.session_state.display[:-1]
        else:
            st.session_state.display = '0'

# Main Calculator Container
st.markdown('<div class="calculator-box">', unsafe_allow_html=True)

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="calc-title">🔬 Scientific Calculator</div>', unsafe_allow_html=True)
with col2:
    if st.button("RAD" if st.session_state.is_radian else "DEG", key="mode_toggle"):
        st.session_state.is_radian = not st.session_state.is_radian
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Display
st.markdown(f"""
<div class="display-container">
    <div class="equation-display">{st.session_state.equation if st.session_state.equation else '&nbsp;'}</div>
    <div class="main-display">{st.session_state.display}</div>
</div>
""", unsafe_allow_html=True)

# Function buttons row 1
cols = st.columns(5)
functions_1 = [('sin', 'sin'), ('cos', 'cos'), ('tan', 'tan'), ('ln', 'ln'), ('log', 'log')]
for i, (label, func) in enumerate(functions_1):
    with cols[i]:
        if st.button(label, key=f'func1_{i}'):
            handle_function(func)
            st.rerun()

# Function buttons row 2
cols = st.columns(5)
functions_2 = [('√x', 'sqrt'), ('x²', 'x²'), ('x³', 'x³'), ('1/x', '1/x'), ('eˣ', 'e^x')]
for i, (label, func) in enumerate(functions_2):
    with cols[i]:
        if st.button(label, key=f'func2_{i}'):
            handle_function(func)
            st.rerun()

# Function buttons row 3
cols = st.columns(5)
special_buttons = [
    ('π', lambda: setattr(st.session_state, 'display', str(math.pi))),
    ('e', lambda: setattr(st.session_state, 'display', str(math.e))),
    ('|x|', lambda: handle_function('|x|')),
    ('x!', lambda: handle_function('x!')),
    ('AC', clear)
]
for i, (label, action) in enumerate(special_buttons):
    with cols[i]:
        if st.button(label, key=f'special_{i}', type='primary' if label == 'AC' else 'secondary'):
            action()
            st.rerun()

# Number pad row 1
cols = st.columns(5)
buttons_row1 = [('7', lambda: handle_number('7')), ('8', lambda: handle_number('8')), ('9', lambda: handle_number('9')), 
                ('÷', lambda: handle_operator('÷')), ('⌫', backspace)]
for i, (label, action) in enumerate(buttons_row1):
    with cols[i]:
        btn_type = 'primary' if label in ['÷', '⌫'] else 'secondary'
        if st.button(label, key=f'row1_{i}', type=btn_type):
            action()
            st.rerun()

# Number pad row 2
cols = st.columns(5)
buttons_row2 = [('4', lambda: handle_number('4')), ('5', lambda: handle_number('5')), ('6', lambda: handle_number('6')), 
                ('×', lambda: handle_operator('×')), ('^', lambda: handle_operator('^'))]
for i, (label, action) in enumerate(buttons_row2):
    with cols[i]:
        btn_type = 'primary' if label in ['×', '^'] else 'secondary'
        if st.button(label, key=f'row2_{i}', type=btn_type):
            action()
            st.rerun()

# Number pad row 3
cols = st.columns(5)
buttons_row3 = [('1', lambda: handle_number('1')), ('2', lambda: handle_number('2')), ('3', lambda: handle_number('3')), 
                ('−', lambda: handle_operator('-')), ('mod', lambda: handle_operator('mod'))]
for i, (label, action) in enumerate(buttons_row3):
    with cols[i]:
        btn_type = 'primary' if label in ['−', 'mod'] else 'secondary'
        if st.button(label, key=f'row3_{i}', type=btn_type):
            action()
            st.rerun()

# Number pad row 4
cols = st.columns(5)
buttons_row4 = [('0', lambda: handle_number('0')), ('.', lambda: handle_number('.')), 
                ('(', lambda: handle_number('(')), (')', lambda: handle_number(')')), 
                ('+', lambda: handle_operator('+'))]
for i, (label, action) in enumerate(buttons_row4):
    with cols[i]:
        btn_type = 'primary' if label == '+' else 'secondary'
        if st.button(label, key=f'row4_{i}', type=btn_type):
            action()
            st.rerun()

# Equals button (full width)
if st.button('=', key='equals', type='primary', use_container_width=True):
    calculate()
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; margin-top: 2rem; color: rgba(255, 255, 255, 0.6); font-size: 0.9rem;'>
    <p>💡 Toggle between RAD/DEG modes • Full scientific functionality</p>
</div>
""", unsafe_allow_html=True)
