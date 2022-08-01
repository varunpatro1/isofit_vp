from isofit.inversion.inverse import error_code

from isofit.configs.base_config import BaseConfigSection
from isofit.configs.configs import Config
from isofit.utils import surface_model
from isofit.core.forward import ForwardModel
from isofit.configs.configs import create_new_config, get_config_differences
from isofit.inversion.inverse import Inversion
from isofit.core.fileio import IO
import numpy as np


def test_error_code():
    assert error_code == -1

print('BUILDING ...')

# Surface model
surface_model("examples/20171108_Pasadena/configs/ang20171108t184227_surface.json")

config = create_new_config("examples/20171108_Pasadena/configs/ang20171108t184227_beckmanlawn.json")
fm = ForwardModel(config)


x = np.loadtxt(r'/Users/varunpatro/Desktop/avirisng_input.txt')
x = np.append(x,1.75)
x = np.append(x,0.05)

inv = Inversion(config, fm)
io = IO(config, fm)

io.get_components_at_index(0, 0)
geom = io.current_input_data.geom # alternately, call via geom = Geometry()...this won't have data from the above config file
meas = io.current_input_data.meas  # a numpy  array

assert(inv.full_statevector(x).all() == x.all()) # inv.self_fixed = None

count = 0
OE_estimations = [[], [], [], [], []]
for i in range(5):
    radiance_measurement = fm.calc_rdn(x,geom)
    calculated_reflectance = inv.invert(radiance_measurement, geom)[0]
    OE_estimations[i] = calculated_reflectance

OE_estimations = np.array(OE_estimations)

assert(OE_estimations[0,:].all() == OE_estimations[1,:].all())
assert(OE_estimations[0,:].all() == OE_estimations[2,:].all())
assert(OE_estimations[0,:].all() == OE_estimations[3,:].all())
assert(OE_estimations[0,:].all() == OE_estimations[4,:].all())


#print(type(inv.invert(radiance_measurement, geom)))
#print(inv.invert(radiance_measurement, geom).shape)
<<<<<<< HEAD
#print(inv.invert(radiance_measurement, geom)[0])
=======
np.savetxt(r'/Users/varunpatro/Desktop/OE_reflectance_estimation.txt',\
     OE_estimations)

#first_col = OE_estimations[0,:]
#print(OE_estimations.shape)
#print(first_col.shape)

#for i in range(1,5):


>>>>>>> 7233fc971e1c5d194c3e09be071e3fec685afe1c

print('TESTS COMPLETE')




