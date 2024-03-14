import json as j
import BasicFuzzyFunctions as bf
import numpy as np


def read_fis(jf):
    return j.load(open(jf))

def var_prompt(d,x):
    return f'{x} ({d[x]["LeftB"]} - {d[x]["RightB"]}) = '

def read_inputs(fis):
    for x in fis['Inputs']:
        fis['Inputs'][x]['Value']=float(input(var_prompt(fis['Inputs'],x)))



def calc_mf(mf, x):
    if mf['MFType']=='Z':
        a=mf['Parameters']['a']
        b=mf['Parameters']['b']
        return bf.Z(x,a,b)
    elif mf['MFType']=='Trap':
        a=mf['Parameters']['a']
        b=mf['Parameters']['b']
        c=mf['Parameters']['c']
        d=mf['Parameters']['d']
        return bf.Trap(x,a,b,c,d)
    elif mf['MFType']=='S':
        a=mf['Params']['a']
        b=mf['Params']['b']
        return bf.S(x,a,b)
    elif mf['MFType']=='SmZ':
        a=mf['Parameters']['a']
        b=mf['Parameters']['b']
        return bf.SmZ(x,a,b)
    elif mf['MFType']=='SmTrap':
        a=mf['Parameters']['a']
        b=mf['Parameters']['b']
        c=mf['Parameters']['c']
        d=mf['Parameters']['d']
        return bf.SmTrap(x,a,b,c,d)
    elif mf['MFType']=='SmS':
        a=mf['Parameters']['a']
        b=mf['Parameters']['b']
        return bf.SmS(x,a,b)

def calc_lit(fis,VN,LTN,N):
    v=fis['Inputs'][VN]['LTerms'][LTN]['MFValue']
    return 1-v if N else v

def calc_con(fis, C):
    return min([calc_lit(fis,l['VarName'],l['LTName'],l['Neg']) for l in C])

def calc_dis(fis, D):
    return max([calc_con(fis,C) for C in D])

def calc_defuzz(X, Y, meth):
    if meth=='Centroid':
        return bf.Centroid(X, Y)
    elif meth=='FirstMax':
        return bf.FirstMax(X, Y)
    elif meth=='LastMax':
        return bf.LastMax(X, Y)
    elif meth=='AvgMax':
        return bf.AvgMax(X, Y)



def fuzzyfication(fis):
    for X in fis['Inputs']:
        x=fis['Inputs'][X]
        for T in x['LTerms']:
            t=x['LTerms'][T]
            t['MFValue']=calc_mf(t['MFunction'],x['Value'])

            
def fuzzyinference(fis):
    for Y in fis['Outputs']:
        y=fis['Outputs'][Y]
        for T in y['LTerms']:
            t=y['LTerms'][T]
            D=t['Disjunct']
            t['MFValue']=calc_dis(fis, D)
            
def composition(fis):
    A={}
    for Y in fis['Outputs']:
        y=fis['Outputs'][Y]
        N=y['NumOfPoints']
        LB=y['LeftB']
        RB=y['RightB']
        x_array=np.linspace(LB,RB,N)
        ts=y['LTerms']
        a={T: [min(calc_mf(ts[T]['MFunction'],z),ts[T]['MFValue']) for z in x_array] for T in ts}
        y_array=np.amax(np.array([a[T] for T in ts]),0)
        A[Y] = {'X': x_array, 'Y': y_array}
    return A
            
def defuzzyfication(fis, A):
    for Y in A:
        y = fis['Outputs'][Y]
        meth=y['DefMethod']
        y['Value'] = calc_defuzz(A[Y]['X'], A[Y]['Y'], meth)
    

        
def Run():    
    fis = read_fis('sample_laboratornaya2.json')
    read_inputs(fis)
    fuzzyfication(fis)
    fuzzyinference(fis)
    A = composition(fis)
    print()
    defuzzyfication(fis,A)
    for Y in fis['Outputs']:
        y=fis['Outputs'][Y]
        print(Y,':',f"{y['Value']:.2f}")   
        


if __name__=='__main__':
    Run()
    
