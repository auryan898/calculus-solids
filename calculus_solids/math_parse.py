import numbers
import sympy
from sympy.sets.sets import Interval
# from mathml.lmathdom import MathDOM
# from mathml.utils import pyterm
import math

from pyparsing import alphas,CaselessLiteral,Literal,Word,ZeroOrMore,Forward,nums,oneOf,Regex,Group,Combine,Optional

def addAsterisks(s,l,t):
    if len(t)>0:
        return [ ['*']+list(token) for token in t ]
    else:
        return list(t)

def replaceExponentiate(s,l,t):
    if len(t)>0:
        return  [ '**' if token=='^' else token for token in t ]
    else:
        return t

def BNF():
    """
    expop   :: '^'
    multop  :: '*' | '/'
    addop   :: '+' | '-'
    integer :: ['+' | '-'] '0'..'9'+
    atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
    factor  :: atom [ expop factor ]*
    term    :: factor [ multop factor ]*
    expr    :: term [ addop term ]*
    """
    lpar = Literal('(')
    rpar = Literal(')')
    point = Literal('.')
    pi = CaselessLiteral("pi")
    e = CaselessLiteral("e")

    num = Combine( Word( nums ) + 
        Optional( point + Optional( Word( nums ) ) ) +
        Optional( e + Word( nums ) ) )
    # num = Regex(r"[+-]?\d+(:?\.\d*)?(:?[eE][+-]?\d+)?")
    # num = Word(nums)
    # ident = Word(alphas)
    ident = oneOf('factorial sin cos tan asin acos atan sinh cosh tanh asinh acosh atanh') | oneOf('exp exp ln log ceil floor exp int abs')
    
    plus = Literal('+')
    minus = Literal('-')
    mult = Literal('*')
    div = Literal('/')
    expop = Literal('^') | Literal('**')
    multop = mult | div
    addop =  plus | minus

    x = Literal('x') # We just care about x as the only variable

    exp=Literal('exp')

    expr = Forward()

    # literals = oneOf('tau')
    subatom = ( (exp+lpar+expr+rpar) | pi | e | x | num | (ident+lpar+expr+rpar) |  (lpar+expr+rpar) )
    atom = (0,None)*addop + ( subatom + ZeroOrMore(Group(subatom)).setParseAction(addAsterisks))

    # atom = Forward()
    # atom << ((0,None)*minus + (exp+lpar+expr+rpar | pi | e | x | num | ident+lpar+expr+rpar | ident |  Group(lpar+expr+rpar) ))
    # atom = ( (0,None)*minus + ( exp+lpar+expr+rpar | pi | e | x | num | ident+lpar+expr+rpar | ident ) | Group(lpar+expr+rpar))


    # atoms = atom + ZeroOrMore( atom )
    factor = Forward()
    factor << (atom + ZeroOrMore((expop+factor)) ) # atom [^factor]
    factor.setParseAction(replaceExponentiate)
    
    term = (factor + ZeroOrMore( multop+factor ))  # factor [/*factor] | factor [factor]
    # added = (term + ZeroOrMore( (addop+term) ))     # term [ +- term]
    # expr << (added + ZeroOrMore(added)) 

    expr << (term + ZeroOrMore( (addop+term) ))     # term [ +- term]
    return expr

def solve_functions(func1,func2,start=None,end=None,mirror_axis=False):
    parser = BNF()
    x = sympy.Symbol('x')
    try:
        expr1 = parser.parseString(func1)
    except Exception as e:
        return None, e
    try:
        expr2 = parser.parseString(func2)
    except Exception as e:
        return None, e
    expr1 = sympy.sympify(parser.transformString(func1))
    expr2 = sympy.sympify(parser.transformString(func2))
    if all( [ isinstance(item,numbers.Number) for item in [start,end]] ):
        start = min(float(start),float(end))
        end = max(float(start),float(end))
        set_dom = Interval(start,end)
        eq = sympy.Eq(expr1,expr2)
        solv = sympy.solveset(eq,x,domain=set_dom)
    else:
        eq = sympy.Eq(expr1,expr2)
        solv = sympy.solveset(eq,x,domain=sympy.S.Reals)
    try:
        if not isinstance(solv,sympy.FiniteSet):
            meta = None

        else:
            meta = list(solv)
            # meta =  meta if all([ isinstance(i,sympy.numbers.Number) for i in list(meta) ]) else [ i.__class__ for i in list(meta) ]
            # meta = 
            [ sympy.evalf() for i in meta]
    except:
        meta = None
    
    
    # print expr1,expr2
    expr1 = sympy.lambdify(x,expr1,'math')
    expr2 = sympy.lambdify(x,expr2,'math')
    result = lambda t : (max(expr1(t),expr2(t)), min(expr1(t),expr2(t))) # all bottom values
    
    def mirrored(x):
        y1 = expr1(x)
        y2 = expr2(x)
        a = max(y1,y2)
        b = min(y1,y2)
        r1 = max(abs(a),abs(b)) # outer value
        r2 = min(abs(a),abs(b)) # tentative inner value
        r2 = 0 if r2==a or r2==-b else r2
        return (r2,r1) # inner,outer

    if mirror_axis:
        # interv_pos = lambda t : (min(expr1(t),expr2(t)),max(expr1(t),expr2(t))) # returning a tuple representing the interval between top and bottom
        # interv_neg = lambda t : (min(-expr1(t),-expr2(t)),max(-expr1(t),-expr2(t)))
        result = mirrored



    return result,meta

def discrete_points_generator(func1,func2,start,end,interval=0.1,mirror_axis=False):
    start = float(min(start,end))
    end = float(max(start,end))
    interval = float(interval)
    x = sympy.Symbol('x')
    expr,solved_points = solve_functions(func1,func2,start,end,mirror_axis)

    r1 = []
    r2 = []
    xvalues = [ i*interval for i in range(int(start/interval),int(end/interval)+1)]
    if solved_points is not None:
        for pt in solved_points:
            if pt is not None:
                xvalues.append(pt.evalf())
    xvalues.sort()
    for xval in xvalues:
        y1,y2 = expr(xval)
        r1.append(min(y1,y2))
        r2.append(max(y1,y2))
    return r1,r2,xvalues


if __name__=='__main__':
    from calculus_solids import plotting_math
    y1,y2,x = discrete_points_generator('2.0*sin(x)-3.8','2.0*exp(x-8.4)-3.8',start=0,end=10,mirror_axis=False)
    points = list(zip(x,y1)) + (list(zip(x,y2)))
    print x
    points = [ (x,0,y) for x,y in points ]

    plotting_math.mesh_plotly(points,name="test_set")

    exit()
    expr = BNF()

    def test(c,s,v):
        results = expr.transformString( s )

        print results==v.strip(),c,' \t|',s,'<-', results,':', v
    def test(c,s,v):
        print c,'  \t',solve_functions(s,'2x',start=0,end=10), '->' ,expr.transformString(s)

    tests = [
    ("e","y"),
    ("x","y+x"),
    ("x2",""),
    ( "sin(pi(1/2))exp(-E)", 'sin(PI*(1/2))*exp(-E)'),
    ( "(9+3) / 11", '(9+3)/11'),
    ( "45exp(E)", '45*exp(E)'),
    ("-4/2x^2+9",'-4/2*x**2+9'),
    # ("45exp(6.7)32 + (x-8(exp(5^34x)-2))",'45*exp(6.7)*32+(x-8*(exp(5**34*x)-2))'),
    ("(3pi/9)^2+1",'(3*PI/9)**2+1'),
    # ("3xexp(x)+3exp(x)",'3*x*exp(x)+3*exp(x)'),
    ( "9 - -(12 - 6)", '9--(12-6)'),
    ("5",'5'),
    ( "9", '9'),
    ( "-9", '-9'),
    ( "--9", '--9x+3'),
    ( "-e", '-E'),
    ( "9 + 3 + 6", '9+3+6'),
    ( "9 + 3 / 11", '9+3/11'),
    ( "(9 + 3)", '(9+3)'),
    ( "9 - 12 - 6", '9-12-6'),
    ( "2*3.14159", '2*3.14159 '),
    ( "3.1415926535*3.1415926535 / 10", '3.1415926535*3.1415926535/10'),
    ( "pi * pi / 10", ' PI*PI/10'),
    ( "pi*pi/10", 'PI*PI/10 '),
    ( "pi^2", 'PI**2 '),
    ( "exp(pi^2)", 'exp(PI**2)'),
    ( "6.02E23 * 8.048", '6.02E23*8.048'),
    ( "e / 3", 'E/3'),
    ( "xsin(pi/2)", 'x*sin(PI/2)'),
    ( "exp(E)", 'exp(E)'),
    ( "exp(-E)", 'exp(-E)'),
    ( "E^pi", 'E**PI'),
    ( "2^3^2", '2**3**2'),
    ( "2^3+2", '2**3+2'),
    ( "2^3+5", '2**3+5'),
    ( "2^9", '2**9 '),
    # ( "sgn(-2)", '-1 '),
    # ( "sgn(0)", '0 '),
    # ( "foo(0.1)", '1 '),
    # ( "sgn(0.1)", '1' )
    ]
    counter = 0
    for t in tests:
        counter += 1
        test(counter,t[0],t[1])