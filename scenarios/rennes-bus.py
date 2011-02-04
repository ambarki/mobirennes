#MUMORO CONFIGURATION BEFORE LAUNCHING SERVER

#Database type, choose among : 'sqlite', 'mysql', 'postgres', 'oracle', 'mssql', and 'firebird'
db_type = 'sqlite'

#Database connexion URL
#For user oriented databases : 'username:password@host:port/database'
#Port can be excluded (default one depending on db_type will be used) : 'username:password@host/database'
#For SQLiTE : 'file_name.db' for relative path or absolute : '/data/guidage/file_name.db'
db_params = 'db.sqlite'

#Load street data from (compressed or not) osm file(s)
#-----------------------------------------------------
osm_data = import_street_data( 'rennes.osm' )

#Load bike service from an API URL (Don't forget to add http://) with required valid params (depending on each API)
#------------------------------------------------------------------------------------------------------------------
# data_bike = import_bike_service('http://data.keolis-rennes.com/xml/?version=1.0&key=6D0RGK6K94FYNI6&cmd=getstation&param[request]=all', 
                                 # 'Le velo STAR')


#Loads muncipal data file and inserts it into database.
#starting_date & end_date in this format : 'YYYYMMDD' Y for year's digists, M for month's and D for day's
#starting_date and end_date MUST be defined if municipal data is imported
#------------------------------------------------------------------------------------------------------------------

start_date = '20110101'
end_date = '20110331'

star_data = import_gtfs_data('GTFS-20110101.zip', 'Bus STAR')

#Create relevant layers from previously imported data (origin paramater) with a name, a color and the mode.
#Color in the html format : '#RRGGBB' with R, G and B respetcly reg, green and blue values in hex
#Mode choose among: mumoro.Foot, mumoro.Bike and mumoro.Car 
#For GTFS Municipal layer dont mention layer mode
#--------------------------------------------------------------------------------------------------------------------
foot_layer = street_layer( data=osm_data , name='Foot', color='#7E2217', mode=mumoro.Foot )
# bike_layer = street_layer( data=osm_data, name='Bike', color='#652AF7', mode=mumoro.Bike )
star_layer = public_transport_layer(data=star_data ,name='STAR', color='#4CC417' )

paths( foot_layer, foot_layer, [ mode_change, line_change ] )
# paths( star_layer, star_layer, [ dist, mode_change ] )

#Starting layer is the layer on wich the route begins
#Destination layer is the layer on wich the route finishes
#Starting & destination layers MUST be selected, otherwise the server could not start
#If by mistake you select more than one starting/destination layers, the affectation will go on the last one
# set_starting_layer( layer )
# set_destination_layer( layer )

#Creates a transit cost variable, including the duration in seconds of the transit and if the mode is changed (True or False)
#------------------------------------------------------------------------------------------------------------
#cost1 = cost( duration , mode_changed )
cost1 = cost( duration = 120, mode_change = True )
cost2 = cost( duration = 60, mode_change = False )
#Connect 2 given layers on same nodes with the given cost(s)
#-----------------------------------------------------------
#connect_layers_same_nodes( layer1 , layer2 , cost )

#Connect 2 given layers on nodes imported from a list (Returned value from import_bike_service or import_municipal_data) with the given cost(s)
#----------------------------------------------------------------------------------------------------------------------------------------------
#connect_layers_from_node_list( layer1, layer2, list, cost1, cost2 )
#Connect 2 given layers on nearest nodes
#----------------------------------------
#connect_layers_on_nearest_nodes( layer1, layer2, cost )

# connect_layers_from_node_list( foot_layer, bike_layer, data_bike,cost1, cost2 )
connect_layers_on_nearest_nodes(star_layer, foot_layer, cost1 , cost2)


#Administrator valid email
#REQUIRED for geocoding services, if empty the service will NOT work
#-------------------------------------------------------------------
admin_email = 'pplr@free.fr'

#Website valid URL : 'http://url/' example 'http://mumoro.openstreetmap.fr/'
#REQUIRED for urls generating (allowing you to send the url to a friend and to find the same route)
#--------------------------------------------------------------------------------------------------
web_url =  'http://localhost:8085'

#Listening port
#Check that it is free and port-fordwarded if behind a router
#-------------------------------------------------------------
listening_port = 8085
