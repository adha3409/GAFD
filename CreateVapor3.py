import numpy as np
import sys
import h5py
from netCDF4 import Dataset


try:
    visStates = sys.argv[1:]
except:
    print('failure to read inputs')
    sys.exit()


dataset = Dataset('vapor.nc', 'w', format = 'NETCDF4_CLASSIC')

try:
    vis = h5py.File(visStates[0], 'r')
except:
    print('failed to open ' + visStates[0])
    sys.exit()

try:
    xmesh = np.sort(vis.get('mesh/grid_x'))
    ymesh = np.sort(vis.get('mesh/grid_y'))
    zmesh = np.sort(vis.get('mesh/grid_z'))
except:
    print('failed to open meshgrid')
    sys.exit()


x = dataset.createDimension('x', len(xmesh))
x = dataset.createDimension('y', len(ymesh))
z = dataset.createDimension('z', len(zmesh))
time = dataset.createDimension('time',len(visStates))

xcoord = dataset.createVariable('x', np.float32, ('x'))
ycoord = dataset.createVariable('y', np.float32, ('y'))
zcoord = dataset.createVariable('z', np.float32, ('z'))
tcoord = dataset.createVariable('time', np.float32, ('time'))

xcoord.axis = 'Y'
ycoord.axis = 'X'
zcoord.axis = 'Z'
tcoord.axis = 'T'
tcoord.units = 's'

xcoord[:] = xmesh
ycoord[:] = ymesh
zcoord[:] = zmesh
tcoord[:] = np.arange(len(visStates))


ux = dataset.createVariable('ux',np.float32,('time','z','x','y'))
uy = dataset.createVariable('uy',np.float32,('time','z','x','y'))
uz = dataset.createVariable('uz',np.float32,('time','z','x','y'))
vortx = dataset.createVariable('vortx',np.float32,('time','z','x','y'))
vorty = dataset.createVariable('vorty',np.float32,('time','z','x','y'))
vortz = dataset.createVariable('vortz',np.float32,('time','z','x','y'))
#Bx = dataset.createVariable('Bx',np.float32,('time','z','x','y'))
#By = dataset.createVariable('By',np.float32,('time','z','x','y'))
#Bz = dataset.createVariable('Bz',np.float32,('time','z','x','y'))
temp_fluct = dataset.createVariable('temp_fluct',np.float32,('time','z','x','y'))


for i in range(len(visStates)):
    try:
        vis = h5py.File(visStates[i], 'r')
    except:
        print('failed to open ' + visStates[i])
        sys.exit()


    data_ux = vis.get('velocity/velocity_x')
    data_uy = vis.get('velocity/velocity_y')
    data_uz = vis.get('velocity/velocity_z')
    data_vortx = vis.get('velocity_curl/velocity_curl_x')
    data_vorty = vis.get('velocity_curl/velocity_curl_y')
    data_vortz = vis.get('velocity_curl/velocity_curl_z')
#    data_Bx = vis.get('magnetic/magnetic_x')
#    data_By = vis.get('magnetic/magnetic_y')
#    data_Bz = vis.get('magnetic/magnetic_z')
    data_temp = vis.get('fluct_temperature/fluct_temperature')


    ux[i,:,:,:] = data_ux
    uy[i,:,:,:] = data_uy
    uz[i,:,:,:] = data_uz
    vortx[i,:,:,:] = data_vortx
    vorty[i,:,:,:] = data_vorty
    vortz[i,:,:,:] = data_vortz
#    Bx[i,:,:,:] = data_Bx
#    By[i,:,:,:] = data_By
#    Bz[i,:,:,:] = data_Bz
    temp_fluct[i,:,:,:] = data_temp




dataset.close()
