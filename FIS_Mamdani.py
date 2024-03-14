import json as j
import BasicFuzzyFunctions as bf
import numpy as np
import matplotlib.pyplot as plt


def read_fis(jf):
    with open(jf, 'r') as f:
        return j.load(f)

################# Просмотр JSON файла ####################
def j_to_str(d):                                         #
    return j.dumps(d, ensure_ascii=False, indent=4)      #
##########################################################

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
        a=mf['Parameters']['a']
        b=mf['Parameters']['b']
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
#####################################
    MI={}                           #
#####################################
    for X in fis['Inputs']:
        x=fis['Inputs'][X]
#####################################
        N=100                       #
        LB=x['LeftB']               #
        RB=x['RightB']              #
        x_array=np.linspace(LB,RB,N)#
        MI[X]={}                    #
#####################################
        for T in x['LTerms']:
            t=x['LTerms'][T]
            t['MFValue']=calc_mf(t['MFunction'],x['Value'])
##############################################################################
            MI[X][T]={}                                                      #
            MI[X][T]['X']=x_array                                            #
            MI[X][T]['Y']=np.array([calc_mf(t['MFunction'],z) for z in x_array]) #        
##############################################################################
    return MI

            
def fuzzyinference(fis):
    for Y in fis['Outputs']:
        y=fis['Outputs'][Y]
        for T in y['LTerms']:
            t=y['LTerms'][T]
            D=t['Disjunct']
            t['MFValue']=calc_dis(fis, D)
            
def composition(fis):
    A={}
#########################################
    M={}                                #
    B={}                                #
#########################################
    for Y in fis['Outputs']:
        y=fis['Outputs'][Y]
        N=y['NumOfPoints']
        LB=y['LeftB']
        RB=y['RightB']
        x_array=np.linspace(LB,RB,N)
        ts=y['LTerms']
#########################################################################
        m={T: [calc_mf(ts[T]['MFunction'],z) for z in x_array] for T in ts} #
#########################################################################
        a={T: [min(calc_mf(ts[T]['MFunction'],z),ts[T]['MFValue']) for z in x_array] for T in ts}
        y_array=np.amax(np.array([a[T] for T in ts]),0)
#########################################################################
        M[Y] = {T: {'X': x_array, 'Y': m[T]} for T in ts}               #
        B[Y] = {T: {'X': x_array, 'Y': a[T]} for T in ts}               #
#########################################################################
        A[Y] = {'X': x_array, 'Y': y_array}
    return A, B, M
            
def defuzzyfication(fis, A):
    for Y in A:
        y = fis['Outputs'][Y]
        meth = y['DefMethod']
        y['Value'] = calc_defuzz(A[Y]['X'], A[Y]['Y'], meth)


############################################################
def get_depth(A):                                          #
    if type(A) not in {list, dict, np.ndarray}:            #
        return 0                                           #
    else:                                                  #
        if type(A)==dict:                                  #
            return max([get_depth(A[x]) for x in A]) +1    #
        else:                                              #
            return max([get_depth(x) for x in A]) + 1      #
                                                           #
def Graph_Show(aA):                                        #
    n=0                                                    #
    K=sum([len(A) for A in aA])                            #
    fig, axs = plt.subplots(K, 1, figsize=(10, 2.5*K))     #
    plt.subplots_adjust(hspace=0.5)                        #
    for A in aA:                                           #
        for X in A:                                        #
            if K>1:                                        #
                axs[n].set_title(X)                        #
            else:                                          #
                axs.set_title(X)                           #
            if get_depth(A)>3:                             #
                for T in A[X]:                             #
                    if K>1:                                ###################
                        axs[n].plot(A[X][T]['X'], A[X][T]['Y'], linewidth=3) #
                    else:                                                    #
                        axs.plot(A[X][T]['X'], A[X][T]['Y'], linewidth=3)    #
            else:                                                            #
                if K>1:                                                      #
                    axs[n].plot(A[X]['X'], A[X]['Y'], linewidth=3)           #
                else:                                                        #
                    axs.plot(A[X]['X'], A[X]['Y'], linewidth=3)              #
            n+=1                                                             #
    plt.show()                                                               #
##############################################################################


def Run():    
    fis = read_fis('sample_laboratornaya2.json')
    read_inputs(fis)
    MI = fuzzyfication(fis)
    #########################
    Graph_Show([MI])        #
    #########################
    fuzzyinference(fis)
    A, B, M = composition(fis)
    print()
    defuzzyfication(fis,A)
    for Y in fis['Outputs']:
        y=fis['Outputs'][Y]
        print(Y,':',f"{y['Value']:.2f}")   
    #########################
    Graph_Show([M, B, A])   #
    #########################
        


if __name__=='__main__':
    Run()
    
