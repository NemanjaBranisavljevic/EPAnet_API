# EPANetPY API Guide

## Introduction
EPANet is a software solution for mathematical modeling of pressurized networks. Input data is stored in an input file (with a *.INP extension), while the simulation results (where the simulation involves running the model with a single version of input data) are written to an output file (with a *.RPT extension).

- `readINP(filenameINP)` – loads data from the *.INP file into the class's data structure
- `writeINP(filenameINP)` – creates the *.INP file and populates it with data from the class's data structure
- `pushData(SERVER, DEFAULT_DATABASE, UID, PWD, DATABASE_NAME)` – forms and populates the appropriate tables in the MSSQL Server database with data from the class's data structure
- `retrieveData(SERVER, UID, PWD, DATABASE_NAME)` – loads model input data from the MSSQL Server database into the class's data structure
- `readRPT(filenameRPT)` – loads data from the *.RPT file into the class's data structure
- `pushRPT(SERVER, UID, PWD, DATABASE_NAME)` - forms and populates the appropriate tables in the MSSQL Server database from the class's data structure
- `retrieveRPT(SERVER, UID, PWD, DATABASE_NAME)` - loads simulation results from the MSSQL Server database into the class's data structure
- `runINP(EPANet, INPfile, RPTfile, OUTfile="")` – runs a simulation with data from the corresponding *.INP file and creates a *.RPT file with simulation results

The data structure in the `EPANetModel` class consists of lists and associative tables that store all data needed for simulation in the EPANet software package. The data structure in the `EPANetModel` class includes the following components:

- `TITLE` (list) - Name of the simulation.
- `JUNCTIONS` (list) - List of objects with node data in the network.
- `RESERVOIRS` (list) - List of objects with data on reservoirs and sources.
- `TANKS` (list) - List of objects with data on tanks.
- `PIPES` (list) - List of objects with data on pipes in the network.
- `PUMPS` (list) - List of objects with data on pumps in the network.
- `VALVES` (list) - List of objects with data on valves in the network.
- `TAGS` (list) - List of objects with tag data.
- `DEMANDS` (list) - List of objects with node demand data.
- `STATUS` (list) - List of objects with status data of links in the network (pipes, pumps, and valves).
- `PATTERNS` (list) - List of objects with consumption pattern data.
- `CURVES` (list) - List of objects with curve data (Q/H characteristics of pumps, etc.).
- `CONTROLS` (list) - List with control data.
- `RULES` (list) - List of objects with data on more complex controls.
- `ENERGY` (associative table) - Table with data necessary for calculating energy balances.
- `EMITTERS` (list) - List of objects with emitter data.
- `QUALITY` (list) - List of objects with water quality data.
- `SOURCES` (list) - List of objects with data on water sources of specific quality.
- `REACTIONS` (list) - List of objects with data related to chemical reactions.
- `REACTIONS_1` (associative table) - Table with data on chemical reactions.
- `MIXING` (list) - List of objects with data on methods of mixing water in tanks.
- `TIMES` (associative table) - Table with time data related to the simulation.
- `REPORT` (associative table) - Table with data on how to form reports.
- `OPTIONS` (associative table) - Table with data on options related to the simulation.
- `LABELS` (list) - List of objects with label data.
- `BACKDROP` (associative table) - Table with data on the background image.
- `META` (associative table) - Table with meta-data about the version of the model.
- `RES_NODES` (list) - List of objects with simulation results related to nodes, sources, and reservoirs.
- `RES_LINKS` (list) - List of objects with simulation results related to pipes, pumps, and valves.

In addition to the main API class, data in the lists is stored through types specific to certain data related to water system components. The type names correspond to the names of the sections in which the input data in the *.INP file and the simulation results in the *.RPT file are found. Additional explanations regarding the types and fields in their structure can be found in the official EPANet software package documentation at [EPA Website](https://www.epa.gov/water-research/epanet). The following types have been created for data storage:

### Data Types

#### JUNCTION - Node Data
Class Fields:
- `ID` (string)
- `Elev` (float)
- `Demand` (float)
- `Pattern` (string)
- `Description` (string)
- `X_Coord` (float)
- `Y_Coord` (float)

#### RESERVOIR - Source Data
Class Fields:
- `ID` (string)
- `Pattern` (string)
- `Description` (string)
- `X_Coord` (float)
- `Y_Coord` (float)

#### TANK - Tank Data
Class Fields:
- `ID` (string)
- `Elevation` (float)
- `InitLevel` (float)
- `MinLevel` (float)
- `MaxLevel` (float)
- `Diameter` (float)
- `MinVol` (float)
- `VolCurve` (float)
- `Description` (string)
- `X_Coord` (float)
- `Y_Coord` (float)

#### PIPE - Pipe Data
Class Fields:
- `ID` (string)
- `Node1` (JUNCTION, RESERVOIR, TANK)
- `Node2` (JUNCTION, RESERVOIR, TANK)
- `Length` (float)
- `Diameter` (float)
- `Roughness` (float)
- `MinorLoss` (float)
- `Status` (string)
- `Vert` (list of tuples of float)
- `Description` (string)

#### PUMP - Pump Data
Class Fields:
- `ID` (string)
- `Node1` (JUNCTION, RESERVOIR, TANK)
- `Node2` (JUNCTION, RESERVOIR, TANK)
- `Parameters` (float)
- `Description` (string)

#### VALVE - Valve Data
Class Fields:
- `ID` (string)
- `Node1` (JUNCTION, RESERVOIR, TANK)
- `Node2` (JUNCTION, RESERVOIR, TANK)
- `Diameter` (float)
- `Type` (string)
- `Setting` (float)
- `MinorLoss` (float)
- `Description` (string)

#### TAG - Tag Data
Class Fields:
- `ElementType` (string)
- `ID` (string)
- `Description` (string)

#### STATUS - Link Status Data
Class Fields:
- `ID` (string)
- `Status_Setting` (string)

#### PATTERN - Consumption Pattern Data
Class Fields:
- `Description` (string)
- `ID` (string)
- `Multipliers` (list - float)

#### CURVE - Curve Data
Class Fields:
- `Description` (string)
- `ID` (string)
- `X_Value` (list - float)
- `Y_Value` (list - float)

#### RULE - Complex Control Data
Class Fields:
- `Name` (string)
- `Lines` (list - string)

#### EMITTER - Emitter Data
Class Fields:
- `Junction` (string)
- `Coefficient` (float)
- `Description` (string)

#### QUALITY - Quality Data
Class Fields:
- `Node` (string)
- `InitQual` (float)
- `Description` (string)

#### SOURCE - Water Source Data
Class Fields:
- `Node` (string)
- `Type` (string)
- `Quality` (float)
- `Pattern` (string)
- `Description` (string)

#### REACTION - Chemical Reaction Data
Class Fields:
- `Type` (string)
- `Pipe
Here's the translation in Markdown format:

```markdown
# REACTION
Data on chemical reactions. Class fields:
- **Type** (string)
- **Pipe_Tank** (string)
- **Coefficient** (float)
- **Description** (string)

# MIXING
Data on water mixing methods in tanks. Class fields:
- **Tank** (string)
- **Model** (string)
- **Description** (string)

# LABEL
Data on map labels. Class fields:
- **X_Coord** (float)
- **Y_Coord** (float)
- **Label_And_Anchor_Node** (string)

# RES_NODE
Simulation results related to nodes, sources, and tanks. Class fields:
- **ID** (string)
- **DataTime** (string)
- **Demand** (float)
- **Head** (float)
- **Pressure** (float)
- **Chlorine** (float)
- **Node_Type** (string)

# RES_LINK
Simulation results related to pipes, pumps, and valves. Class fields:
- **ID** (string)
- **DataTime** (string)
- **Flow** (float)
- **Velocity** (float)
- **Headloss** (float)
- **Link_Type** (string)

## Methods in the EPANetModel class:

- **readINP(filenameINP)** - Method of the EPANetModel class for loading data from a *.INP file. The input of this method (filenameINP) represents the path to the *.INP file, the input file of the EPANet software package.

- **writeINP(filenameINP)** - Method of the EPANetModel class for creating a *.INP file. The input of this method (filenameINP) represents the path and name of the *.INP file to be created.

- **pushData(SERVER, DEFAULT_DATABASE, UID, PWD, DATABASE_NAME)** - Method of the EPANetModel class for sending data from the object to the MSSQL Server database. The inputs of this method are:
  - **SERVER** - name of the MSSQL server
  - **DEFAULT_DATABASE** - existing database
  - **UID** - username
  - **PWD** - password
  - **DATABASE_NAME** - name of the database where the data will be stored

Data from the class data structure is written to the following tables:
- **EPA_TITLE** - columns: DBID (ID field in the database), Line
- **EPA_JUNCTIONS** - columns: DBID, ID, Elev, Demand, Pattern, Description, X_Coord, Y_Coord
- **EPA_RESERVOIRS** - columns: DBID, ID, Head, Pattern, Description, X_Coord, Y_Coord
- **EPA_TANKS** - columns: DBID, ID, Elevation, InitLevel, MinLevel, MaxLevel, Diameter, MinVol, VolCurve, Description, X_Coord, Y_Coord
- **EPA_PIPES** - columns: DBID, ID, Node1, Node2, Length, Diameter, Roughness, MinorLoss, Status, Description, Vert VARCHARmax
- **EPA_PUMPS** - columns: DBID, ID, Node1, Node2, Parameters, Description
- **EPA_VALVES** - columns: DBID, ID, Node1, Node2, Diameter, Type, Setting, MinorLoss, Description
- **EPA_TAGS** - columns: DBID, ElementType, ID, Description
- **EPA_DEMANDS** - columns: DBID, Junction, Demand, Pattern, Category, Description
- **EPA_STATUS** - columns: DBID, ID, Status_Setting
- **EPA_PATTERNS** - columns: DBID, ID, Position INT, Multipliers, Description
- **EPA_CURVES** - columns: DBID, ID, Position INT, X_Value, Y_Value, Description
- **EPA_CONTROLS** - columns: DBID, Line
- **EPA_RULES** - columns: DBID, Name, Position INT, Lines
- **EPA_ENERGY** - columns: DBID, Global_Efficiency, Global_Price, Demand_Charge
- **EPA_EMITTERS** - columns: DBID, Junction, Coefficient, Description
- **EPA_QUALITY** - columns: DBID, Node, InitQual, Description
- **EPA_SOURCES** - columns: DBID, Node, Type, Quality, Pattern, Description
- **EPA_REACTIONS** - columns: DBID, Type, Pipe_Tank, Coefficient, Description
- **EPA_REACTIONS_1** - columns: DBID, Order_Bulk, Order_Tank, Order_Wall, Global_Bulk, Global_Wall, Limiting_Potential, Roughness_Correlation
- **EPA_MIXING** - columns: DBID, Tank, Model, Description
- **EPA_TIMES** - columns: DBID, Duration, Hydraulic_Timestep, Quality_Timestep, Pattern_Timestep, Pattern_Start, Report_Timestep, Report_Start, Start_ClockTime, Statistic
- **EPA_REPORT** - columns: DBID, Status, Summary, Page, Node, Link
- **EPA_OPTIONS** - columns: DBID, Units, Headloss, Specific_Gravity, Viscosity, Trials, Accuracy, CHECKFREQ, MAXCHECK, DAMPLIMIT, Unbalanced, Pattern, Demand_Multiplier, Emitter_Exponent, Quality, Diffusivity, Tolerance
- **EPA_LABELS** - columns: DBID, X_Coord, Y_Coord, Label_And_Anchor_Node
- **EPA_BACKDROP** - columns: DBID, DIMENSIONS, UNITS, BACKDROP_FILE, OFFSET
- **EPA_META** - columns: DBID, Version, Date, SimulationName, Description

- **retrieveData(SERVER, UID, PWD, DATABASE_NAME)** - Method of the EPANetModel class for loading data from the MSSQL Server database into the fields of the class object. The inputs of this method are:
  - **SERVER** - name of the MSSQL server
  - **UID** - username
  - **PWD** - password
  - **DATABASE_NAME** - name of the database where the data is stored

- **readRPT(filenameRPT)** - Method of the EPANetModel class for loading data from the simulation results file into the fields of the class object. The input of this method (filenameRPT) represents the name of the simulation results file.

- **pushRPT(SERVER, UID, PWD, DATABASE_NAME)** - Method of the EPANetModel class for sending simulation results to the MSSQL Server database. The database must already exist. It is best for the database to contain the data based on which the *.INP file for the simulation was created. The inputs of this method are:
  - **SERVER** - name of the MSSQL server
  - **UID** - username
  - **PWD** - password
  - **DATABASE_NAME** - name of the database where the data will be stored

Data is written to the following tables:
- **EPA_RES_NODES** - columns: DBID, ID, DataTime, Demand, Head, Pressure, Chlorine, Node_Type
- **EPA_RES_LINKS** - columns: DBID, ID, DataTime, Flow, Velocity, Headloss, Link_Type

- **retrieveRPT(SERVER, UID, PWD, DATABASE_NAME)** - Method of the EPANetModel class for loading simulation results from the MSSQL Server database into the fields of the class object. The inputs of this method are:
  - **SERVER** - name of the MSSQL server
  - **UID** - username
  - **PWD** - password
  - **DATABASE_NAME** - name of the database where the data is stored

## OPERATING SYSTEM
The API is developed on the Windows operating system. It has not been tested on other operating systems.

## PROGRAMMING LANGUAGES
The API is written in Python 2.7. The interpreter for this programming language can be installed for free from the website – [python.org](https://www.python.org). SQL was used for creating databases, creating tables within the database, populating tables, and retrieving data from tables.

## DATABASE
An MSSQL Server database was used as the database. It is recommended to use version 2008 or higher.

## LIBRARIES
To communicate the API with the database, it is necessary to install the free `pyodbc` library ([pyodbc GitHub](https://github.com/mkleehammer/pyodbc)). The `pyodbc` library can be installed automatically if you are connected to the internet by typing the following in the command window:
```bash
pip install pyodbc
```
Alternatively, you can manually select the appropriate installation file from [Google Code Archive](https://code.google.com/archive/p/pyodbc/downloads).

## EXAMPLES OF API USAGE

```markdown
# EXAMPLES OF API USAGE
```

Loading a *.INP file into the data structure of the EPANetModel class:
```python
from EPANetPY import *  
e = EPANetModel() 
e.readINP('NS.inp')
```

Entering metadata into the data structure of the EPANetModel class:
```python
from EPANetPY import *  
e = EPANetModel() 
e.readINP('NS.inp') 
e.META['Version'] = 'Version 1' 
e.META['VersionDate'] = '1/1/2016' 
e.META['SimulationName'] = 'Simulation 1' 
e.META['Description'] = 'This is the first simulation'
```

Changing input data in the fields of the EPANetModel class object:
```python
from EPANetPY import *  
e = EPANetModel() 
e.readINP("NS.inp") 
e.JUNCTIONS[0].Demand = 25 
```

Writing input data to the database from the EPANetModel class objects:
```python
from EPANetPY import *  
e = EPANetModel() 
e.readINP("NS.inp") 
e.pushData(xxxxxx, yyyyyy, zzzzzz, ccccccc, 'EPANet_1')
```

Loading input data from the database into the data structure of the EPANetModel class:
```python
from EPANetPY import *  
b = EPANetModel() 
b.retrieveData(xxxxxx, zzzzzz, ccccccc, 'EPANet_1')
```

Creating a *.INP file from the data structure of the EPANetModel class:
```python
from EPANetPY import *  
b = EPANetModel() 
b.retrieveData(xxxxxx, zzzzzz, ccccccc, 'EPANet_1') 
b.writeINP('NS1.inp')
```

Simulation:
```python
from EPANetPY import *  
b.runINP('epanet2d.exe', 'NS.inp', 'NS.rpt')  # *RPT file may be huge
```

Loading a *.RPT file into the data structure of the EPANetModel class:
```python
from EPANetPY import *  
e.readRPT('t1.rpt')
```

Reviewing the simulation results:
```python
from EPANetPY import *  
e.readRPT('t1.rpt') 
print(e.RES_NODES[0].Pressure) 
```

Writing simulation results to the database from the data structure of the EPANetModel class:
```python
from EPANetPY import *  
e.readRPT('t1.rpt') 
e.pushRPT(xxxxxx, zzzzzz, ccccccc, 'EPANet_1')
```

Loading simulation results from the database into the data structure of the EPANetModel class:
```python
from EPANetPY import *  
c = EPANetModel() 
c.retrieveRPT(xxxxxx, zzzzzz, ccccccc, 'EPANet_1')
```
```
