from django.http import HttpResponse

from django.template import loader
from django.shortcuts import render
import pandas as pd
import numpy as np
import plotly.express as px

from django import forms





class MyForm(forms.Form):
    my_choices = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices')
        super(MyForm, self).__init__(*args, **kwargs)
        self.fields['my_choices'].choices = choices


def index(request):
    valeursfoncieres_2022=pd.read_csv("valeursfoncieres-2022.txt", sep="|")

    valeursfoncieres_2022 = valeursfoncieres_2022.dropna(axis=1, how='all') #Supprime les colonnes vide
    valeursfoncieres_2022["Date mutation"] = pd.to_datetime(valeursfoncieres_2022["Date mutation"].str.strip(), format="%d/%m/%Y")#Convertit Date mutation en datetime 

    valeursfoncieres_2022["Valeur fonciere"] = valeursfoncieres_2022["Valeur fonciere"].astype(str).str.replace(",",".")
    valeursfoncieres_2022["Valeur fonciere"] = valeursfoncieres_2022["Valeur fonciere"].replace("nan", np.nan)
    valeursfoncieres_2022["Valeur fonciere"] = pd.to_numeric(valeursfoncieres_2022["Valeur fonciere"])

    valeursfoncieres_2022["Surface Carrez du 1er lot"] = valeursfoncieres_2022["Surface Carrez du 1er lot"].astype(str).str.replace(",",".")
    valeursfoncieres_2022["Surface Carrez du 1er lot"] = valeursfoncieres_2022["Surface Carrez du 1er lot"].replace("nan", np.nan)
    valeursfoncieres_2022["Surface Carrez du 1er lot"] = pd.to_numeric(valeursfoncieres_2022["Surface Carrez du 1er lot"])

    valeursfoncieres_2022["Surface Carrez du 2eme lot"] = valeursfoncieres_2022["Surface Carrez du 2eme lot"].astype(str).str.replace(",",".")
    valeursfoncieres_2022["Surface Carrez du 2eme lot"] = valeursfoncieres_2022["Surface Carrez du 2eme lot"].replace("nan", np.nan)
    valeursfoncieres_2022["Surface Carrez du 2eme lot"] = pd.to_numeric(valeursfoncieres_2022["Surface Carrez du 2eme lot"])
    
    #template = loader.get_template("template0.html")
    
    
        

    list_dep = set(valeursfoncieres_2022["Code departement"])
    list_dep -= {'30', '29'}
    list_dep = list(list_dep) 
    form = MyForm(choices=[(x,list_dep[x]) for x in range(len(list_dep))])
    
    
               
    D = valeursfoncieres_2022.loc[valeursfoncieres_2022["Code departement"] == 91] 
    D = D.dropna(subset=["Surface reelle bati"])
    D = D.dropna(subset=["Surface Carrez du 1er lot"])
    fig = px.scatter(D, x="Surface Carrez du 1er lot", y="Valeur fonciere", opacity = 0.65, trendline="ols",labels={
                     "Surface Carrez du 1er lot": "Surface Carrez"},)
    plot_html=fig.to_html(full_html=False, default_height=500, default_width=700)
    

    context ={
        'plot_html' : plot_html,
        'form' : form,
        }
    return render(request, "template0.html", context)
    #return HttpResponse(template.render(context, request))


def index1(request):
     return render(request, "template1.html", {})

def index2(request):
    valeursfoncieres_2022=pd.read_csv("valeursfoncieres-2022.txt", sep="|")

    valeursfoncieres_2022 = valeursfoncieres_2022.dropna(axis=1, how='all') #Supprime les colonnes vide
    valeursfoncieres_2022["Date mutation"] = pd.to_datetime(valeursfoncieres_2022["Date mutation"].str.strip(), format="%d/%m/%Y")#Convertit Date mutation en datetime 

    valeursfoncieres_2022["Valeur fonciere"] = valeursfoncieres_2022["Valeur fonciere"].astype(str).str.replace(",",".")
    valeursfoncieres_2022["Valeur fonciere"] = valeursfoncieres_2022["Valeur fonciere"].replace("nan", np.nan)
    valeursfoncieres_2022["Valeur fonciere"] = pd.to_numeric(valeursfoncieres_2022["Valeur fonciere"])

    valeursfoncieres_2022["Surface Carrez du 1er lot"] = valeursfoncieres_2022["Surface Carrez du 1er lot"].astype(str).str.replace(",",".")
    valeursfoncieres_2022["Surface Carrez du 1er lot"] = valeursfoncieres_2022["Surface Carrez du 1er lot"].replace("nan", np.nan)
    valeursfoncieres_2022["Surface Carrez du 1er lot"] = pd.to_numeric(valeursfoncieres_2022["Surface Carrez du 1er lot"])

    valeursfoncieres_2022["Surface Carrez du 2eme lot"] = valeursfoncieres_2022["Surface Carrez du 2eme lot"].astype(str).str.replace(",",".")
    valeursfoncieres_2022["Surface Carrez du 2eme lot"] = valeursfoncieres_2022["Surface Carrez du 2eme lot"].replace("nan", np.nan)
    valeursfoncieres_2022["Surface Carrez du 2eme lot"] = pd.to_numeric(valeursfoncieres_2022["Surface Carrez du 2eme lot"])

    plot_html = ""
    if(request.GET['region']=="Ile-de-France"):
        plot_html = IDF(valeursfoncieres_2022)
    if(request.GET['region']=="Auvergne-Rhône-Alpes"):
        plot_html = ARH(valeursfoncieres_2022)
    if(request.GET['region']=="Bourgogne-Franche-Comté"):
        plot_html = BFC(valeursfoncieres_2022)
    if(request.GET['region']=="Bretagne"):
        plot_html = B(valeursfoncieres_2022)
    if(request.GET['region']=="Centre-Val de Loire"):
           plot_html = CVL(valeursfoncieres_2022) 
    if(request.GET['region']=="Corse"):
           plot_html = C(valeursfoncieres_2022) 
    if(request.GET['region']=="Grand Est"):
           plot_html = GE(valeursfoncieres_2022) 
    if(request.GET['region']=="Hauts-de-France"):
           plot_html = HDF(valeursfoncieres_2022) 
    if(request.GET['region']=="Normandie"):
           plot_html = N(valeursfoncieres_2022) 
    if(request.GET['region']=="Nouvelle-Aquitaine"):
           plot_html = NA(valeursfoncieres_2022) 
    if(request.GET['region']=="Occitanie"):
           plot_html = O(valeursfoncieres_2022) 
    if(request.GET['region']=="Pays de la Loire"):
           plot_html = PDL(valeursfoncieres_2022) 
    if(request.GET['region']=="Provence-Alpes-Côte d'Azur"):
           plot_html = PACA(valeursfoncieres_2022) 
    if(request.GET['region']=="Outre-Mer"):
           plot_html = OM(valeursfoncieres_2022) 

    context ={
        'plot_html' : plot_html,
        }
    return render(request, "template2.html", context)

def OM(valeursfoncieres_2022):
    
    D = valeursfoncieres_2022

    D = D[(D["Surface reelle bati"]!=0)]
    D =  pd.concat([D.loc[D["Code departement"] == 971 ], D.loc[D["Code departement"] == 972 ], D.loc[D["Code departement"] == 973 ]
                    , D.loc[D["Code departement"] == 974 ]], ignore_index=True)
    D = D.dropna(subset=["Surface reelle bati"])
    D = D.dropna(subset=["Surface Carrez du 1er lot"])

    fig = px.scatter(D, x="Surface Carrez du 1er lot", y="Valeur fonciere", color="Code departement")
    return fig.to_html(full_html=False, default_height=500, default_width=700)

def PACA(valeursfoncieres_2022):
    
    D = valeursfoncieres_2022

    D = D[(D["Surface reelle bati"]!=0)]
    D =  pd.concat([D.loc[D["Code departement"] == 4 ], D.loc[D["Code departement"] == 5 ], D.loc[D["Code departement"] == 6 ]
                , D.loc[D["Code departement"] == 13 ], D.loc[D["Code departement"] == 83 ], D.loc[D["Code departement"] == 84 ]]
                , ignore_index=True)
    D = D.dropna(subset=["Surface reelle bati"])
    D = D.dropna(subset=["Surface Carrez du 1er lot"])

    fig = px.scatter(D, x="Surface Carrez du 1er lot", y="Valeur fonciere", color="Code departement")
    return fig.to_html(full_html=False, default_height=500, default_width=700)

def PDL(valeursfoncieres_2022):
    
    D = valeursfoncieres_2022

    D = D[(D["Surface reelle bati"]!=0)]
    D =  pd.concat([D.loc[D["Code departement"] == 44 ], D.loc[D["Code departement"] == 49 ], D.loc[D["Code departement"] == 53 ]
                , D.loc[D["Code departement"] == 72 ], D.loc[D["Code departement"] == 85 ]]
                , ignore_index=True)
    D = D.dropna(subset=["Surface reelle bati"])
    D = D.dropna(subset=["Surface Carrez du 1er lot"])

    fig = px.scatter(D, x="Surface Carrez du 1er lot", y="Valeur fonciere", color="Code departement")
    return fig.to_html(full_html=False, default_height=500, default_width=700)

def O(valeursfoncieres_2022):
    
    D = valeursfoncieres_2022

    D = D[(D["Surface reelle bati"]!=0)]
    D =  pd.concat([D.loc[D["Code departement"] == 9 ], D.loc[D["Code departement"] == 11 ], D.loc[D["Code departement"] == 12 ]
                , D.loc[D["Code departement"] == 30 ], D.loc[D["Code departement"] == 31 ], D.loc[D["Code departement"] == 32]
                , D.loc[D["Code departement"] == 34 ], D.loc[D["Code departement"] == 46 ], D.loc[D["Code departement"] == 48]
                , D.loc[D["Code departement"] == 65 ], D.loc[D["Code departement"] == 66 ], D.loc[D["Code departement"] == 81]
                , D.loc[D["Code departement"] == 82]]
                , ignore_index=True)
    D = D.dropna(subset=["Surface reelle bati"])
    D = D.dropna(subset=["Surface Carrez du 1er lot"])

    fig = px.scatter(D, x="Surface Carrez du 1er lot", y="Valeur fonciere", color="Code departement")
    return fig.to_html(full_html=False, default_height=500, default_width=700)

def NA(valeursfoncieres_2022):
    
    D = valeursfoncieres_2022

    D = D[(D["Surface reelle bati"]!=0)]
    D =  pd.concat([D.loc[D["Code departement"] == 16 ], D.loc[D["Code departement"] == 17 ], D.loc[D["Code departement"] == 19 ]
                , D.loc[D["Code departement"] == 23 ], D.loc[D["Code departement"] == 24 ], D.loc[D["Code departement"] == 33]
                , D.loc[D["Code departement"] == 40 ], D.loc[D["Code departement"] == 47 ], D.loc[D["Code departement"] == 64]
                , D.loc[D["Code departement"] == 79 ], D.loc[D["Code departement"] == 86 ], D.loc[D["Code departement"] == 87]]
                , ignore_index=True)
    D = D.dropna(subset=["Surface reelle bati"])
    D = D.dropna(subset=["Surface Carrez du 1er lot"])

    fig = px.scatter(D, x="Surface Carrez du 1er lot", y="Valeur fonciere", color="Code departement")
    return fig.to_html(full_html=False, default_height=500, default_width=700)

def N(valeursfoncieres_2022):
    
    D = valeursfoncieres_2022

    D = D[(D["Surface reelle bati"]!=0)]
    D =  pd.concat([D.loc[D["Code departement"] == 14 ], D.loc[D["Code departement"] == 27 ]
                , D.loc[D["Code departement"] == 50 ], D.loc[D["Code departement"] == 61 ], D.loc[D["Code departement"] == 76]]
                , ignore_index=True)
    D = D.dropna(subset=["Surface reelle bati"])
    D = D.dropna(subset=["Surface Carrez du 1er lot"])

    fig = px.scatter(D, x="Surface Carrez du 1er lot", y="Valeur fonciere", color="Code departement")
    return fig.to_html(full_html=False, default_height=500, default_width=700)

def HDF(valeursfoncieres_2022):
    
    D = valeursfoncieres_2022

    D = D[(D["Surface reelle bati"]!=0)]
    D =  pd.concat([D.loc[D["Code departement"] == 2 ], D.loc[D["Code departement"] == 59 ]
                , D.loc[D["Code departement"] == 60 ], D.loc[D["Code departement"] == 62 ], D.loc[D["Code departement"] == 80]]
                , ignore_index=True)
    D = D.dropna(subset=["Surface reelle bati"])
    D = D.dropna(subset=["Surface Carrez du 1er lot"])

    fig = px.scatter(D, x="Surface Carrez du 1er lot", y="Valeur fonciere", color="Code departement")
    return fig.to_html(full_html=False, default_height=500, default_width=700)

def GE(valeursfoncieres_2022):
    
    D = valeursfoncieres_2022

    D = D[(D["Surface reelle bati"]!=0)]
    D =  pd.concat([D.loc[D["Code departement"] == 8 ], D.loc[D["Code departement"] == 10 ]
                , D.loc[D["Code departement"] == 51 ], D.loc[D["Code departement"] == 52 ], D.loc[D["Code departement"] == 54 ]
                , D.loc[D["Code departement"] == 55 ], D.loc[D["Code departement"] == 88]]
                , ignore_index=True)
    D = D.dropna(subset=["Surface reelle bati"])
    D = D.dropna(subset=["Surface Carrez du 1er lot"])

    fig = px.scatter(D, x="Surface Carrez du 1er lot", y="Valeur fonciere", color="Code departement")
    return fig.to_html(full_html=False, default_height=500, default_width=700)

def C(valeursfoncieres_2022):
    
    D = valeursfoncieres_2022

    D = D[(D["Surface reelle bati"]!=0)]
    D =  pd.concat([D.loc[D["Code departement"] == "2A" ], D.loc[D["Code departement"] == "2B" ]]
                , ignore_index=True)
    D = D.dropna(subset=["Surface reelle bati"])
    D = D.dropna(subset=["Surface Carrez du 1er lot"])

    fig = px.scatter(D, x="Surface Carrez du 1er lot", y="Valeur fonciere", color="Code departement")
    return fig.to_html(full_html=False, default_height=500, default_width=700)

def CVL(valeursfoncieres_2022):
    
    D = valeursfoncieres_2022

    D = D[(D["Surface reelle bati"]!=0)]
    D =  pd.concat([D.loc[D["Code departement"] == 18 ], D.loc[D["Code departement"] == 28 ]
                , D.loc[D["Code departement"] == 36 ], D.loc[D["Code departement"] == 37 ]
                , D.loc[D["Code departement"] == 41 ], D.loc[D["Code departement"] == 45 ]]
                , ignore_index=True)
    D = D.dropna(subset=["Surface reelle bati"])
    D = D.dropna(subset=["Surface Carrez du 1er lot"])

    fig = px.scatter(D, x="Surface Carrez du 1er lot", y="Valeur fonciere", color="Code departement")
    return fig.to_html(full_html=False, default_height=500, default_width=700)


def B(valeursfoncieres_2022):
    
    D = valeursfoncieres_2022

    D = D[(D["Surface reelle bati"]!=0)]
    D =  pd.concat([D.loc[D["Code departement"] == 22 ], D.loc[D["Code departement"] == 29 ]
                , D.loc[D["Code departement"] == 35 ], D.loc[D["Code departement"] == 56 ]]
                , ignore_index=True)
    D = D.dropna(subset=["Surface reelle bati"])
    D = D.dropna(subset=["Surface Carrez du 1er lot"])

    fig = px.scatter(D, x="Surface Carrez du 1er lot", y="Valeur fonciere", color="Code departement")
    return fig.to_html(full_html=False, default_height=500, default_width=700)

def BFC(valeursfoncieres_2022):
    
    D = valeursfoncieres_2022

    D = D[(D["Surface reelle bati"]!=0)]
    D =  pd.concat([D.loc[D["Code departement"] == 21 ], D.loc[D["Code departement"] == 25 ]
                , D.loc[D["Code departement"] == 39 ], D.loc[D["Code departement"] == 58 ], D.loc[D["Code departement"] == 70 ]
                , D.loc[D["Code departement"] == 71 ], D.loc[D["Code departement"] == 89], D.loc[D["Code departement"] == 90]]
                , ignore_index=True)
    D = D.dropna(subset=["Surface reelle bati"])
    D = D.dropna(subset=["Surface Carrez du 1er lot"])

    fig = px.scatter(D, x="Surface Carrez du 1er lot", y="Valeur fonciere", color="Code departement")
    return fig.to_html(full_html=False, default_height=500, default_width=700)

def ARH(valeursfoncieres_2022):
    
    D = valeursfoncieres_2022

    D = D[(D["Surface reelle bati"]!=0)]
    D =  pd.concat([D.loc[D["Code departement"] == 1 ], D.loc[D["Code departement"] == 3 ]
                , D.loc[D["Code departement"] == 7 ], D.loc[D["Code departement"] == 15 ], D.loc[D["Code departement"] == 26 ]
                , D.loc[D["Code departement"] == 38 ], D.loc[D["Code departement"] == 42], D.loc[D["Code departement"] == 43]
                , D.loc[D["Code departement"] == 63 ], D.loc[D["Code departement"] == 69 ], D.loc[D["Code departement"] == 73 ]
                , D.loc[D["Code departement"] == 74 ]], ignore_index=True)
    D = D.dropna(subset=["Surface reelle bati"])
    D = D.dropna(subset=["Surface Carrez du 1er lot"])

    fig = px.scatter(D, x="Surface Carrez du 1er lot", y="Valeur fonciere", color="Code departement")
    return fig.to_html(full_html=False, default_height=500, default_width=700)

def IDF(valeursfoncieres_2022):

    D = valeursfoncieres_2022

    D = D[(D["Surface reelle bati"]!=0)]
    D =  pd.concat([D.loc[D["Code departement"] == 75 ], D.loc[D["Code departement"] == 77 ]
                , D.loc[D["Code departement"] == 78 ], D.loc[D["Code departement"] == 91 ], D.loc[D["Code departement"] == 92 ]
                , D.loc[D["Code departement"] == 93 ], D.loc[D["Code departement"] == 94], D.loc[D["Code departement"] == 94]
                , D.loc[D["Code departement"] == 95 ]], ignore_index=True)
    D = D.dropna(subset=["Surface reelle bati"])
    D = D.dropna(subset=["Surface Carrez du 1er lot"])

    fig = px.scatter(D, x="Surface Carrez du 1er lot", y="Valeur fonciere", color="Code departement")
    return fig.to_html(full_html=False, default_height=500, default_width=700)
