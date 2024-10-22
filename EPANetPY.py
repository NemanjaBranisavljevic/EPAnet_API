import pyodbc # Requires pip install pyodbc
from subprocess import call

class EPANetModel:
    """ EPANetModel - Osnovna klasa ovog API-a."""
    """ U objektima ove klase se cuvaju svi podaci potrebni za simulaciju u programskom paketu EPANet. """
    """ Objekti se cuvaju u sledecim strukturama: """
    """  """
    """ TITLE (lista) - Naziv simulacije. """
    """ JUNCTIONS (lista) - Lista objekata sa podacima o cvorovima u mrezi. """
    """ RESERVOIRS (lista) - Lista objekata sa podacima o akumulacijama i izvoristima. """
    """ TANKS (lista) - Lista objekata sa podacima o rezervoarima. """
    """ PIPES (lista) - Lista objekata sa podacima o cevima u mrezi. """
    """ PUMPS (lista) - Lista objekata sa podacima o pumpama u mrezi. """
    """ VALVES (lista) - Lista objekata sa podacima o zatvaracima u mrezi. """
    """ TAGS (lista) - Lista objekata sa podacima o oznakama. """
    """ DEMANDS (lista) - Lista objekata sa podacima o cvornoj potrosnji. """
    """ STATUS (lista) - Lista objekata sa podacima o statusu linkova u mrezi (cevima, pumpama i zatvaracima). """
    """ PATTERNS (lista) - Lista objekata sa podacima o sablonima potrosnje. """
    """ CURVES (lista) - Lista objekata sa podacima o krivama (parakteristike pumpi, itd.). """
    """ CONTROLS (lista) - Lista sa podacima o kontrolama. """
    """ RULES (lista) - Lista objekata sa podacima o slozenijim kontrolama. """
    """ ENERGY (asocijativna tabela) - Tabela sa podacima neophodnim za izracunavanje bilansa energije. """
    """ EMITTERS (lista) - Lista objekata sa podacima o emiterima. """
    """ QUALITY (lista) - Lista objekata sa podacima o kvalitetu vode. """
    """ SOURCES (lista) - Lista objekata sa podacima o izvorima vode odredjenog kvaliteta. """
    """ REACTIONS (lista) - Lista objekata sa podacima vezanim za hemijske reakcije. """
    """ REACTIONS_1 (asocijativna tabela) - Tabela sa podacima o hemijskim reakcijama. """
    """ MIXING (lista) - Lista objekata sa podacima o o nacinima mesanja vode u rezervorima. """ 
    """ IMES (asocijativna tabela) - Tabela sa vremenskim podacima vezanim za simulaciju. """ 
    """ REPORT (asocijativna tabela) - Tabela sa podacima o nacinu formiranja izvestaja. """
    """ OPTIONS (asocijativna tabela) - Tabela sa podacima o opcijama vezanim za simulaciju. """
    """ LABELS (lista) - Lista objekata sa podacima o oznakama. """
    """ BACKDROP (asocijativna tabela) - Tabela sa podacima o pozadisnkoj slici. """
    """ META (asocijativna tabela) - Tabela sa meta-podacima o verziji modela. """

    """ RES_NODES (lista) - Lista objekata sa rezultatima simulcije vezanim za cvorove, izvorista i rezervore. """  
    """ RES_LINKS (lista) - Lista objekata sa rezultatima simulcije vezanim za cevi, pumpe i zatavrace. """


    def __init__(self): 

        self.TITLE=[]
        self.JUNCTIONS=[]
        self.RESERVOIRS=[]
        self.TANKS=[]
        self.PIPES=[]
        self.PUMPS=[]
        self.VALVES=[]
        self.TAGS=[]
        self.DEMANDS=[]
        self.STATUS=[]
        self.PATTERNS=[]
        self.CURVES=[]
        self.CONTROLS=[]
        self.RULES=[]
        self.ENERGY={}
        self.EMITTERS=[]
        self.QUALITY=[]
        self.SOURCES=[]
        self.REACTIONS=[]
        self.REACTIONS_1={}#drugi odeljak koji se zove [REACTIONS]?!?
        self.MIXING=[]
        self.TIMES={}
        self.REPORT={}
        self.OPTIONS={}
        self.LABELS=[]
        self.BACKDROP={}
        self.META={'Version': None, 'VersionDate': None, 'SimulationName': None, 'Description': None}

        #Rezultati
        self.RES_NODES=[]
        self.RES_LINKS=[]

    def readINP(self, filenameINP):
        """ readINP - metoda klase EPANetModel za ucitavanje podataka iz *.INP fajla"""
        """ Ulaz ove metode predstavlja putanja do *.INP fajla, ulaznog fajla EPANet programskog paketa. """

        sections=["TITLE","JUNCTIONS", "RESERVOIRS", "TANKS", "PIPES", "PUMPS", "VALVES", "TAGS", "DEMANDS", "STATUS", "PATTERNS", "CURVES", "CONTROLS", "RULES", "ENERGY", "EMITTERS", "QUALITY", "SOURCES", "REACTIONS", "MIXING", "TIMES", "REPORT", "OPTIONS", "COORDINATES", "VERTICES", "LABELS", "BACKDROP","END"]

        section=""


        f=open(filenameINP, 'r')
        for line in f:
            if not line == '\n':                          
                line_list=line.split()
                if line_list[0][1:-1] in sections:
                    section=line_list[0][1:-1]
                    #print section                        
                    continue

                line_list=[x.strip() for x in line.split("\t")]
                if section=="TITLE":                          
                        self.TITLE.append(line_list[0])

                if section=="JUNCTIONS":
                    if line[0]==";": continue
                    else:                            
                        self.JUNCTIONS.append(JUNCTION(line_list[0], float(line_list[1]), float(line_list[2]), line_list[3], line_list[4]))

                elif section=="RESERVOIRS":
                    if line[0]==";": continue
                    else:  
                        self.RESERVOIRS.append(RESERVOIR(line_list[0], float(line_list[1]), line_list[2], line_list[3]))

                elif section=="TANKS":
                    if line[0]==";": continue
                    else:  
                        self.TANKS.append(TANK(line_list[0], float(line_list[1]), float(line_list[2]), float(line_list[3]), float(line_list[4]), float(line_list[5]), float(line_list[6]), line_list[7], line_list[8]))

                elif section=="PIPES":
                    if line[0]==";": continue
                    else:  

                        node1=[x for x in self.JUNCTIONS+self.RESERVOIRS+self.TANKS if x.ID==line_list[1]]
                        node2=[x for x in self.JUNCTIONS+self.RESERVOIRS+self.TANKS if x.ID==line_list[2]]

                        self.PIPES.append(PIPE(line_list[0], node1[0], node2[0], float(line_list[3]), float(line_list[4]), float(line_list[5]), float(line_list[6]), line_list[7], line_list[8]))


                elif section=="PUMPS":
                    if line[0]==";": continue
                    else:  

                        node1=[x for x in self.JUNCTIONS+self.RESERVOIRS+self.TANKS if x.ID==line_list[1]]
                        node2=[x for x in self.JUNCTIONS+self.RESERVOIRS+self.TANKS if x.ID==line_list[2]]

                        self.PUMPS.append(PUMP(line_list[0], node1[0], node2[0], line_list[3], line_list[4]))


                elif section=="VALVES":
                    if line[0]==";": continue
                    else:  

                        node1=[x for x in self.JUNCTIONS+self.RESERVOIRS+self.TANKS if x.ID==line_list[1]]
                        node2=[x for x in self.JUNCTIONS+self.RESERVOIRS+self.TANKS if x.ID==line_list[2]]

                        self.VALVES.append(VALVE(line_list[0], node1[0], node2[0], float(line_list[3]), line_list[4], float(line_list[5]), float(line_list[6]), line_list[7]))

                elif section=="TAGS":
                    if line[0]==";": continue
                    else:  
                        self.TAGS.append(TAG(line_list[0], line_list[1], line_list[2]))


                elif section=="DEMANDS":
                    if line[0]==";": continue
                    else:  
                        self.DEMANDS.append(DEMAND(line_list[0], float(line_list[1]), line_list[2], line_list[3]))


                elif section=="STATUS":
                    if line[0]==";": continue
                    else:  
                        self.STATUS.append(STATUS(line_list[0], line_list[1]))

                elif section=="PATTERNS":
                    if line[0:3]==";ID": continue
                    if line[0]==";":
                        if len(line)>1: 
                            self.PATTERNS.append(PATTERN(line_list[0][1:]))
                        else:
                            self.PATTERNS.append(PATTERN(""))
                    else:  
                        if self.PATTERNS[-1].ID == None:
                            self.PATTERNS[-1].ID=line_list[0]
                            self.PATTERNS[-1].Multipliers.extend([float(x) for x in line_list[1:]])
                        else:
                            self.PATTERNS[-1].Multipliers.extend([float(x) for x in line_list[1:]])

                elif section=="CURVES":
                    if line[0:3]==";ID": continue
                    if line[0]==";":
                        if len(line)>1: 
                            self.CURVES.append(CURVE(line_list[0][1:]))
                        else:
                            self.CURVES.append(CURVE(""))
                    else:  
                        if self.CURVES[-1].ID == None:
                            self.CURVES[-1].ID=line_list[0]
                            self.CURVES[-1].X_Value.append(float(line_list[1]))
                            self.CURVES[-1].Y_Value.append(float(line_list[2]))
                        else:
                            self.CURVES[-1].X_Value.append(float(line_list[1]))
                            self.CURVES[-1].Y_Value.append(float(line_list[2]))

                elif section=="CONTROLS":
                    self.CONTROLS.append(line_list[0])

                elif section=="RULES":
                    if line[0:4]=="RULE":
                            self.RULES.append(RULE(line_list[0]))
                    else:  
                            self.RULES[-1].Lines.append(line_list[0])

                elif section=="ENERGY":
                        self.ENERGY.update({line_list[0]:float(line_list[1])})


                elif section=="EMITTERS":
                    if line[0]==";": continue
                    else:  
                        self.EMITTERS.append(EMITTER(line_list[0], float(line_list[1]), line_list[2]))


                elif section=="QUALITY":
                    if line[0]==";": continue
                    else:  
                        self.QUALITY.append(QUALITY(line_list[0], float(line_list[1]), line_list[2]))

                elif section=="SOURCES":
                    if line[0]==";": continue
                    else:  
                        self.SOURCES.append(SOURCE(line_list[0], line_list[1], float(line_list[2]), line_list[3], line_list[4]))


                elif section=="REACTIONS":
                    if line[0]==";": continue
                    elif line_list[0] in ["Order Bulk", "Order Tank", "Order Wall", "Global Bulk", "Global Wall", "Limiting Potential", "Roughness Correlation"]:
                        self.REACTIONS_1.update({line_list[0]:float(line_list[1])}) 
                    else:
                        self.REACTIONS.append(REACTION(line_list[0], line_list[1], float(line_list[2]), line_list[3]))                                               

                elif section=="MIXING":
                    if line[0]==";": continue
                    else:  
                        self.MIXING.append(MIXING(line_list[0], line_list[1], line_list[2]))

                elif section=="TIMES":
                        self.TIMES.update({line_list[0]:line_list[1]})               

                elif section=="REPORT":
                        self.REPORT.update({line_list[0]:line_list[1]})   

                elif section=="OPTIONS":
                        self.OPTIONS.update({line_list[0]:line_list[1]}) 

                elif section=="COORDINATES": 
                    if line[0]==";": continue
                    else:                
                        juncs = [x for x in self.JUNCTIONS if x.ID == line_list[0]]
                        if juncs:
                            juncs[0].X_Coord=float(line_list[1])
                            juncs[0].Y_Coord=float(line_list[2])

                        res = [x for x in self.RESERVOIRS if x.ID == line_list[0]]
                        if res:
                            res[0].X_Coord=float(line_list[1])
                            res[0].Y_Coord=float(line_list[2])

                        tan = [x for x in self.TANKS if x.ID == line_list[0]]
                        if tan:
                            tan[0].X_Coord=float(line_list[1])
                            tan[0].Y_Coord=float(line_list[2])


                elif section=="VERTICES":
                    #pass
                    if line[0]==";": continue
                    else:                
                        pips = [x for x in self.PIPES if x.ID == line_list[0]]
                        if pips:
                            pips[0].Vert.append((float(line_list[1]), float(line_list[2])))

                elif section=="LABELS":
                    if line[0]==";": continue
                    else:  
                        self.LABELS.append(LABEL(float(line[1:18]), float(line[18:35]), line[35:]))

                elif section=="BACKDROP":
                        self.BACKDROP.update({line_list[0]:'\t'.join(line_list[1:])})

                elif section=="END":
                    pass

        f.close()

    def writeINP(self, filenameINP):
        """ writeINP - metoda klase EPANetModel za formiranje *.INP fajla"""
        """ Ulaz ove metode predstavlja putanja i ime *.INP fajla. """

        f=open(filenameINP, 'w')

        f.write("[TITLE]")
        for x in self.TITLE:
            f.write('\n%-s' % (x))


        f.write("\n\n[JUNCTIONS]")
        f.write("\n;ID                Elev            Demand          Pattern         ")
        for x in self.JUNCTIONS:
            f.write('\n %-16s\t%-12.6f\t%-12.6f\t%-s\t%-s' % (x.ID, x.Elev, x.Demand, x.Pattern, x.Description))


        f.write("\n\n[RESERVOIRS]")
        f.write("\n;ID                  Head            Pattern         ")
        for x in self.RESERVOIRS:
            f.write('\n %-16s\t%-12.6f\t%-16s\t%-s' % (x.ID, x.Head, x.Pattern, x.Description))
        

        f.write("\n\n[TANKS]")
        f.write("\n;ID                  Elevation       InitLevel       MinLevel        MaxLevel        Diameter        MinVol          VolCurve")
        for x in self.TANKS:
            f.write('\n %-16s \t %-12.6f \t %-12.6f \t %-12.6f \t %-12.6f \t %-12.6f \t %-12.6f \t %-16s \t %-s' % (x.ID, x.Elevation, x.InitLevel, x.MinLevel, x.MaxLevel, x.Diameter, x.MinVol, x.VolCurve, x.Description))
        

        f.write("\n\n[PIPES]")
        f.write("\n;ID                  Node1               Node2               Length          Diameter        Roughness       MinorLoss       Status")
        for x in self.PIPES:
            f.write('\n %-16s \t %-16s \t %-16s \t %-12.6f \t %-12.6f \t %-12.6f \t %-12.6f \t %-6s \t %-s' % (x.ID, x.Node1.ID, x.Node2.ID, x.Length, x.Diameter, x.Roughness, x.MinorLoss, x.Status, x.Description))
        

        f.write("\n\n[PUMPS]")
        f.write("\n;ID                  Node1               Node2               Parameters")
        for x in self.PUMPS:
            f.write('\n %-16s \t %-16s \t %-16s \t %-s \t %-s' % (x.ID, x.Node1.ID, x.Node2.ID, x.Parameters, x.Description))
        

        f.write("\n\n[VALVES]")
        f.write("\n;ID                  Node1               Node2               Diameter        Type    Setting         MinorLoss   ")
        for x in self.VALVES:
            f.write('\n %-16s \t %-16s \t %-16s \t %-12.6f \t %-4s \t %-12.6f \t %-12.6f \t %-s' % (x.ID, x.Node1.ID, x.Node2.ID, x.Diameter, x.Type, x.Setting, x.MinorLoss, x.Description))
        

        f.write("\n\n[TAGS]")
        for x in self.TAGS:
            f.write('\n %-5s \t %-16s \t %-s' % (x.ElementType, x.ID, x.Description))
        

        f.write("\n\n[DEMANDS]")
        f.write("\n;Junction            Demand          Pattern             Category")
        for x in self.DEMANDS:
            f.write('\n %-16s \t %-12.6f \t %-s \t %-s \t %-s' % (x.Junction, x.Demand, x.Pattern, x.Category, x.Description))
        

        f.write("\n\n[STATUS]")
        f.write("\n;ID                  Status/Setting")
        for x in self.STATUS:
            f.write('\n %-16s \t %-s' % (x.ID, x.Status_Setting))
        

        f.write("\n\n[PATTERNS]")
        f.write("\n;ID                  Multipliers")
        for x in self.PATTERNS:
            f.write('\n;%-s' % (x.Description))
            for index, p in enumerate(x.Multipliers):
                if index % 6 == 0:
                    f.write('\n %-31s'% x.ID)
                f.write(' %12.4f'% p)


        f.write("\n\n[CURVES]")
        f.write("\n;ID                  X-Value         Y-Value")
        for x in self.CURVES:
            f.write('\n;%-s' % (x.Description))
            for index, p in enumerate(x.X_Value):
                    f.write('\n %-16s \t %-12.6f \t %-12.6f'% (x.ID , p, x.Y_Value[index]))


        f.write("\n\n[CONTROLS]")
        for x in self.CONTROLS:
            f.write('\n %-s' % (x))


        f.write("\n\n[RULES]")
        for x in self.RULES:
            f.write('\n\n %-s' % (x.Name))
            for l in x.Lines:
                f.write('\n %-s' % (l))               


        f.write("\n\n[ENERGY]")
        for key, value in self.ENERGY.iteritems():
            f.write('\n %-19s \t %-f' % (key, value))



        f.write("\n\n[EMITTERS]")
        f.write("\n;Junction            Coefficient")
        for x in self.EMITTERS:
            f.write('\n %-16s \t %-12.6f \t %-s' % (x.Junction, x.Coefficient, x.Description))
        

        f.write("\n\n[QUALITY]")
        f.write("\n;Node                InitQual")
        for x in self.QUALITY:
            f.write('\n %-16s \t %-12.6f \t %-s' % (x.Node, x.InitQual, x.Description))
        


        f.write("\n\n[SOURCES]")
        f.write("\n;Node                Type            Quality         Pattern")
        for x in self.SOURCES:
            f.write('\n %-16s \t %-16s \t %-12.6f \t %-16s \t %-s' % (x.Node, x.Type, x.Quality, x.Pattern, x.Description))
        


        f.write("\n\n[REACTIONS]")
        f.write("\n;Type        Pipe/Tank           Coefficient")
        for x in self.SOURCES:
            f.write('\n %-16s \t %-16s \t %-12.6f \t %-s' % (x.Type, x.Pipe_Tank, x.Coefficient, x.Description))


        f.write("\n\n[REACTIONS]")
        for key, value in self.REACTIONS_1.iteritems():
            f.write('\n %-19s \t %-f' % (key, value))


        f.write("\n\n[MIXING]")
        f.write("\n;Tank                Model")
        for x in self.MIXING:
            f.write('\n %-16s \t %-16s \t %-s' % (x.Tank, x.Model, x.Description))



        f.write("\n\n[TIMES]")
        for key, value in self.TIMES.iteritems():
            f.write('\n %-19s \t %-s' % (key, value))



        f.write("\n\n[REPORT]")
        for key, value in self.REPORT.iteritems():
            f.write('\n %-19s \t %-s' % (key, value))


        f.write("\n\n[OPTIONS]")
        for key, value in self.OPTIONS.iteritems():
            f.write('\n %-19s \t %-s' % (key, value))


        f.write("\n\n[COORDINATES]")
        f.write("\n;Node                X-Coord             Y-Coord")
        for x in self.JUNCTIONS:
            f.write('\n %-16s \t %-16.2f \t %-16.2f' % (x.ID, x.X_Coord, x.Y_Coord))
        for x in self.RESERVOIRS:
            f.write('\n %-16s \t %-16.2f \t %-16.2f' % (x.ID, x.X_Coord, x.Y_Coord))
        for x in self.TANKS:
            f.write('\n %-16s \t %-16.2f \t %-16.2f' % (x.ID, x.X_Coord, x.Y_Coord))


        f.write("\n\n[VERTICES]")
        f.write("\n;Link               X-Coord             Y-Coord")
        for x in self.PIPES:
            for v in x.Vert:
                f.write('\n %-16s \t %-16.2f \t %-16.2f' % (x.ID, v[0], v[1]))

        
        f.write("\n\n[LABELS]")
        f.write("\n;X-Coord           Y-Coord          Label & Anchor Node")
        for x in self.LABELS:
            f.write('\n %-17.2f%-17.2f%-s' % (x.X_Coord, x.Y_Coord, x.Label_And_Anchor_Node))


        f.write("\n\n[BACKDROP]")
        for key, value in self.BACKDROP.iteritems():
            f.write('\n %-s \t %-s' % (key, value))


        f.write("\n\n[END]")
        f.close

    
    def pushData(self, SERVER, DEFAULT_DATABASE, UID, PWD, DATABASE_NAME):
        """ pushData - metoda klase EPANetModel za slanje podataka iz objekta u MSSQLServer bazu podataka."""
        """ Ulaz ove metode su:"""
        """ """
        """ SERVER - ime servera"""
        """ DEFAULT_DATABASE - postojeca baza podataka"""
        """ UID - user"""
        """ PWD - loznka"""
        """ DATABASE_NAME - naziv baze podataka u kojoj ce biti cuvani podaci"""
        """ """
        """ Podaci se upisuju u sledece tabele:"""        
        """ EPA_TITLE - kolone: DBID (ID polja u bazi), Line """
        """ EPA_JUNCTIONS - kolone: DBID (ID polja u bazi), ID , Elev , Demand , Pattern , Description , X_Coord , Y_Coord """
        """ EPA_RESERVOIRS - kolone: DBID (ID polja u bazi), ID , Head , Pattern , Description , X_Coord , Y_Coord """
        """ EPA_TANKS - kolone: DBID (ID polja u bazi), ID , Elevation , InitLevel , MinLevel , MaxLevel , Diameter , MinVol , VolCurve , Description , X_Coord , Y_Coord """
        """ EPA_PIPES - kolone: DBID (ID polja u bazi), ID , Node1 , Node2 , Length , Diameter , Roughness , MinorLoss , Status , Description , Vert VARCHARmax"""
        """ EPA_PUMPS - kolone: DBID (ID polja u bazi), ID , Node1 , Node2 , Parameters , Description """
        """ EPA_VALVES - kolone: DBID (ID polja u bazi), ID , Node1 , Node2 , Diameter , Type , Setting , MinorLoss , Description """
        """ EPA_TAGS - kolone: DBID (ID polja u bazi), ElementType , ID , Description """
        """ EPA_DEMANDS - kolone: DBID (ID polja u bazi), Junction , Demand , Pattern , Category , Description """
        """ EPA_STATUS - kolone: DBID (ID polja u bazi), ID , Status_Setting """
        """ EPA_PATTERNS - kolone: DBID (ID polja u bazi), ID , Position INT, Multipliers , Description """
        """ EPA_CURVES - kolone: DBID (ID polja u bazi), ID , Position INT, X_Value , Y_Value , Description """
        """ EPA_CONTROLS - kolone: DBID (ID polja u bazi), Line """
        """ EPA_RULES - kolone: DBID (ID polja u bazi), Name , Position INT, Lines """
        """ EPA_ENERGY - kolone: DBID (ID polja u bazi), Global_Efficiency , Global_Price , Demand_Charge """
        """ EPA_EMITTERS - kolone: DBID (ID polja u bazi), Junction , Coefficient , Description """
        """ EPA_QUALITY - kolone: DBID (ID polja u bazi), Node , InitQual , Description """
        """ EPA_SOURCES - kolone: DBID (ID polja u bazi), Node , Type , Quality , Pattern , Description """
        """ EPA_REACTIONS - kolone: DBID (ID polja u bazi), Type , Pipe_Tank , Coefficient , Description """
        """ EPA_REACTIONS_1 - kolone: DBID (ID polja u bazi), Order_Bulk , Order_Tank , Order_Wall , Global_Bulk , Global_Wall , Limiting_Potential , Roughness_Correlation """
        """ EPA_MIXING - kolone: DBID (ID polja u bazi), Tank , Model , Description """
        """ EPA_TIMES - kolone: DBID (ID polja u bazi), Duration , Hydraulic_Timestep , Quality_Timestep , Pattern_Timestep , Pattern_Start , Report_Timestep , Report_Start , Start_ClockTime , Statistic """
        """ EPA_REPORT - kolone: DBID (ID polja u bazi), Status , Summary , Page , Node , Link """
        """ EPA_OPTIONS - kolone: DBID (ID polja u bazi), Units , Headloss , Specific_Gravity , Viscosity , Trials , Accuracy , CHECKFREQ , MAXCHECK , DAMPLIMIT , Unbalanced , Pattern , Demand_Multiplier , Emitter_Exponent , Quality , Diffusivity , Tolerance """
        """ EPA_LABELS - kolone: DBID (ID polja u bazi), X_Coord , Y_Coord , Label_And_Anchor_Node """
        """ EPA_BACKDROP - kolone: DBID (ID polja u bazi), DIMENSIONS , UNITS , BACKDROP_FILE , OFFSET """
        """ EPA_META - kolone: DBID (ID polja u bazi), Version , Date , SimulationName , Description """

        #Konekcija sa postojecom bazom podataka (DEFAULT_DATABASE) zbog pravljenja nove baze
        conection_string=r'DRIVER={SQL Server Native Client 11.0};;SERVER=' + SERVER + ';DATABASE=' + DEFAULT_DATABASE + ';UID=' + UID + ';PWD=' + PWD
        conn = pyodbc.connect(conection_string, autocommit=True)
        cursor = conn.cursor()

        #Formiranje baze podataka
        create_db_sql = 'CREATE DATABASE ' +  DATABASE_NAME
        try:
            cursor.execute(create_db_sql)
        except pyodbc.ProgrammingError:   # Izbrisi vec postojecu bazu sa istim imenom i napravi novu
            drop_db_sql = 'DROP DATABASE ' + db_name
            cursor.execute(drop_db_sql)
            cursor.execute(create_db_sql)
            cursor.commit() # Komituj bazu

        conn.close()

        #Konekcija sa novoformiranom bazom podataka (DATABASE_NAME)
        conection_string=r'DRIVER={SQL Server Native Client 11.0};;SERVER=' + SERVER + ';DATABASE=' + DATABASE_NAME + ';UID=' + UID + ';PWD=' + PWD
        conn = pyodbc.connect(conection_string)
        cursor = conn.cursor()


        #Create and populate table EPA_TITLE
        sql_command = """CREATE TABLE EPA_TITLE (DBID INT IDENTITY(1,1) NOT NULL, Line NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit() 

        rows=[]
        for x in self.TITLE:
            rows.append([x])
        
        if rows:
            sql_command = """INSERT INTO EPA_TITLE VALUES (?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()   


        #Create and populate table EPA_JUNCTIONS
        sql_command = """CREATE TABLE EPA_JUNCTIONS (DBID INT IDENTITY(1,1) NOT NULL, ID NVARCHAR(256), Elev FLOAT, Demand FLOAT, Pattern NVARCHAR(256), Description NVARCHAR(256), X_Coord FLOAT, Y_Coord FLOAT)"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[]
        for x in self.JUNCTIONS:
            rows.append([x.ID, x.Elev, x.Demand, x.Pattern, x.Description, x.X_Coord, x.Y_Coord])
        
        if rows:
            sql_command = """INSERT INTO EPA_JUNCTIONS VALUES (?, ?, ?, ?, ?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()   


        #Create and populate table EPA_RESERVOIRS
        sql_command = """CREATE TABLE EPA_RESERVOIRS (DBID INT IDENTITY(1,1) NOT NULL, ID NVARCHAR(256), Head FLOAT, Pattern NVARCHAR(256), Description NVARCHAR(256), X_Coord FLOAT, Y_Coord FLOAT)"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[]
        for x in self.RESERVOIRS:
            rows.append([x.ID, x.Head, x.Pattern, x.Description, x.X_Coord, x.Y_Coord])
        
        if rows:
            sql_command = """INSERT INTO EPA_RESERVOIRS VALUES (?, ?, ?, ?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()   


        #Create and populate table EPA_TANKS
        sql_command = """CREATE TABLE EPA_TANKS (DBID INT IDENTITY(1,1) NOT NULL, ID NVARCHAR(256), Elevation FLOAT, InitLevel FLOAT, MinLevel FLOAT, MaxLevel FLOAT, Diameter FLOAT, MinVol FLOAT, VolCurve NVARCHAR(256), Description NVARCHAR(256), X_Coord FLOAT, Y_Coord FLOAT)"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[]
        for x in self.TANKS:
            rows.append([x.ID, x.Elevation, x.InitLevel, x.MinLevel, x.MaxLevel, x.Diameter, x.MinVol, x.VolCurve, x.Description, x.X_Coord, x.Y_Coord])
        
        if rows:
            sql_command = """INSERT INTO EPA_TANKS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()   
     
        #Create and populate table EPA_PIPES
        sql_command = """CREATE TABLE EPA_PIPES (DBID INT IDENTITY(1,1) NOT NULL, ID NVARCHAR(256), Node1 NVARCHAR(256), Node2 NVARCHAR(256), Length FLOAT, Diameter FLOAT, Roughness FLOAT, MinorLoss FLOAT, Status NVARCHAR(256), Description NVARCHAR(256), Vert VARCHAR(max))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[]
        for x in self.PIPES:
            rows.append([x.ID, x.Node1.ID, x.Node2.ID, x.Length, x.Diameter, x.Roughness, x.MinorLoss, x.Status, x.Description, str(x.Vert)])
        
        if rows:
            sql_command = """INSERT INTO EPA_PIPES VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()   

        #Create and populate table EPA_PUMPS
        sql_command = """CREATE TABLE EPA_PUMPS (DBID INT IDENTITY(1,1) NOT NULL, ID NVARCHAR(256), Node1 NVARCHAR(256), Node2 NVARCHAR(256), Parameters NVARCHAR(256), Description NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[]
        for x in self.PUMPS:
            rows.append([x.ID, x.Node1.ID, x.Node2.ID, x.Parameters, x.Description])
        
        if rows:
            sql_command = """INSERT INTO EPA_PUMPS VALUES (?, ?, ?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()   


        #Create and populate table EPA_VALVES
        sql_command = """CREATE TABLE EPA_VALVES (DBID INT IDENTITY(1,1) NOT NULL, ID NVARCHAR(256), Node1 NVARCHAR(256), Node2 NVARCHAR(256), Diameter FLOAT, Type NVARCHAR(256), Setting FLOAT, MinorLoss FLOAT, Description NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[]
        for x in self.VALVES:
            rows.append([x.ID, x.Node1.ID, x.Node2.ID, x.Diameter, x.Type, x.Setting, x.MinorLoss, x.Description])
        
        if rows:
            sql_command = """INSERT INTO EPA_VALVES VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()   


        # #Create and populate table EPA_TAGS
        sql_command = """CREATE TABLE EPA_TAGS (DBID INT IDENTITY(1,1) NOT NULL, ElementType NVARCHAR(256), ID NVARCHAR(256), Description NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[]
        for x in self.TAGS:
            rows.append([x.ElementType, x.ID, x.Description])
        
        if rows:
            sql_command = """INSERT INTO EPA_TAGS VALUES (?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()   


        # #Create and populate table EPA_DEMANDS
        sql_command = """CREATE TABLE EPA_DEMANDS (DBID INT IDENTITY(1,1) NOT NULL, Junction NVARCHAR(256), Demand FLOAT, Pattern NVARCHAR(256), Category NVARCHAR(256), Description NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[]
        for x in self.DEMANDS:
            rows.append([x.Junction, x.Demand, x.Pattern, x.Category, x.Description])
        
        if rows:
            sql_command = """INSERT INTO EPA_DEMANDS VALUES (?, ?, ?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()   


        # #Create and populate table EPA_STATUS
        sql_command = """CREATE TABLE EPA_STATUS (DBID INT IDENTITY(1,1) NOT NULL, ID NVARCHAR(256), Status_Setting NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[]
        for x in self.STATUS:
            rows.append([x.ID, x.Status_Setting])
        
        if rows:
            sql_command = """INSERT INTO EPA_STATUS VALUES (?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit() 


        # #Create and populate table EPA_PATTERNS
        sql_command = """CREATE TABLE EPA_PATTERNS (DBID INT IDENTITY(1,1) NOT NULL, ID NVARCHAR(256), Position INT, Multipliers FLOAT, Description NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[]
        for x in self.PATTERNS:         
            for index, m in enumerate(x.Multipliers):
                rows.append([x.ID, index, m, x.Description])
        
        if rows:
            sql_command = """INSERT INTO EPA_PATTERNS VALUES (?, ?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()   



        # #Create and populate table EPA_CURVES
        sql_command = """CREATE TABLE EPA_CURVES (DBID INT IDENTITY(1,1) NOT NULL, ID NVARCHAR(256), Position INT, X_Value FLOAT, Y_Value FLOAT, Description NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[]
        for x in self.CURVES:         
            for index, x_value in enumerate(x.X_Value):
                rows.append([x.ID, index, x_value, x.Y_Value[index], x.Description])
        
        if rows:
            sql_command = """INSERT INTO EPA_CURVES VALUES (?, ?, ?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()   


        # #Create and populate table EPA_CONTROLS
        sql_command = """CREATE TABLE EPA_CONTROLS (DBID INT IDENTITY(1,1) NOT NULL, Line NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit() 

        rows=[]
        for x in self.CONTROLS:
            rows.append([x])
        
        if rows:
            sql_command = """INSERT INTO EPA_CONTROLS VALUES (?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()   


        # #Create and populate table EPA_RULES
        sql_command = """CREATE TABLE EPA_RULES (DBID INT IDENTITY(1,1) NOT NULL, Name NVARCHAR(256), Position INT, Lines NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[]
        for x in self.RULES:         
            for index, l in enumerate(x.Lines):
                rows.append([x.Name, index, l])
        
        if rows:
            sql_command = """INSERT INTO EPA_RULES VALUES (?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()   

        # #Create and populate table EPA_ENERGY
        sql_command = """CREATE TABLE EPA_ENERGY (DBID INT IDENTITY(1,1) NOT NULL, Global_Efficiency FLOAT, Global_Price FLOAT, Demand_Charge FLOAT)"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[[self.ENERGY["Global Efficiency"], self.ENERGY["Global Price"], self.ENERGY["Demand Charge"]]]

        if rows:
            sql_command = """INSERT INTO EPA_ENERGY VALUES (?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()   


        # #Create and populate table EPA_EMITTERS
        sql_command = """CREATE TABLE EPA_EMITTERS (DBID INT IDENTITY(1,1) NOT NULL, Junction NVARCHAR(256), Coefficient FLOAT, Description NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[]
        for x in self.EMITTERS:
            rows.append([x.Junction, x.Coefficient, x.Description])
        
        if rows:
            sql_command = """INSERT INTO EPA_EMITTERS VALUES (?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit() 

        # #Create and populate table EPA_QUALITY
        sql_command = """CREATE TABLE EPA_QUALITY (DBID INT IDENTITY(1,1) NOT NULL, Node NVARCHAR(256), InitQual FLOAT, Description NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[]
        for x in self.QUALITY:
            rows.append([x.Node, x.InitQual, x.Description])
        
        if rows:
            sql_command = """INSERT INTO EPA_QUALITY VALUES (?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit() 


        # #Create and populate table EPA_SOURCES
        sql_command = """CREATE TABLE EPA_SOURCES (DBID INT IDENTITY(1,1) NOT NULL, Node NVARCHAR(256), Type NVARCHAR(256), Quality FLOAT, Pattern NVARCHAR(256), Description NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[]
        for x in self.SOURCES:
            rows.append([x.Node, x.Type, x.Quality, x.Pattern, x.Description])
        
        if rows:
            sql_command = """INSERT INTO EPA_SOURCES VALUES (?, ?, ?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit() 


        # #Create and populate table EPA_REACTIONS
        sql_command = """CREATE TABLE EPA_REACTIONS (DBID INT IDENTITY(1,1) NOT NULL, Type NVARCHAR(256), Pipe_Tank NVARCHAR(256), Coefficient FLOAT, Description NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[]
        for x in self.REACTIONS:
            rows.append([x.Type, x.Pipe_Tank, x.Coefficient, x.Description])
        
        if rows:
            sql_command = """INSERT INTO EPA_REACTIONS VALUES (?, ?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit() 

        # #Create and populate table EPA_REACTIONS_1
        sql_command = """CREATE TABLE EPA_REACTIONS_1 (DBID INT IDENTITY(1,1) NOT NULL, Order_Bulk FLOAT, Order_Tank FLOAT, Order_Wall FLOAT, Global_Bulk FLOAT, Global_Wall FLOAT, Limiting_Potential FLOAT, Roughness_Correlation FLOAT)"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[[self.REACTIONS_1["Order Bulk"], self.REACTIONS_1["Order Tank"], self.REACTIONS_1["Order Wall"], self.REACTIONS_1["Global Bulk"], self.REACTIONS_1["Global Wall"], self.REACTIONS_1["Limiting Potential"], self.REACTIONS_1["Roughness Correlation"]]]

        if rows:
            sql_command = """INSERT INTO EPA_REACTIONS_1 VALUES (?, ?, ?, ?, ?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()  


        # #Create and populate table EPA_MIXING
        sql_command = """CREATE TABLE EPA_MIXING (DBID INT IDENTITY(1,1) NOT NULL, Tank NVARCHAR(256), Model NVARCHAR(256), Description NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[]
        for x in self.MIXING:
            rows.append([x.Tank, x.Model, x.Description])
        
        if rows:
            sql_command = """INSERT INTO EPA_MIXING VALUES (?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit() 

        # #Create and populate table EPA_TIMES
        sql_command = """CREATE TABLE EPA_TIMES (DBID INT IDENTITY(1,1) NOT NULL, Duration NVARCHAR(256), Hydraulic_Timestep NVARCHAR(256), Quality_Timestep NVARCHAR(256), Pattern_Timestep NVARCHAR(256), Pattern_Start NVARCHAR(256), Report_Timestep NVARCHAR(256), Report_Start NVARCHAR(256), Start_ClockTime NVARCHAR(256), Statistic NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[[self.TIMES["Duration"], self.TIMES["Hydraulic Timestep"], self.TIMES["Quality Timestep"], self.TIMES["Pattern Timestep"], self.TIMES["Pattern Start"], self.TIMES["Report Timestep"], self.TIMES["Report Start"], self.TIMES["Start ClockTime"], self.TIMES["Statistic"]]]

        if rows:
            sql_command = """INSERT INTO EPA_TIMES VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()  

        # #Create and populate table EPA_REPORT
        sql_command = """CREATE TABLE EPA_REPORT (DBID INT IDENTITY(1,1) NOT NULL, Status NVARCHAR(256), Summary NVARCHAR(256), Page NVARCHAR(256), Node NVARCHAR(256), Link NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[[self.REPORT["Status"], self.REPORT["Summary"], self.REPORT["Page"], self.REPORT["Node"], self.REPORT["Link"]]]

        if rows:
            sql_command = """INSERT INTO EPA_REPORT VALUES (?, ?, ?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()  

        # #Create and populate table EPA_OPTIONS
        sql_command = """CREATE TABLE EPA_OPTIONS (DBID INT IDENTITY(1,1) NOT NULL, Units NVARCHAR(256), Headloss NVARCHAR(256), Specific_Gravity FLOAT, Viscosity FLOAT, Trials FLOAT, Accuracy FLOAT, CHECKFREQ FLOAT, MAXCHECK FLOAT, DAMPLIMIT FLOAT, Unbalanced NVARCHAR(256), Pattern NVARCHAR(256), Demand_Multiplier FLOAT, Emitter_Exponent FLOAT, Quality NVARCHAR(256), Diffusivity FLOAT, Tolerance FLOAT)"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[[self.OPTIONS["Units"], self.OPTIONS["Headloss"], self.OPTIONS["Specific Gravity"], self.OPTIONS["Viscosity"], self.OPTIONS["Trials"], self.OPTIONS["Accuracy"], self.OPTIONS["CHECKFREQ"], self.OPTIONS["MAXCHECK"], self.OPTIONS["DAMPLIMIT"],self.OPTIONS["Unbalanced"], self.OPTIONS["Pattern"], self.OPTIONS["Demand Multiplier"], self.OPTIONS["Emitter Exponent"], self.OPTIONS["Quality"], self.OPTIONS["Diffusivity"], self.OPTIONS["Tolerance"]]]

        if rows:
            sql_command = """INSERT INTO EPA_OPTIONS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()  


        # #Create and populate table EPA_LABELS
        sql_command = """CREATE TABLE EPA_LABELS (DBID INT IDENTITY(1,1) NOT NULL, X_Coord FLOAT, Y_Coord FLOAT, Label_And_Anchor_Node NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[]
        for x in self.LABELS:
            rows.append([x.X_Coord, x.Y_Coord, x.Label_And_Anchor_Node])
        
        if rows:
            sql_command = """INSERT INTO EPA_LABELS VALUES (?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit() 

        # #Create and populate table EPA_BACKDROP
        sql_command = """CREATE TABLE EPA_BACKDROP (DBID INT IDENTITY(1,1) NOT NULL, DIMENSIONS NVARCHAR(256), UNITS NVARCHAR(256), BACKDROP_FILE NVARCHAR(256), OFFSET NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[[self.BACKDROP["DIMENSIONS"], self.BACKDROP["UNITS"], self.BACKDROP["FILE"], self.BACKDROP["OFFSET"]]]
        if rows:
            sql_command = """INSERT INTO EPA_BACKDROP VALUES (?, ?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()  

        # #Create and populate table EPA_META
        sql_command = """CREATE TABLE EPA_META (DBID INT IDENTITY(1,1) NOT NULL, Version NVARCHAR(256), VersionDate NVARCHAR(256), SimulationName NVARCHAR(256), Description NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[[self.META["Version"], self.META["VersionDate"], self.META["SimulationName"], self.META["Description"]]]

        if rows:
            sql_command = """INSERT INTO EPA_META VALUES (?, ?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()   

        conn.close()


    def retrieveData(self, SERVER, UID, PWD, DATABASE_NAME):
        """ retrieveData - metoda klase EPANetModel za ucitavanje podataka iz MSSQLServer baze podataka u polja objekta klase."""
        """ Ulaz ove metode su:"""
        """ """
        """ SERVER - ime servera"""
        """ UID - user"""
        """ PWD - loznka"""
        """ DATABASE_NAME - naziv baze podataka u kojoj se cuvaju podaci"""
        """ """
        conection_string=r'DRIVER={SQL Server Native Client 11.0};;SERVER=' + SERVER + ';DATABASE=' + DATABASE_NAME + ';UID=' + UID + ';PWD=' + PWD
        conn = pyodbc.connect(conection_string)
        cursor = conn.cursor()

        # Retrieve from table EPA_TITLE
        sql_command = """SELECT Line FROM EPA_TITLE"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.TITLE.append(row[0])

        # Retrieve from table EPA_JUNCTIONS
        sql_command = """SELECT ID, Elev, Demand, Pattern, Description, X_Coord, Y_Coord FROM EPA_JUNCTIONS"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.JUNCTIONS.append(JUNCTION(row[0], float(row[1]), float(row[2]), row[3], row[4]))
                self.JUNCTIONS[-1].X_Coord=float(row[5])
                self.JUNCTIONS[-1].Y_Coord=float(row[6])

        # Retrieve from table EPA_RESERVOIRS
        sql_command = """SELECT ID, Head, Pattern, Description, X_Coord, Y_Coord FROM EPA_RESERVOIRS"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.RESERVOIRS.append(RESERVOIR(row[0], float(row[1]), row[2], row[3]))
                self.RESERVOIRS[-1].X_Coord=float(row[4])
                self.RESERVOIRS[-1].Y_Coord=float(row[5])

        # Retrieve from table EPA_TANKS
        sql_command = """SELECT ID, Elevation, InitLevel, MinLevel, MaxLevel, Diameter, MinVol, VolCurve, Description, X_Coord, Y_Coord FROM EPA_TANKS"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.TANKS.append(TANK(row[0], float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), row[7], row[8]))
                self.TANKS[-1].X_Coord=float(row[9])
                self.TANKS[-1].Y_Coord=float(row[10])

        # Retrieve from table EPA_PIPES
        sql_command = """SELECT ID, Node1, Node2, Length, Diameter, Roughness, MinorLoss, Status, Description, Vert FROM EPA_PIPES"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:

                node1=[x for x in self.JUNCTIONS+self.RESERVOIRS+self.TANKS if x.ID==row[1]]
                node2=[x for x in self.JUNCTIONS+self.RESERVOIRS+self.TANKS if x.ID==row[2]]
                self.PIPES.append(PIPE(row[0], node1[0], node2[0], float(row[3]), float(row[4]), float(row[5]), float(row[6]), row[7], row[8]))
                self.PIPES[-1].Vert=eval(row[9])

        # Retrieve from table EPA_PUMPS
        sql_command = """SELECT ID, Node1, Node2, Parameters, Description FROM EPA_PUMPS"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:

                node1=[x for x in self.JUNCTIONS+self.RESERVOIRS+self.TANKS if x.ID==row[1]]
                node2=[x for x in self.JUNCTIONS+self.RESERVOIRS+self.TANKS if x.ID==row[2]]
                self.PUMPS.append(PUMP(row[0], node1[0], node2[0], row[3], row[4]))

        # Retrieve from table EPA_VALVES
        sql_command = """SELECT ID, Node1, Node2, Diameter, Type, Setting, MinorLoss, Description FROM EPA_VALVES"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:

                node1=[x for x in self.JUNCTIONS+self.RESERVOIRS+self.TANKS if x.ID==row[1]]
                node2=[x for x in self.JUNCTIONS+self.RESERVOIRS+self.TANKS if x.ID==row[2]]
                self.VALVES.append(VALVE(row[0], node1[0], node2[0], float(row[3]), row[4], float(row[5]), float(row[6]), row[7]))


        # Retrieve from table EPA_TAGS
        sql_command = """SELECT ElementType, ID, Description FROM EPA_TAGS"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.TAGS.append(TAG(row[0], row[1], row[2]))

        # Retrieve from table EPA_DEMANDS
        sql_command = """SELECT Junction, Demand, Pattern, Category, Description FROM EPA_DEMANDS"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.DEMANDS.append(DEMAND(row[0], float(row[1]), row[2], row[3], row[4]))

        # Retrieve from table EPA_STATUS
        sql_command = """SELECT ID, Status_Setting FROM EPA_STATUS"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.STATUS.append(STATUS(row[0], row[1]))

        # Retrieve from table EPA_PATTERNS
        sql_command = """SELECT ID, Position, Multipliers, Description FROM EPA_PATTERNS"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                if row[1]==0:
                    self.PATTERNS.append(PATTERN(row[3]))
                    self.PATTERNS[-1].ID=row[0]
                    self.PATTERNS[-1].Multipliers.append(float(row[2]))
                else:
                    self.PATTERNS[-1].Multipliers.append(float(row[2]))                    


        # Retrieve from table EPA_CURVES
        sql_command = """SELECT ID, Position, X_Value, Y_Value, Description FROM EPA_CURVES"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                if row[1]==0:
                    self.CURVES.append(CURVE(row[4]))
                    self.CURVES[-1].ID=row[0]
                    self.CURVES[-1].X_Value.append(float(row[2]))
                    self.CURVES[-1].Y_Value.append(float(row[3]))                        
                else:
                    self.CURVES[-1].X_Value.append(float(row[2]))
                    self.CURVES[-1].Y_Value.append(float(row[3]))    

        # Retrieve from table EPA_CONTROLS
        sql_command = """SELECT Line FROM EPA_CONTROLS"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.CONTROLS.append(row[0])

        # Retrieve from table EPA_RULES
        sql_command = """SELECT Name, Position, Lines FROM EPA_RULES"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                if row[1]==0:
                    self.RULES.append(RULE(row[0]))
                    self.RULES[-1].Lines.append(row[2])
                else:
                    self.RULES[-1].Lines.append(row[2])


        # Retrieve from table EPA_ENERGY
        sql_command = """SELECT Global_Efficiency, Global_Price, Demand_Charge FROM EPA_ENERGY"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.ENERGY["Global Efficiency"]=row[0]
                self.ENERGY["Global Price"]=row[1]
                self.ENERGY["Demand Charge"]=row[2]


        # Retrieve from table EPA_EMITTERS
        sql_command = """SELECT Junction, Coefficient, Description FROM EPA_EMITTERS"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.EMITTERS.append(EMITTER(row[0], float(row[1]), row[2]))

        # Retrieve from table EPA_QUALITY
        sql_command = """SELECT Node, InitQual, Description FROM EPA_QUALITY"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.QUALITY.append(QUALITY(row[0], float(row[1]), row[2]))

        # Retrieve from table EPA_SOURCES
        sql_command = """SELECT Node, Type, Quality, Pattern, Description FROM EPA_SOURCES"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.SOURCES.append(SOURCE(row[0], row[1], float(row[2]), row[3], row[4]))

        # Retrieve from table EPA_REACTIONS
        sql_command = """SELECT Type, Pipe_Tank, Coefficient, Description FROM EPA_REACTIONS"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.REACTIONS.append(REACTION(row[0], row[1], float(row[2]), row[3]))

        # Retrieve from table EPA_REACTIONS_1
        sql_command = """SELECT Order_Bulk, Order_Tank, Order_Wall, Global_Bulk, Global_Wall, Limiting_Potential, Roughness_Correlation FROM EPA_REACTIONS_1"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.REACTIONS_1["Order Bulk"]=row[0]
                self.REACTIONS_1["Order Tank"]=row[1]
                self.REACTIONS_1["Order Wall"]=row[2]
                self.REACTIONS_1["Global Bulk"]=row[3]
                self.REACTIONS_1["Global Wall"]=row[4]
                self.REACTIONS_1["Limiting Potential"]=row[5]
                self.REACTIONS_1["Roughness Correlation"]=row[6]

        # Retrieve from table EPA_MIXING
        sql_command = """SELECT Tank, Model, Description FROM EPA_MIXING"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.MIXING.append(MIXING(row[0], row[1], row[2]))

        # Retrieve from table EPA_TIMES
        sql_command = """SELECT Duration, Hydraulic_Timestep, Quality_Timestep, Pattern_Timestep, Pattern_Start, Report_Timestep, Report_Start, Start_ClockTime, Statistic FROM EPA_TIMES"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.TIMES["Duration"]=row[0]
                self.TIMES["Hydraulic Timestep"]=row[1]
                self.TIMES["Quality Timestep"]=row[2]
                self.TIMES["Pattern Timestep"]=row[3]
                self.TIMES["Pattern Start"]=row[4]
                self.TIMES["Report Timestep"]=row[5]
                self.TIMES["Report Start"]=row[6]
                self.TIMES["Start ClockTime"]=row[7]
                self.TIMES["Statistic"]=row[8]

        # Retrieve from table EPA_REPORT
        sql_command = """SELECT Status, Summary, Page,  Node, Link FROM EPA_REPORT"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.REPORT["Status"]=row[0]
                self.REPORT["Summary"]=row[1]
                self.REPORT["Page"]=row[2]
                self.REPORT["Node"]=row[3]
                self.REPORT["Link"]=row[4]


        # Retrieve from table EPA_OPTIONS
        sql_command = """SELECT Units, Headloss, Specific_Gravity, Viscosity, Trials, Accuracy, CHECKFREQ, MAXCHECK, DAMPLIMIT, Unbalanced, Pattern, Demand_Multiplier, Emitter_Exponent, Quality, Diffusivity, Tolerance FROM EPA_OPTIONS"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.OPTIONS["Units"]=row[0]
                self.OPTIONS["Headloss"]=row[1]
                self.OPTIONS["Specific Gravity"]=row[2]
                self.OPTIONS["Viscosity"]=row[3]
                self.OPTIONS["Trials"]=row[4]
                self.OPTIONS["Accuracy"]=row[5]
                self.OPTIONS["CHECKFREQ"]=row[6]
                self.OPTIONS["MAXCHECK"]=row[7]
                self.OPTIONS["DAMPLIMIT"]=row[8]
                self.OPTIONS["Unbalanced"]=row[9]
                self.OPTIONS["Pattern"]=row[10]
                self.OPTIONS["Demand Multiplier"]=row[11]
                self.OPTIONS["Emitter Exponent"]=row[12]
                self.OPTIONS["Quality"]=row[13]
                self.OPTIONS["Diffusivity"]=row[14]
                self.OPTIONS["Tolerance"]=row[15]

        # Retrieve from table EPA_LABELS
        sql_command = """SELECT X_Coord, Y_Coord, Label_And_Anchor_Node FROM EPA_LABELS"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.LABELS.append(LABEL(float(row[0]), float(row[1]), row[2]))

        # Retrieve from table EPA_BACKDROP
        sql_command = """SELECT DIMENSIONS, UNITS, BACKDROP_FILE, OFFSET FROM EPA_BACKDROP"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.BACKDROP["DIMENSIONS"]=row[0]
                self.BACKDROP["UNITS"]=row[1]
                self.BACKDROP["FILE"]=row[2]
                self.BACKDROP["OFFSET"]=row[3]

        # Retrieve from table EPA_META
        sql_command = """SELECT Version, VersionDate, SimulationName, Description FROM EPA_META"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.META["Version"]=row[0]
                self.META["VersionDate"]=row[1]
                self.META["SimulationName"]=row[2]
                self.META["Description"]=row[3]


        conn.close()

    def readRPT(self, filenameRPT):
        """ readRPT - metoda klase EPANetModel za ucitavanje podataka iz fajla sa rezultatima simulacije u polja objekta klase."""
        """ Ulaz ove metode je:"""
        """ """
        """ filenameRPT - ime fajla sa rezultatima simulacije"""
        """ """              
        sections=["Node", "Link"]

        section=""
        datatime=""

        f=open(filenameRPT, 'r')
        for line in f:
            line_list=line.split()

            if line_list == []: continue
            else:             
                if line_list[0].strip() in sections and line_list[1].strip()=='Results':
                    section=line_list[0].strip()
                    datatime=line_list[3]                      
                    continue

                line_list=[x.strip() for x in line.split()]              
                if section=="Node":
                    if line_list[0][0:4]=="----" or line_list[0]=="Demand" or line_list[0]=="Node": continue  
                    if len(line_list)==5:   
                        self.RES_NODES.append(RES_NODE(line_list[0], datatime, float(line_list[1]), float(line_list[2]), float(line_list[3]), line_list[4]))
                    else:
                        self.RES_NODES.append(RES_NODE(line_list[0], datatime, float(line_list[1]), float(line_list[2]), float(line_list[3])))

                elif section=="Link":   
                    if line_list[0][0:4]=="----" or line_list[0]=="Flow" or line_list[0]=="Link": continue  
                    if len(line_list)==5:     
                        self.RES_LINKS.append(RES_LINK(line_list[0], datatime, float(line_list[1]), float(line_list[2]), float(line_list[3]), line_list[4]))
                    else:
                        self.RES_LINKS.append(RES_LINK(line_list[0], datatime, float(line_list[1]), float(line_list[2]), float(line_list[3])))


    def pushRPT(self, SERVER, UID, PWD, DATABASE_NAME):
        """ pushRPT - metoda klase EPANetModel za slanje rezultata simulacije u MSSQLServer bazu podataka."""
        """ Neophodno je da baza vec postoji. Najbolje je da baza bude sa podacima na osnovu kojih je formiran *.INP fajl za simulaciju."""
        """ Ulaz ove metode su:"""
        """ """
        """ SERVER - ime servera"""
        """ UID - user"""
        """ PWD - loznka"""
        """ DATABASE_NAME - naziv baze podataka u kojoj ce biti cuvani podaci"""
        """ """
        """ Podaci se upisuju u sledece tabele:"""        
        """ EPA_RES_NODES - kolone: DBID (ID polja u bazi), ID, DataTime, Demand, Head, Pressure, Chlorine, Node_Type """
        """ EPA_RES_LINKS - kolone: DBID (ID polja u bazi), ID, DataTime, Flow, Velocity, Headloss, Link_Type """


        conection_string=r'DRIVER={SQL Server Native Client 11.0};;SERVER=' + SERVER + ';DATABASE=' + DATABASE_NAME + ';UID=' + UID + ';PWD=' + PWD
        conn = pyodbc.connect(conection_string)
        cursor = conn.cursor()


        #Create and populate table EPA_RES_NODES
        sql_command = """CREATE TABLE EPA_RES_NODES (DBID INT IDENTITY(1,1) NOT NULL, ID NVARCHAR(256), DataTime NVARCHAR(256), Demand FLOAT, Head FLOAT, Pressure FLOAT, Chlorine FLOAT, Node_Type NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[]
        for x in self.RES_NODES:
            rows.append([x.ID, x.DataTime, x.Demand, x.Head, x.Pressure, x.Chlorine, x.Node_Type])
        
        if rows:
            sql_command = """INSERT INTO EPA_RES_NODES VALUES (?, ?, ?, ?, ?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()   


        #Create and populate table EPA_RES_LINKS
        sql_command = """CREATE TABLE EPA_RES_LINKS (DBID INT IDENTITY(1,1) NOT NULL, ID NVARCHAR(256), DataTime NVARCHAR(256), Flow FLOAT, Velocity FLOAT, Headloss FLOAT, Link_Type NVARCHAR(256))"""
        cursor.execute(sql_command)
        conn.commit()   
        
        rows=[]
        for x in self.RES_LINKS:
            rows.append([x.ID, x.DataTime, x.Flow, x.Velocity, x.Headloss, x.Link_Type])
        
        if rows:
            sql_command = """INSERT INTO EPA_RES_LINKS VALUES (?, ?, ?, ?, ?, ?)"""
            cursor.executemany(sql_command,rows)
            conn.commit()   

        conn.close()


    def retrieveRPT(self, SERVER, UID, PWD, DATABASE_NAME):
        """ retrieveRPT - metoda klase EPANetModel za ucitavanje rezultata simulacije iz MSSQLServer baze podataka u polja objekta klase."""
        """ Ulaz ove metode su:"""
        """ """
        """ SERVER - ime servera"""
        """ UID - user"""
        """ PWD - loznka"""
        """ DATABASE_NAME - naziv baze podataka u kojoj se cuvaju podaci"""
        """ """
        conection_string=r'DRIVER={SQL Server Native Client 11.0};;SERVER=' + SERVER + ';DATABASE=' + DATABASE_NAME + ';UID=' + UID + ';PWD=' + PWD
        conn = pyodbc.connect(conection_string)
        cursor = conn.cursor()


        # Retrieve from table EPA_RES_NODES
        sql_command = """SELECT ID, DataTime, Demand, Head, Pressure, Chlorine, Node_Type FROM EPA_RES_NODES"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows: 
                if not row[5]==None:
                    self.RES_NODES.append(RES_NODE(row[0], row[1], float(row[2]), float(row[3]), float(row[4]), row[6]))
                    self.RES_NODES[-1].Chlorine=float(row[5])
                else:
                    self.RES_NODES.append(RES_NODE(row[0], row[1], float(row[2]), float(row[3]), float(row[4]), row[6]))                    


        # Retrieve from table EPA_RES_LINKS
        sql_command = """SELECT ID, DataTime, Flow, Velocity, Headloss, Link_Type FROM EPA_RES_LINKS"""
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        if rows:
            for row in rows:
                self.RES_LINKS.append(RES_LINK(row[0], row[1], float(row[2]), float(row[3]), float(row[4]), row[5]))

        conn.close()


    def runINP(self, EPANet, INPfile, RPTfile, OUTfile=""):
        """ RunINP(EPANet, INPfile, RPTfile, OUTfile="") - poziva i pokrece EPANet sa sledecim ulaznim podacima:"""
        """ """            
        """ EPANet - puna putanja ka epanet2d.exe fajlu"""
        """ INPfile - puna putanja ka ulaznom fajlu sa ekstenzijom *.inp"""
        """ RPTfile - puna putanja ka fajlu sa rezultatima sa ekstenzijom *.rpt"""
        """ OUTfile (opciono) - puna putanja ka binarnom fajlu sa rezultatima saekstenzijom *.out"""
        return call([EPANet, INPfile, RPTfile, OUTfile])


class JUNCTION:
    """ JUNCTION - podaci o cvorovima """
    """ Polja klase (dokumentacija: https://www.epa.gov/water-research/epanet): """
    """ """
    """ ID (string)"""
    """ Elev (float)"""
    """ Demand (float)"""
    """ Pattern (string)"""
    """ Description (string)"""
    """ X_Coord (float)"""
    """ Y_Coord (float)"""
    """ """
    def __init__(self, ID, Elev, Demand, Pattern=None, Description=None):
        self.ID = ID
        self.Elev=Elev
        self.Demand= Demand
        self.Pattern=Pattern
        self.Description=Description

class RESERVOIR:
    """ RESERVOIR - podaci o izvoristima"""
    """ Polja klase (dokumentacija: https://www.epa.gov/water-research/epanet): """
    """ """
    """ ID (string)"""
    """ Pattern (string)"""
    """ Description (string)"""
    """ X_Coord (float)"""
    """ Y_Coord (float)"""
    """ """
    def __init__(self, ID, Head, Pattern=None, Description=None):
        self.ID = ID
        self.Head=Head
        self.Pattern= Pattern
        self.Description=Description

class TANK:
    """ TANK - podaci o rezervoarima"""
    """ Polja klase (dokumentacija: https://www.epa.gov/water-research/epanet): """
    """ """
    """ ID (string)"""
    """ Elevation (float)"""
    """ InitLevel (float)"""    
    """ MinLevel (float)"""
    """ MaxLevel (float)"""    
    """ Diameter (float)"""
    """ MinVol (float)"""    
    """ VolCurve (float)"""
    """ Description (string)"""
    """ X_Coord (float)"""
    """ Y_Coord (float)"""
    """ """
    def __init__(self, ID, Elevation, InitLevel, MinLevel, MaxLevel, Diameter, MinVol, VolCurve, Description=None):    
        self.ID = ID
        self.Elevation=Elevation
        self.InitLevel= InitLevel
        self.MinLevel=MinLevel
        self.MaxLevel=MaxLevel
        self.Diameter=Diameter
        self.MinVol=MinVol
        self.VolCurve=VolCurve
        self.Description=Description


class PIPE:
    """ PIPE - podaci o cevima"""
    """ Polja klase (dokumentacija: https://www.epa.gov/water-research/epanet): """
    """ """
    """ ID (string)"""
    """ Node1 (JUNCTION, RESERVOIR, TANK)"""
    """ Node2 (JUNCTION, RESERVOIR, TANK)"""
    """ Length (float)"""
    """ Diameter (float)"""    
    """ Roughness (float)"""
    """ MinorLoss (float)"""    
    """ Status (string)"""
    """ Vert (list of tuples of float)"""
    """ Description (string)"""
    """ """
    def __init__(self, ID, Node1, Node2, Length, Diameter, Roughness, MinorLoss, Status, Description=None):        
        self.ID = ID
        self.Node1=Node1
        self.Node2= Node2
        self.Length=Length
        self.Diameter=Diameter
        self.Roughness=Roughness
        self.MinorLoss=MinorLoss
        self.Status=Status
        self.Vert=[]
        self.Description=Description


class PUMP:
    """ PUMP - podaci o pumpama"""
    """ Polja klase (dokumentacija: https://www.epa.gov/water-research/epanet): """
    """ """
    """ ID (string)"""
    """ Node1 (JUNCTION, RESERVOIR, TANK)"""
    """ Node2 (JUNCTION, RESERVOIR, TANK)"""
    """ Parameters (float)"""
    """ Description (string)"""
    """ """
    def __init__(self, ID, Node1, Node2, Parameters, Description=None): 
        self.ID = ID
        self.Node1=Node1
        self.Node2= Node2
        self.Parameters=Parameters
        self.Description=Description

class VALVE:
    """ VALVE - podaci o zatvaracima"""
    """ Polja klase (dokumentacija: https://www.epa.gov/water-research/epanet): """
    """ """
    """ ID (string)"""
    """ Node1 (JUNCTION, RESERVOIR, TANK)"""
    """ Node2 (JUNCTION, RESERVOIR, TANK)"""
    """ Diameter (float)"""
    """ Type (string)"""    
    """ Setting (float)"""
    """ MinorLoss (float)"""    
    """ Description (string)"""
    """ """
    def __init__(self, ID, Node1, Node2, Diameter, Type, Setting, MinorLoss, Description=None):        
        self.ID = ID
        self.Node1=Node1
        self.Node2= Node2
        self.Diameter=Diameter
        self.Type=Type
        self.Setting=Setting
        self.MinorLoss=MinorLoss
        self.Description=Description

class TAG:
    """ TAG - podaci o oznakama"""
    """ Polja klase (dokumentacija: https://www.epa.gov/water-research/epanet): """
    """ """
    """ ElementType (string)"""    
    """ ID (string)"""
    """ Description (string)"""
    """ """
    def __init__(self, ElementType, ID, Description=None):        
        self.ElementType = ElementType
        self.ID=ID
        self.Description=Description


class DEMAND:
    """ VALVE - podaci o cevima"""
    """ Polja klase (dokumentacija: https://www.epa.gov/water-research/epanet): """
    """ """
    """ Junction (string)"""
    """ Demand (float)"""
    """ Pattern (string)"""    
    """ Category (string)"""
    """ Description (string)"""
    """ """
    def __init__(self, Junction, Demand, Pattern, Category, Description=None):    
        self.Junction = Junction
        self.Demand=Demand
        self.Pattern= Pattern
        self.Category=Category
        self.Description=Description


class STATUS:
    """ STATUS - podaci o statusu cevi, pumpi i zatvaraca"""
    """ Polja klase (dokumentacija: https://www.epa.gov/water-research/epanet): """
    """ """
    """ ID (string)"""
    """ Status_Setting (string)"""
    """ """
    def __init__(self, ID, Status_Setting):    
        self.ID = ID
        self.Status_Setting=Status_Setting


class PATTERN:
    """ PATTERN - podaci o sablonima potrosnje"""
    """ Polja klase (dokumentacija: https://www.epa.gov/water-research/epanet): """
    """ """
    """ Description (string)"""
    """ ID (string)"""
    """ Multipliers (lista - float)"""
    """ """
    def __init__(self, Description=None):    
        self.Description=Description
        self.ID = None      
        self.Multipliers=[]

class CURVE:
    """ CURVE - podaci o krivama"""
    """ Polja klase (dokumentacija: https://www.epa.gov/water-research/epanet): """
    """ """
    """ Description (string)"""
    """ ID (string)"""
    """ X_Value (lista - float)"""
    """ Y_Value (lista - float)"""
    """ """
    def __init__(self, Description=None):    
        self.Description=Description
        self.ID = None
        self.X_Value=[]
        self.Y_Value=[] 

class RULE:
    """ RULE - podaci o slozenim kontrolama"""
    """ Polja klase (dokumentacija: https://www.epa.gov/water-research/epanet): """
    """ """
    """ Name (string)"""
    """ Lines (lista - string)"""
    """ """
    def __init__(self, Name):    
        self.Name = Name
        self.Lines=[]

class EMITTER:
    """ EMITTER - podaci o emiterima"""
    """ Polja klase (dokumentacija: https://www.epa.gov/water-research/epanet): """
    """ """
    """ Junction (string)"""
    """ Coefficient (float)"""
    """ Description (string)"""
    """ """
    def __init__(self, Junction, Coefficient, Description=None):    
        self.Junction = Junction
        self.Coefficient=Coefficient
        self.Description=Description


class QUALITY:
    """ QUALITY - podaci o kvalitetu"""
    """ Polja klase (dokumentacija: https://www.epa.gov/water-research/epanet): """
    """ """
    """ Node (string)"""
    """ InitQual (float)"""
    """ Description (string)"""
    """ """
    def __init__(self, Node, InitQual, Description=None):    
        self.Node = Node
        self.InitQual=InitQual
        self.Description=Description

class SOURCE:
    """ SOURCE - podaci o izvorima vode odredjenog kvaliteta"""
    """ Polja klase (dokumentacija: https://www.epa.gov/water-research/epanet): """
    """ """
    """ Node (string)"""
    """ Type (string)"""
    """ Quality (float)"""
    """ Pattern (string)"""
    """ Description (string)"""
    """ """
    def __init__(self, Node, Type, Quality, Pattern, Description=None):    
        self.Node = Node
        self.Type=Type
        self.Quality = Quality
        self.Pattern=Pattern
        self.Description=Description


class REACTION:
    """ REACTION - podaci o hemijskim reakcijama"""
    """ Polja klase (dokumentacija: https://www.epa.gov/water-research/epanet): """
    """ """
    """ Type (string)"""
    """ Pipe_Tank (string)"""
    """ Coefficient (float)"""
    """ Description (string)"""
    """ """
    def __init__(self, Type, Pipe_Tank, Coefficient, Description=None):    
        self.Type = Type
        self.Pipe_Tank=Pipe_Tank
        self.Coefficient = Coefficient
        self.Description=Description


class MIXING:
    """ MIXING - podaci o metodama mesanja vode u rezervoarima"""
    """ Polja klase (dokumentacija: https://www.epa.gov/water-research/epanet): """
    """ """
    """ Tank (string)"""
    """ Model (string)"""
    """ Description (string)"""
    """ """
    def __init__(self, Tank, Model, Description=None):    
        self.Tank = Tank
        self.Model=Model
        self.Description=Description


class LABEL:
    """ LABEL - podaci o oznakama na mapi"""
    """ Polja klase (dokumentacija: https://www.epa.gov/water-research/epanet): """
    """ """
    """ X_Coord (float)"""
    """ Y_Coord (float)"""
    """ Label_And_Anchor_Node (string)"""
    def __init__(self, X_Coord, Y_Coord, Label_And_Anchor_Node):    
        self.X_Coord=X_Coord 
        self.Y_Coord=Y_Coord
        self.Label_And_Anchor_Node=Label_And_Anchor_Node


class RES_NODE:
    """ RES_NODE - rezultati simulacije vezani za cvorove, izvorista i rezervoare"""
    """ Polja klase (dokumentacija: https://www.epa.gov/water-research/epanet): """
    """ """
    """ ID (string)"""
    """ DataTime (string)"""
    """ Demand (float)"""
    """ Head (float)"""
    """ Pressure (float)"""    
    """ Chlorine (float)"""
    """ Node_Type (string)"""    
    """ """
    def __init__(self, ID, Time, Demand, Head, Pressure, Node_Type='Junction'):   
        self.ID=ID      
        self.DataTime=Time 
        self.Demand=Demand
        self.Head=Head
        self.Pressure=Pressure
        self.Chlorine=None
        self.Node_Type=Node_Type

class RES_LINK:
    """ RES_LINK - rezultati simulacije vezani za cevi, pumpe i zatvarace"""
    """ Polja klase (dokumentacija: https://www.epa.gov/water-research/epanet): """
    """ """
    """ ID (string)"""
    """ DataTime (string)"""
    """ Flow (float)"""
    """ Velocity (float)"""
    """ Headloss (float)"""    
    """ Link_Type (string)"""   
    """ """
    def __init__(self, ID, Time, Flow, Velocity, Headloss, Link_Type='Pipe'): 
        self.ID=ID         
        self.DataTime=Time 
        self.Flow=Flow
        self.Velocity=Velocity
        self.Headloss=Headloss
        self.Link_Type=Link_Type
