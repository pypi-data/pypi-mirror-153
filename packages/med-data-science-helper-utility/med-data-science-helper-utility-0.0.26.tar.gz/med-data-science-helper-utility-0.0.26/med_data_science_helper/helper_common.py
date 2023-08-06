# -*- coding: utf-8 -*-
"""
Created on Fri May 27 11:48:20 2022

@author: User
"""



def get_niveles_grados_por_modalidad(modalidad=None,id_nivel_list=None, grado_list=None,rt_ngm=True,rt_key=False,rt_niveles=False):
    # returna lista de id grado, dsc grado y media de edad en ese grado por cada nivel educativo
    id_nivel_list_ = [] 
    if modalidad=="EBE":
        id_nivel_list_ = ["E0","E1","E2"]
    elif modalidad=="EBR":
        id_nivel_list_ = ["A1","A2","A3","A5","B0","F0"]
    elif modalidad is None:
        modalidad = "EBR_EBE"
        id_nivel_list_ = ["A1","A2","A3","A5","B0","F0","E0","E1","E2"]        
    else:
        return
    
    if id_nivel_list is None:
        id_nivel_list = id_nivel_list_
    
    list_dict_niv_gr = []   
     
    
    for id_nivel_ in id_nivel_list:
        dict_niv_gr={}
        list_id_grados_ = []
        list_dsc_grados_ = []
        if id_nivel_=="E0":
            #list_id_grados_ = [(1,"0 a 2 anios",1)]
            list_id_grados_ = [(1,"0_2_ANIOS",1)]
            
        if id_nivel_=="E1":
            list_id_grados_ = [(3,"3_ANIOS",3),(4,"4_ANIOS",4),(5,"5_ANIOS",5)]
            
        if id_nivel_=="E2":
            list_id_grados_ = [(6,"PR_1ERO",7),(7,"PR_2DO",8),(8,"PR_3ERO",10),(9,"PR_4TO",11),(10,"PR_5TO",13),(11,"PR_6TO",14)]
        
        if id_nivel_=="A1":
            list_id_grados_ = [(1,"0_2_ANIOS",2)]
        
        if id_nivel_=="A2":
            list_id_grados_ = [(3,"GP_3_ANIOS",3),(4,"GP_4_ANIOS",4),(5,"GP_5_ANIOS",5)]
            
        if id_nivel_=="A3":
            list_id_grados_ = [(1,"0_2_ANIOS",2),(2,"3_ANIOS",3),(3,"4_ANIOS",4),(4,"5_ANIOS",5)]
            
        if id_nivel_=="A5":
            list_id_grados_ = [(1,"0_2_ANIOS",2),(2,"3_ANIOS",3),(3,"4_ANIOS",4),(4,"5_ANIOS",5)]
        
        if id_nivel_=="B0":
            list_id_grados_ = [(4,"PR_1ERO",6),(5,"PR_2DO",7),(6,"PR_3ERO",8),(7,"PR_4TO",9),(8,"PR_5TO",10),(9,"PR_6TO",11)]
            
        if id_nivel_=="F0":
            list_id_grados_ = [(10,"SC_1ERO",12),(11,"SC_2DO",13),(12,"SC_3ERO",14),(13,"SC_4TO",15),(14,"SC_5TO",16)]  
            
        dict_niv_gr["id_nivel"]=id_nivel_
        
        if grado_list is not None:
            dict_niv_gr["list_grados"]=grado_list
        else:
            dict_niv_gr["list_grados"]=list_id_grados_
            
        list_dict_niv_gr.append(dict_niv_gr)
    
    list_return = []
    if (rt_ngm):    
        list_return.append(list_dict_niv_gr)
        
    list_niveles = []   
        
    list_key = []
    list_key.append(modalidad)
    
    for item in list_dict_niv_gr:

        id_nivel = item["id_nivel"]
        list_niveles.append(id_nivel)
        list_grados = item["list_grados"]
        list_key.append(str(id_nivel))

        for grado in list_grados:

            if isinstance(grado, tuple):
                ID_GRADO = grado[0]
            else:
                ID_GRADO = grado

            list_key.append(str(ID_GRADO))

    key_str = '_'.join(list_key)
    
    if rt_key:
        list_return.append(key_str)
        
    if rt_niveles:
        list_return.append(list_niveles)
        
    return tuple(list_return) if len(list_return)>1 else list_return[0]



def get_edad_promedio(id_nivel=None,id_grado=None):
    edad_promedio = None
    list_dict_niv_gr = get_niveles_grados_por_modalidad()

    for item in list_dict_niv_gr:
        id_nivel_ = item["id_nivel"]

        if (id_nivel_==id_nivel):

            list_grados = item["list_grados"]

            for grado in list_grados:
                id_grado_ = grado[0]
                if (id_grado_==id_grado):
                    edad_promedio = grado[2]
                    
    return edad_promedio


def get_label_grado(id_nivel=None,id_grado=None):
    label_grado = None
    list_dict_niv_gr = get_niveles_grados_por_modalidad()

    for item in list_dict_niv_gr:
        id_nivel_ = item["id_nivel"]

        if (id_nivel_==id_nivel):

            list_grados = item["list_grados"]

            for grado in list_grados:
                id_grado_ = grado[0]
                if (id_grado_==id_grado):
                    label_grado = grado[1]
                    
    return id_nivel+"_"+label_grado



#print(get_label_grado(id_nivel="E0",id_grado=1))
