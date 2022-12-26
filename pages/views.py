from django.shortcuts import render
from django.http import HttpResponse
from queue import PriorityQueue 
# Create your views here.
GR = {'Arad':{'Zerind':75,'Timisoara':118,'Sibiu':140},
         'Zerind':{'Oradea':71,'Arad':75},
         'Oradea':{'Sibiu',151},
         'Sibiu':{'Rimniciu Vilcea':80,'Fagaras':99,'Arad':140},
         'Fagaras':{'Sibiu':99,'Bucharest':211},
         'Rimniciu Vilcea':{'Pitesti':97,'Craiova':146,'Sibiu':80},
         'Timisoara':{'Lugoj':111,'Arad':118},
         'Lugoj':{'Mehadia':70},
         'Mehadia':{'Lugoj':70,'Dorbeta':75},
         'Dorbeta':{'Mehadia':75,'Craiova':120},
         'Pitesti':{'Craiova':138,'Bucharest':101},
         'Craiova':{'Pitesti':138,'Dorbeta':120,'Rimniciu Vilcea':146},
         'Bucharest':{'Giurgiu':90,'Urziceni':85,'Fagaras':211,'Pitesti':101},
         'Giurgiu': {'Bucharest':90},
         'Urziceni':{'Vaslui':142,'Hirsova':98,'Bucharest':85},
         'Vaslui':{'Lasi':92,'Urziceni':142},
         'Lasi':{'Neamt':87,'Vaslui':92},
         'Neamt':{'Lasi':87},
         'Hirsova':{'Eforie':86,'Urziceni':98},
         'Eforie':{'Hirsova':86}
         }
S_L = {
        'Arad': 366,
        'Zerind': 374,
        'Oradea': 380,
        'Sibiu': 253,
        'Fagaras': 176,
        'Rimniciu Vilcea': 193,
        'Timisoara': 329,
        'Lugoj': 244,
        'Mehadia': 241,
        'Dorbeta': 242,
        'Pitesti': 100,
        'Craiova': 160,
        'Bucharest': 0,
        'Giurgiu': 77,
        'Urziceni': 80,
        'Vaslui': 199,
        'Lasi': 226,
        'Neamt': 234,
        'Hirsova': 151,
        'Eforie': 161
    } 

def a_star(FROM, TOO):
   
    PQ,VSTD = PriorityQueue(),{}
    PQ.put((S_L[FROM], 0, FROM, [FROM]))
    VSTD[FROM] = S_L[FROM]
    Queue =[0]*(1000)
    x=0
    while not PQ.empty():
        (HEURISTIC, cost, vertex, path) = PQ.get()
        Queue[x] =  HEURISTIC, cost, vertex, path
        if vertex == TOO:
           return Queue,HEURISTIC, cost, path
        for NEXT in GR[vertex].keys():
            COST = cost + GR[vertex][NEXT]
            HEURISTIC = COST + S_L[NEXT]
            if not NEXT in VSTD or VSTD[NEXT] >= HEURISTIC:
                VSTD[NEXT] = HEURISTIC
                PQ.put((HEURISTIC, COST, NEXT,path + [NEXT]))
        x+=1

def index (request):
    FC = None
    SC = None
    HEURISTIC =None
    cost = None
    Queue = None
    New = None
    Heu = None
    conn =None
    Wet = None 
    if 'on' in request.GET:
        if 'FC' in request.GET:
            FC = request.GET['FC']
        if 'SC' in request.GET:
            SC = request.GET['SC']
        if FC not in GR or SC not in GR:           
            exs="CITY DOES NOT EXIST."
            return render(request , 'pages/index.html',{'exc':exs ,'f':FC,'s':SC})
        else:
            Queue = [0]*(100)
            Queue,HEURISTIC, cost, optimal_path = a_star(FC, SC)
            return render(request,'pages/index.html',{'f':FC ,'s':SC ,'H':HEURISTIC,'C':cost,'Q':Queue ,'y':GR})
    if 'tos' in request.GET:
        if 'New' in request.GET:
            New = request.GET['New']    
            if 'Wet' in request.GET:
                Wet= request.GET['Wet']
                S_L[New]=int(Wet)
        if 'Connctio' in request.GET:
            conn = request.GET['Connctio']    
            if 'Heu' in request.GET:
                Heu = request.GET['Heu']
                if New in GR:
                    GR[New][conn]=int(Heu)
                    GR[conn][New]=int(Heu)
                if New not in GR:
                    GR[New]={conn:int(Heu)}
                    GR[conn][New]=int(Heu)
        return render(request,'pages/index.html',{'NEW':New ,'Conn':conn ,'He':Heu,'C':cost,'G':GR,'a':S_L,'y':GR})
    else:
        return render(request,'pages/index.html',{'y':GR })

