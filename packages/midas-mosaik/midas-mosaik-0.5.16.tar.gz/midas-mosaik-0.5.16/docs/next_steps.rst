Next steps
==========

In this part, you will learn about scenario configuration files and
the command line interface.

Scenario configuration
----------------------

A *midas* co-simulation is highly configurable with so-called scenario
configuration files. If you have followed this guide from the beginning,
you should by now have run your first simulation with *midas*.

Inspect your current directory and you will find a new directory
*_outputs* and inside that directory a file called *midasmv_cfg.yml*
that contains the full configuration of the scenario you ran before.
Note, since the file is created automatically, it is kind of unordered
(actually, the keys are ordered alphabetically). If you plan to tinker
around with that file, you should rename it. Otherwise, it will be
overwritten when you start the *midasmv* scenario again.

Keep this in mind. However, for the purpose of this guide, we will start with
a new and empty configuration.

Runtime configuration
---------------------

Remember, we created a runtime configuration in the first step. Now it's time
to have a short look at it. If you decided to use the default configuration,
you will find the runtime configuration *runtime-conf.yml* at

* Linux: ~/.config/midas/
* Windows: C:\\Users\\%USERNAME%\\AppData\\Local\\OFFIS\\midas\\

Open it with the text editor of your choice. Most of the stuff configured here
is not important for now. Scroll down to bottom of the file, where you find
path definitions. This contains three path definitions:

* *data_path*: This path specifies where the datasets are located. Per
  default you find this folder at the same location like the runtime
  configuration. You should not change afterwards. Otherwise, the datasets
  will be downloaded again (unless you move the old data folder to the new
  location).
* *output_path*: This path specifies where output files will be created. We
  already saw the *midasmv_cfg.yml* file that was created by the demo
  scenario. Per default, an output folder *_outputs* is created in your
  current working directory. You can change this value to an absolute path if
  you like or choose a different name. Relative paths will always use the
  current working directory as base.
* *scenario_path*: This is the configuration we're looking for. This path
  specifies where *midas* looks for scenario configuration files. Per default,
  this folder is named *midas_scenarios* and is located in the same directory
  like the runtime configuration. You can change it to any location you like
  (especially for Windows, the default location might be too hidden for
  convenient access), e.g., point it to your Documents folder.

Creating your own configuration
-------------------------------

Now, create an empty text document and rename it to *my_first_scenario.yml*.
Open it and paste the following content:

.. code-block:: yaml

  my_first_midas:
    modules: [powergrid, sndata]
    end: 1*24*60*60

This is the most simple scenario you can create. You could run it with
:code:`midasctl run my_first_midas` if you like, but we will have a closer
look at what happened here.

On the top level you find a key called *my_first_midas*. You can rename this
as you like as long as it is **unique**. If you ever happen to have the same
key twice, the scenario creation will **fail**. This key is the name that you
pass to the *midasctl* command. As long as the scenario file is located in the
scenario folder, passing that name is sufficient.

On the second level, global settings for the scenario are defined. The most
important setting is the *modules* key. It is a list specifying which modules,
i.e., which simulators, should be included in the scenario. In this case you
have *powergrid* and *sndata* (which is the simulator for the Smart Nord
dataset).

The second parameter is called *end* and specifies how many steps of the
simulation will be performed. One step corresponds to one (simulated) second.
The default step size for all simulators is 900 seconds (15 minutes). Providing a value
lower than 900 will result in only the first step simulated. It is recommended
(but not necessary) to provide this value as multiplation products since it is
more readable. In this example, we want the scenario to be simulated for one
day.

Default values
--------------

To allow such a minimalistic configuration, *midas* provides default values
for nearly everything. If you run your previously created scenario, you will
find *my_first_midas_cfg.yml* in the *_outputs* folder. You can have a look at
it and see what was auto-configurated for you. Not all the values there are
needed and most values can be left to default values.

In our example, the configuration for *powergrid* and *sndata* was auto-
configurated, i.e., a grid model was chosen and the load mapping was provided.
The default grid is *midasmv*, which is basically the CIGRE medium voltage
grid. The default mapping for *sndata* is a mapping for *midasmv*. Simply
choosing a different grid will, therefore, fail since you have to provide an
appropriate mapping.

For the rest of this tutorial, we assume that you keep the *midasmv* as grid.
However, let's add the default values to our scenario:

.. code-block:: yaml

  my_first_midas:
    modules: [powergrid, sndata]
    end: 1*24*60*60
    powergrid_params:
      my_grid:
        gridfile: midasmv
    sndata_params:
      my_grid:
        land_mapping:
          1: [[0, 1.0], [2, 1.0], [3, 2.0], [6, 2.0], [7, 1.0]]
          3: [[2, 1.0], [3, 1.0], [6, 1.0], [7, 1.0]]
          4: [[0, 2.0], [3, 2.0], [7, 1.0]]
          5: [[3, 2.0], [7, 1.0]]
          6: [[0, 2.0], [3, 1.0]]
          7: [[0, 2.0], [2, 1.0], [3, 2.0], [7, 1.0]]
          8: [[0, 1.0], [3, 1.0], [6, 1.0]]
          9: [[2, 1.0], [3, 1.0], [6, 2.0], [7, 1.0]]
          10: [[0, 2.0], [2, 1.0], [3, 1.0], [6, 2.0], [7, 1.0]]
          11: [[0, 1.0], [2, 1.0], [3, 1.0], [6, 2.0], [7, 1.0]]
    mosaikdb_params:
      import_str: mosaik_hdf5:MosaikHdf5
      filename: mymidasdb.hdf5

Just a few more words about that configuration. We added parameters for the
two modules (the key scheme is always *module name* underscore *params*).
The first subkey of those modules is *my_grid*. For both modules this key
needs to be same to allow *midas* to connect those configurations.

The *land_mapping* of *sndata* seems a bit confusing at the first look. The
first keys of the land_mapping represent the grid bus, to which load should be
connected, e.g., :code:`1: [[..], ..]` means *connect the following loads to
bus 1 of the grid*. On the next sublevel, we have a list that contains several
smaller lists. Each of these smaller lists represents a time series and is
configured by two values: The first one is the *ID* and the second one a
*scaling factor*, e.g., :code:`[6, 2.0]` means *take the time series with ID 6
and scale it with factor 2*.

This schema will be used by other modules as well, although sometimes it will
look a bit different.

Adding a different load simulator
---------------------------------

Now we will add another load simulator with commercial loads. Those loads have
a different profile than households and have their own module, which we first
have to add. Simply modify the following line of your configuration:

.. code-block:: yaml

    modules: [powergrid, sndata, comdata]

Although we have a default configuration for this as well, we will add the
parameters manually. Add the following lines after the last current line in
the file:

.. code-block:: yaml

    comdata_params:
      my_grid:
        interpolate: true
        randomize_data: true
        noise_factor: 0.2
        mapping:
          13: [[SuperMarket, 0.089]]
          14: [[SmallHotel, 0.022]]

Make sure you get the indentation right. The *comdata_params* needs to be at
the same level like the other *_params*.

You will recognize the mapping scheme. However, this time we have names as IDs
instead of numbers. You also see two new options that we've activated.

* *interpolate*: Since most of the datasets have a certain time resolution
  (e.g., hourly, quarter-hourly). Setting *interpolate* to true will activate
  interpolation if the values are accessed with higher frequency than the
  resolution. Since the commercial datasets have hourly resolution, it makes
  sense to use this feature, here.
* *randomize_data*: This feature adds a random distributed noise to the data
  from the dataset.
* *noise_factor*: The default noise is 20 % (:code:`noise_factor: 0.2`) of the
  datasets' standard deviation.

All these three options could be activated for the *sndata* module, as well.

Simulation results
------------------

Before we add the final two modules for this guide, we'll have a short look at
the simulation results. You'll find them in the *_outputs* folder. During the
simulation, a HDF5 database will be created and saved to *mymidasdb.hdf5*. You
can open this file, e.g., with `hdfview`__  or `HDFCompass`__. The database
contains most of the powergrid outputs and all outputs from the timeseries
provided by *sndata* and *comdata*. The following chart is created with
HDFCompass and displays the averaged bus voltage magnitude per unit of our
scenario.

.. image:: avg_vm_pu.png
    :width: 400

__ https://www.hdfgroup.org/downloads/hdfview/
__ https://github.com/HDFGroup/hdf-compass/tree/py3

Extending the scenario
----------------------

As last part of this tutorial, we want to add some distributed energy
resources (DER). More precise, we will add Photovoltaic (PV) plants and
combined heat and power (CHP) units. They are provided by the *pysimmods*
package that was installed together with *midas*. Both of them depend on
weather information. Therefore, we will add a weather simulator as well.

But first, we do some additional considerations. We have created a basic
scenario with loads only. Now, we are going to add some generation units. But
what if you want to compare both scenarios afterwards? Do you have to create
two files, one with and one without the generators?

Of course not. *midas* allows to create scenarios that *inherit* from
other scenarios and both can even be in the same file! Let's give it a try and
add this to the bottom of your scenario configuration file:

.. code-block:: yaml

  my_second_midas:
    parent: my_first_midas
    modules: [weather, der]
    start_date: 2017-01-01 00:00:00+0100

A scenario that has the *parent* key defined, inherits all configurations from
the parent scenario. If you change something there, it will be changed here,
too. But you are free to overwrite single values. Keys that have a list or a
dictionary, will be updated, e.g., the *modules* key is extended by two
values, *weather* and *der*. The final configuration will contain all modules
from the parent scenario and the modules from this scenario. We now also added
a start date as ISO timestring. This is the default value that is already used
in the first scenario.

First, we need to configure the weather module. Update the configuration:

.. code-block:: yaml

  my_second_midas:
    parent: my_first_midas
    modules: [weather, der]
    start_date: 2017-01-01 00:00:00+0100
    weather_params:
      my_weather_station:
        weather_mapping:
          WeatherCurrent: ["interpolate": true]

Like at the grid configuration, we have a custom name *my_weather_station*
here. This name is required when we a assign the a weather station to our DER
models. The *weather_mapping* allows to define two models, *WeatherCurrent*
and *WeatherForecast*. The latter will not be used in this tutorial.
Additionally, multiple instances can be created, although most of the time one
instance should be sufficient. Furthermore, interpolation and randomization
can be activated for each instance individually.

Next, we need to add the DER models. The module is already loaded, so we only
need to add the configuration.

.. code-block:: yaml

  der_params:
    my_grid_pv:
      grid_name: my_grid
      mapping:
        3: [[PV, 3], [PV, 1]]
        7: [[PV, 1]]
        8: [[PV, 2]]
        14: [[PV, 2], [PV, 2]]
      weather_provider_mapping:
        PV: [my_weather_station, 0]

(Again, make sure you get the indentation right.)
Most of the scheme should be common by now. However, some things are
different. Instead of relying on the subkey *my_grid* like at the other
simulators, we added a new key-value pair *grid_name* that needs to store the
correct value. This means, *my_grid_pv* does not need to match the correct
grid.

This allows you to split the definition or even define multiple simulators for
the same grid, e.g., one for PV plants and a second one for CHP.
Alternatively, it is still possible to only use a single simulator for both.

The *mapping* follows the same rules like what we've seen before. The new
thing here is the *weather_provider_mapping*. This field defines, which
weather station is used as source for weather data. You need to define a
mapping for each plant type but in the most simple case, all plants of a type
use the same weather data provider.

Next, we add another simulator definition for the CHP models and change the
path of the database, so that a different database will be created instead of
overwriting the database from *my_first_midas*. The full configuration file
now looks like:

.. code-block:: yaml

  my_first_midas:
    modules: [powergrid, sndata, comdata]
    end: 1*24*60*60
    powergrid_params:
      my_grid:
        gridfile: midasmv
    sndata_params:
      my_grid:
        land_mapping:
          1: [[0, 1.0], [2, 1.0], [3, 2.0], [6, 2.0], [7, 1.0]]
          3: [[2, 1.0], [3, 1.0], [6, 1.0], [7, 1.0]]
          4: [[0, 2.0], [3, 2.0], [7, 1.0]]
          5: [[3, 2.0], [7, 1.0]]
          6: [[0, 2.0], [3, 1.0]]
          7: [[0, 2.0], [2, 1.0], [3, 2.0], [7, 1.0]]
          8: [[0, 1.0], [3, 1.0], [6, 1.0]]
          9: [[2, 1.0], [3, 1.0], [6, 2.0], [7, 1.0]]
          10: [[0, 2.0], [2, 1.0], [3, 1.0], [6, 2.0], [7, 1.0]]
          11: [[0, 1.0], [2, 1.0], [3, 1.0], [6, 2.0], [7, 1.0]]
    comdata_params:
      my_grid:
        interpolate: true
        randomize_data: true
        noise_factor: 0.2
        mapping:
          13: [[SuperMarket, 0.089]]
          14: [[SmallHotel, 0.022]]
  my_second_midas:
    parent: my_first_midas
    modules: [weather, der]
    start_date: 2017-01-01 00:00:00+0100
    weather_params:
      my_weather_station:
        weather_mapping:
          WeatherCurrent: ["interpolate": true]
    der_params:
      my_grid_pv:
        grid_name: my_grid
        sim_name: PysimmodsPV
        mapping:
          3: [[PV, 3], [PV, 1]]
          7: [[PV, 1]]
          8: [[PV, 2]]
          14: [[PV, 2], [PV, 2]]
        weather_provider_mapping:
          PV: [my_weather_station, 0]
      my_grid_chp:
        grid_name: my_grid
        sim_name: PysimmodsCHP
        mapping:
          4: [[CHP, 0.4], [CHP, 0.4]]
          13: [[CHP, 0.4], [CHP, 0.4], [CHP, 0.4]]
        weather_provider_mapping:
          CHP: [my_weather_station, 0]
    mosaikdb_params:
      filename: my_second_midas.hdf5

Note that we removed the `import_str` from `mosaikdb_params`. While the
*mosaik_hdf5* is conveniently inspectable with tools like *HDFView* or
*HDFCompass*, inside the code it is much easier to work with pandas/pytables.
The default store `MidasHdf` relies on those packages. Let's run the new
scenario: `midasctl run my_second_midas`.

Once the simulation has finished, we can use the analysis function of midas:
`midasctl analyze _outputs/my_second_midas.hdf5`.
This will create a folder _outputs/my_second_midas/ and in that folder a
markdown document, containing some interesting information about the simulation
run:

.. code-block:: markdown

  # Analysis of my_second_midas_Powergrid-0

  ## Summary

  * bus health: 100.00 %
  * active energy sufficiency: 80.76 %

  ## Demand and Supply

  * total active energy demand: 43.50 MWh
  * total active energy supply: 35.13 MWh or about 11.71 full load hours
  * extg. active energy supply: 28.69 MWh
  * total reactive energy demand: 21.07 MVArh
  * total reactive energy supply: -0.55 MVArh
  * extg. reactive energy supply: 16.51 MVArh
  * total apparent energy demand: 48.33 MVAh
  * total apparent energy supply: 35.13 MVAh
  * extg. apparent energy supply: 33.10 MVAh

This concludes this short tutorial. Further information will follow in the
near future.
