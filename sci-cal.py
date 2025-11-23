import streamlit as st
import math

# Page Configuration
st.set_page_config(
    page_title="Scientific Calculator Pro",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Professional CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit elements */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        min-height: 100vh;
    }
    
    /* Calculator container */
    .calculator-container {
        background: linear-gradient(145deg, #1e1e2e, #16161e);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.5),
            0 0 1px rgba(255, 255, 255, 0.1) inset,
            0 50px 100px rgba(79, 70, 229, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.05);
        max-width: 480px;
        margin: 3rem auto;
    }
    
    /* Header */
    .calculator-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .calculator-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.02em;
    }
    
    .mode-indicator {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.875rem;
        letter-spacing: 0.05em;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Display */
    .display-area {
        background: #000000;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 
            inset 0 2px 8px rgba(0, 0, 0, 0.6),
            0 4px 16px rgba(102, 126, 234, 0.1);
    }
    
    .equation-line {
        color: #8b5cf6;
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        min-height: 24px;
        text-align: right;
        opacity: 0.7;
        font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
    }
    
    .display-value {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: right;
        letter-spacing: -0.02em;
        font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
        word-break: break-all;
    }
    
    /* Button grid improvements */
    .button-grid {
        display: grid;
        gap: 0.5rem;
    }
    
    /* All buttons base style */
    div.stButton > button {
        width: 100%;
        height: 60px;
        font-size: 1.125rem;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        letter-spacing: -0.01em;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    
    div.stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Number buttons - Dark gray */
    div.stButton > button[kind="secondary"] {
        background: linear-gradient(145deg, #2d2d3a, #25252f);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    div.stButton > button[kind="secondary"]:hover {
        background: linear-gradient(145deg, #35354a, #2d2d3a);
        border-color: rgba(255, 255, 255, 0.1);
    }
    
    /* Operator buttons - Blue gradient */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #7c8ff0 0%, #8b5baf 100%);
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Function buttons - Purple tint */
    .element-container:has(button:not([kind])) button {
        background: linear-gradient(145deg, #2d2d3a, #25252f) !important;
        color: #a78bfa !important;
        border: 1px solid rgba(167, 139, 250, 0.1) !important;
    }
    
    .element-container:has(button:not([kind])) button:hover {
        background: linear-gradient(145deg, #35354a, #2d2d3a) !important;
        border-color: rgba(167, 139, 250, 0.3) !important;
        box-shadow: 0 4px 16px rgba(167, 139, 250, 0.2) !important;
    }
    
    /* Equals button - Green gradient */
    button[key="equals"] {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        height: 60px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    button[key="equals"]:hover {
        background: linear-gradient(135deg, #34d399 0%, #10b981 100%) !important;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4) !important;
    }
    
    /* Clear button - Red accent */
    button[key="special_4"] {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    button[key="special_4"]:hover {
        background: linear-gradient(135deg, #f87171 0%, #ef4444 100%) !important;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.4) !important;
    }
    
    /* Remove Streamlit padding */
    .block-container {
        padding: 2rem 1rem;
        max-width: 520px;
    }
    
    /* Column spacing */
    div[data-testid="column"] {
        padding: 0.25rem;
    }
    
    /* Footer styling */
    .calculator-footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.4);
        font-size: 0.875rem;
        margin-top: 1.5rem;
        font-weight: 500;
    }
    
    .feature-tag {
        display: inline-block;
        background: rgba(102, 126, 234, 0.1);
        color: #a78bfa;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.75rem;
        margin: 0.25rem;
        border: 1px solid rgba(167, 139, 250, 0.2);
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
        
        functions = {
            'sin': lambda x: math.sin(x) if st.session_state.is_radian else math.sin(math.radians(x)),
            'cos': lambda x: math.cos(x) if st.session_state.is_radian else math.cos(math.radians(x)),
            'tan': lambda x: math.tan(x) if st.session_state.is_radian else math.tan(math.radians(x)),
            'ln': math.log,
            'log': math.log10,
            'sqrt': math.sqrt,
            'x²': lambda x: x ** 2,
            'x³': lambda x: x ** 3,
            '1/x': lambda x: 1 / x,
            'e^x': math.exp,
            '|x|': abs,
            'x!': lambda x: math.factorial(int(x))
        }
        
        if func in functions:
            result = functions[func](num)
            st.session_state.display = str(result)
    except Exception:
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

# Main Calculator
st.markdown('<div class="calculator-container">', unsafe_allow_html=True)

# Header
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<div class="calculator-title">🧮 Scientific Calculator</div>', unsafe_allow_html=True)
with col2:
    if st.button("RAD" if st.session_state.is_radian else "DEG", key="mode_btn"):
        st.session_state.is_radian = not st.session_state.is_radian
        st.rerun()

# Display
st.markdown(f"""
<div class="display-area">
    <div class="equation-line">{st.session_state.equation if st.session_state.equation else '&nbsp;'}</div>
    <div class="display-value">{st.session_state.display}</div>
</div>
""", unsafe_allow_html=True)

# Row 1: Trigonometric functions
cols = st.columns(5)
for i, (label, func) in enumerate([('sin', 'sin'), ('cos', 'cos'), ('tan', 'tan'), ('ln', 'ln'), ('log', 'log')]):
    with cols[i]:
        if st.button(label, key=f'trig_{i}'):
            handle_function(func)
            st.rerun()

# Row 2: Power functions
cols = st.columns(5)
for i, (label, func) in enumerate([('√', 'sqrt'), ('x²', 'x²'), ('x³', 'x³'), ('1/x', '1/x'), ('eˣ', 'e^x')]):
    with cols[i]:
        if st.button(label, key=f'pow_{i}'):
            handle_function(func)
            st.rerun()

# Row 3: Special functions
cols = st.columns(5)
special = [
    ('π', lambda: setattr(st.session_state, 'display', str(math.pi))),
    ('e', lambda: setattr(st.session_state, 'display', str(math.e))),
    ('|x|', lambda: handle_function('|x|')),
    ('x!', lambda: handle_function('x!')),
    ('AC', clear)
]
for i, (label, action) in enumerate(special):
    with cols[i]:
        if st.button(label, key=f'special_{i}'):
            action()
            st.rerun()

# Row 4: Numbers 7-9
cols = st.columns(5)
for i, (label, action, btn_type) in enumerate([
    ('7', lambda: handle_number('7'), 'secondary'),
    ('8', lambda: handle_number('8'), 'secondary'),
    ('9', lambda: handle_number('9'), 'secondary'),
    ('÷', lambda: handle_operator('÷'), 'primary'),
    ('⌫', backspace, 'primary')
]):
    with cols[i]:
        if st.button(label, key=f'r4_{i}', type=btn_type):
            action()
            st.rerun()

# Row 5: Numbers 4-6
cols = st.columns(5)
for i, (label, action, btn_type) in enumerate([
    ('4', lambda: handle_number('4'), 'secondary'),
    ('5', lambda: handle_number('5'), 'secondary'),
    ('6', lambda: handle_number('6'), 'secondary'),
    ('×', lambda: handle_operator('×'), 'primary'),
    ('^', lambda: handle_operator('^'), 'primary')
]):
    with cols[i]:
        if st.button(label, key=f'r5_{i}', type=btn_type):
            action()
            st.rerun()

# Row 6: Numbers 1-3
cols = st.columns(5)
for i, (label, action, btn_type) in enumerate([
    ('1', lambda: handle_number('1'), 'secondary'),
    ('2', lambda: handle_number('2'), 'secondary'),
    ('3', lambda: handle_number('3'), 'secondary'),
    ('−', lambda: handle_operator('-'), 'primary'),
    ('mod', lambda: handle_operator('mod'), 'primary')
]):
    with cols[i]:
        if st.button(label, key=f'r6_{i}', type=btn_type):
            action()
            st.rerun()

# Row 7: Zero and operators
cols = st.columns(5)
for i, (label, action, btn_type) in enumerate([
    ('0', lambda: handle_number('0'), 'secondary'),
    ('.', lambda: handle_number('.'), 'secondary'),
    ('(', lambda: handle_number('('), 'secondary'),
    (')', lambda: handle_number(')'), 'secondary'),
    ('+', lambda: handle_operator('+'), 'primary')
]):
    with cols[i]:
        if st.button(label, key=f'r7_{i}', type=btn_type):
            action()
            st.rerun()

# Equals button
if st.button('=', key='equals', use_container_width=True):
    calculate()
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="calculator-footer">
    <div style="margin-bottom: 0.75rem;">
        <span class="feature-tag">Trigonometry</span>
        <span class="feature-tag">Logarithms</span>
        <span class="feature-tag">Powers</span>
        <span class="feature-tag">Factorial</span>
    </div>
    <div style="opacity: 0.6;">Professional Scientific Calculator • Toggle RAD/DEG Mode</div>
</div>
""", unsafe_allow_html=True)
