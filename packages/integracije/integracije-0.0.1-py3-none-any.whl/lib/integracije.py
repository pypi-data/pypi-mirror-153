import pandas as pd
import graphviz as gv

def integracije(podatki, excel_Aplikacije_stolpca="Aplikacija/sistem, Komponenta", dodatno_Aplikacije="", excel_Vmesniki_stolpci="Izvor, Ponor, Smer",  dodatno_Vmesniki="", output_format="jpg", file_name="Integracije", zdruzi_povezave=False):
    # STRING, LOČENO Z VEJICAMI -> ARRAYS
    if dodatno_Aplikacije == '':
        specifikacijeAplikacij = []
    else:
        specifikacijeAplikacij = dodatno_Aplikacije.split(', ')
    if dodatno_Vmesniki == '' or zdruzi_povezave:
        specifikacijeVmesnikov = []
    else:
        specifikacijeVmesnikov = dodatno_Vmesniki.split(', ')
    colApl = excel_Aplikacije_stolpca.split(', ')
    colVme = excel_Vmesniki_stolpci.split(', ')

    # BRANJE IZ DATOTEKE
    df_apl = pd.read_excel (podatki, engine='openpyxl', sheet_name='Seznam sistemov', header = None).dropna(how='all')
    df_apl.dropna(axis=1, how='all', inplace=True)
    df_apl.columns = df_apl.iloc[0]
    df_apl = df_apl.iloc[1:].reset_index(drop=True)
    df_vme = pd.read_excel (podatki, engine='openpyxl', sheet_name='Tabela integracij', header = None).dropna(how='all')
    df_vme.dropna(axis=1, how='all', inplace=True)
    df_vme.columns = df_vme.iloc[0]
    df_vme = df_vme.iloc[1:].reset_index(drop=True)

    # PREVERJANJE USTREZNOSTI IMEN STOLPCEV:
    stolpci_apl = df_apl.columns.values.tolist()
    for i in range(2):
        if colApl[i] not in stolpci_apl:
            print("Stolpec {} v prvi xlsx datoteki ne obstaja.".format(colApl[i]))
            return
    for i in specifikacijeAplikacij:
        if i not in stolpci_apl:
            print("Stolpec {} v prvi xlsx datoteki ne obstaja.".format(str(i)))
            return
    stolpci_vme = df_vme.columns.values.tolist()
    for i in range(3):
        if colVme[i] not in stolpci_vme:
            print("Stolpec {} v drugi xlsx datoteki ne obstaja.".format(colVme[i]))
            return
    for i in specifikacijeVmesnikov:
        if i not in stolpci_vme:
            print("Stolpec {} v drugi xlsx datoteki ne obstaja.".format(str(i)))
            return

    # PRETVORI SMER V >/</<>
    optionsRight = ['>', '->', '-->', '--->', '---->', 'desno', 'right']
    optionsLeft = ['<', '<-', '<--', '<---', '<----', 'levo', 'left']
    for i in range(len(df_vme)):
        if pd.isnull(df_vme[colVme[2]][i]):
            continue
        elif str(df_vme[colVme[2]][i]).lower() in optionsRight:
            df_vme[colVme[2]][i] = '>'
        elif str(df_vme[colVme[2]][i]).lower() in optionsLeft:
            df_vme[colVme[2]][i] = '<'
        else:
            df_vme[colVme[2]][i] = '<>'

    # USTVARI GRAF
    graf = gv.Digraph('Integracije', filename='structs.gv', node_attr={'shape': 'plaintext'}, format=output_format.lower(), engine='dot')
    graf.attr(label = 'Sistem aplikacij in vmesnikov') # ime grafa
    graf.attr(compound='true') 

    # SEZNAM APLIKACIJ IN KOMPONENT, DA JIH JE LAŽJE IZRISAT
    dictApl = {}
    rowApl = {}
    # vpiše vse aplikacije in komponente
    for i in range(len(df_apl)):
        if not pd.isnull(df_apl[colApl[0]][i]):
            apl = str(df_apl[colApl[0]][i])
            dictApl[apl] = []
            rowApl[apl] = i
            if not pd.isnull(df_apl[colApl[1]][i+1]):
                while i<len(df_apl)-1 and not pd.isnull(df_apl[colApl[1]][i+1]):
                    part = str(df_apl[colApl[1]][i+1]).partition('.')
                    if part[0] != apl:
                        print("Komponenta " + str(df_apl[colApl[1]][i+1]) + " se ne ujema z aplikacijo.")
                        break
                    dictApl[apl].append(part[2].upper())
                    rowApl[apl + '.' + part[2].upper()] = i+1
                    i += 1
    brezPovezav = [] 
    for i in dictApl: 
        brezPovezav.append(i) 
    # preveri, ali so vse aplikacije in komponente iz tabele z vmesniki v slovarju, sicer doda
    for i in range(len(df_vme)):
        if not pd.isnull(df_vme[colVme[0]][i]):

            # preveri, ali je izvor v slovarju
            part = str(df_vme[colVme[0]][i]).partition('.')
            if part[2] != "":
                if not part[0] in dictApl:
                    dictApl[part[0]] = [part[2].upper()]
                    rowApl[part[0]] = -1
                    rowApl[part[0] + "." + part[2].upper()] = -1
                elif not part[2].upper() in dictApl[part[0]]:
                    dictApl[part[0]].append(part[2].upper())
                    rowApl[part[0] + "." + part[2].upper()] = -1
            else:
                if not part[0] in dictApl:
                    dictApl[part[0]] = []
                    rowApl[part[0]] = -1
            if part[0] in brezPovezav: 
                brezPovezav.remove(part[0]) 

            # preveri, ali je ponor v slovarju
            part = str(df_vme[colVme[1]][i]).partition('.')
            if part[2] != "":
                if not part[0] in dictApl:
                    dictApl[part[0]] = [part[2].upper()]
                    rowApl[part[0]] = -1
                    rowApl[part[0] + "." + part[2].upper()] = -1
                elif not part[2].upper() in dictApl[part[0]]:
                    dictApl[part[0]].append(part[2].upper())
                    rowApl[part[0] + "." + part[2].upper()] = -1
            else:
                if not part[0] in dictApl:
                    dictApl[part[0]] = []
                    rowApl[part[0]] = -1
            if part[0] in brezPovezav: 
                brezPovezav.remove(part[0]) 
    
    # IZRIS APLIKACIJ BREZ POVEZAV (vozlišča)
    with graf.subgraph() as c:
        c.attr(rank='min')
        for apl in brezPovezav:
            # na koncu jih izbriši iz dictApl, da jih naslednja zanka preskoči
            # info o aplikaciji
            if rowApl[apl] == -1:
                infoA = '*'
            else:
                infoA = ""
                for sp in specifikacijeAplikacij:
                    if not pd.isnull(df_apl[sp][rowApl[apl]]):
                        infoA = infoA + '<BR/>' + str(df_apl[sp][rowApl[apl]])
            # komponente in info o njih
            kom = ""
            for i in dictApl[apl]:
                if rowApl[apl+'.'+i.upper()] == -1:
                    infoK = '*'
                else:
                    infoK = ""
                    for sp in specifikacijeAplikacij:
                        if not pd.isnull(df_apl[sp][rowApl[apl+'.'+i.upper()]]):
                            infoK = infoK + '<BR/>' + str(df_apl[sp][rowApl[apl+'.'+i.upper()]])
                kom = kom + '<TD CELLSPACING="20" BORDER="2" PORT="' + apl + "." + i + '">' + i + infoK + '</TD> '
            if kom == "":
                kom = '<TD> </TD> '
            # izris vozlišča
            c.node(apl, '''<
            <TABLE PORT="''' + apl + '''" BORDER="1" CELLBORDER="0" CELLPADDING="5">
            <TR> <TD COLSPAN="''' + str(len(dictApl[apl])+1) +  '''"><B>''' + apl + '''</B>''' + infoA + '''</TD> </TR>
            <TR>
                ''' + kom + '''
            </TR>
            </TABLE>>''')
            del dictApl[apl]

    # IZRIS APLIKACIJ (vozlišča)
    for apl in dictApl:
        # info o aplikaciji
        if rowApl[apl] == -1:
            infoA = '*'
        else:
            infoA = ""
            for sp in specifikacijeAplikacij:
                if not pd.isnull(df_apl[sp][rowApl[apl]]):
                    infoA = infoA + '<BR/>' + str(df_apl[sp][rowApl[apl]])
        # komponente in info o njih
        kom = ""
        for i in dictApl[apl]:
            if rowApl[apl+'.'+i.upper()] == -1:
                infoK = '*'
            else:
                infoK = ""
                for sp in specifikacijeAplikacij:
                    if not pd.isnull(df_apl[sp][rowApl[apl+'.'+i.upper()]]):
                        infoK = infoK + '<BR/>' + str(df_apl[sp][rowApl[apl+'.'+i.upper()]])
            kom = kom + '<TD CELLSPACING="20" BORDER="2" PORT="' + apl + "." + i + '">' + i + infoK + '</TD> '
        if kom == "":
            kom = '<TD> </TD> '
        # izris vozlišča
        graf.node(apl, '''<
        <TABLE PORT="''' + apl + '''" BORDER="1" CELLBORDER="0" CELLPADDING="5">
        <TR> <TD COLSPAN="''' + str(len(dictApl[apl])+1) +  '''"><B>''' + apl + '''</B>''' + infoA + '''</TD> </TR>
        <TR>
            ''' + kom + '''
        </TR>
        </TABLE>>''')

    # IZRIS VMESNIKOV (vozlišča za vmesnike in povezave od aplikacij do vmesnikov)
    if zdruzi_povezave:
        povezave = []
    for i in range(1, len(df_vme)):
        if not pd.isnull(df_vme[colVme[0]][i]):
            #preveri, če taka povezava že obstaja
            if zdruzi_povezave:
                if [str(df_vme[colVme[0]][i]).upper(),  str(df_vme[colVme[2]][i]).upper()] in povezave:
                    continue
                povezave.append([str(df_vme[colVme[0]][i]).upper(),  str(df_vme[colVme[2]][i]).upper()])

            # naredi node za vmesnik
            info = ""
            for sp in specifikacijeVmesnikov:
                if not pd.isnull(df_vme[sp][i]):
                    info = info + '<BR/>' + str(df_vme[sp][i])
            info = info.replace('<BR/>', '', 1)
            graf.node(str(i), '''<
            <TABLE PORT="''' + str(i) + '''" BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="lightgrey"> 
            <TR>
                <TD> </TD>
                <TD WIDTH = "42"> <FONT POINT-SIZE="12">''' + info + ''' </FONT> </TD>
                <TD> </TD>
            </TR>
            </TABLE>>''')

            # izvor in ponor v pravi obliki
            part = df_vme[colVme[0]][i].partition('.')
            if part[2] == "":
                izvor = part[0]
            else:
                izvor =  part[0] + ':' + part[0] + '.' + part[2].upper()
            part = df_vme[colVme[1]][i].partition('.')
            if part[2] == "":
                ponor = part[0]
            else:
                ponor =  part[0] + ':' + part[0] + '.' + part[2].upper()

            # poveže z aplikacijama
            if df_vme[colVme[2]][i] == '>':
                graf.edge(izvor + ':c', str(i), arrowsize='0.5')
                graf.edge(str(i), ponor + ':c', arrowsize='0.5')
            elif df_vme[colVme[2]][i] == '<':
                graf.edge(ponor + ':c', str(i), arrowsize='0.5')
                graf.edge(str(i), izvor + ':c', arrowsize='0.5')
            else:
                graf.edge(izvor + ':c', str(i), arrowsize='0.5', dir='both')
                graf.edge(str(i), ponor + ':c', arrowsize='0.5', dir='both')

    # IZRIS
    graf = graf.unflatten(stagger=2, fanout=True)
    graf.render(file_name, view=True)