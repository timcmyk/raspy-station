# raspy-station
Locally running program on raspberry pi to collect data, transform and persist it into a db 

## Hardware Setup
### Sensors
*ToDo: Link to the supported sensors*

*ToDo: Description where to install them*

![image](https://github.com/timcmyk/raspy-station/assets/61316496/34e57a11-120f-4168-847e-c7d553893181)
### Things to do on your Raspberry Pi
*ToDo: Description what to do on the Rasperry Pi, f.e. activate I2C*
### 
## Software Setup 
### Prerequisites
*ToDo: List all pip dependencies*

- ...
- ...
- ...

### Initialize db entities
Initially you have to create new DB Entities for Owner, Raspy and at least one Sensor.

#### Preparation
In order to do that you have to use our custom CLI Tools that can be found in the directory src/initialization/

> First of all you have to manually add the following sub-directories within there:  
> - `mkdir target`
> - `cd target`
> - `mkdir raspys`
> - `mkdir sensors`

Go back into src/initialization/ - `cd ..`

Now you are able to start the initialization process.

#### Database Connection
*ToDos:* 
*- Change productive db password and remove it from repo*
*- Adjust documentation for description how to connect to db* 


#### Set up your identity
> It is only possible to generate one owner entity.
>
> - `python owner.py name <your-name>`
> - `python owner.py save`
>
> Changing your name is possible by repeating the process.

#### Set up your raspy
You are allowed to add as much rasperry pi entities to the ecosystem as you want.

> - `python raspy.py name <raspy-name>`
> - `python raspy.py owner <raspy-name> <your-owner-id>`

You will find your ownerId in the 'owner.json' file that has been generated in the step before (sitting within the target directory).
Don't forget to set your raspy name as a parameter to localize the specific raspy you want to add/manipulate.

> - `python raspy.py save`

Changing the name of your raspy is possible by running: 
> - `python raspy.py changeName <old-raspy-name> <new-raspy-name>`

Don't forget to run `python raspy.py save` after this to have your changes applied to the database. 

#### Set up your sensors
You are allowed to add as much sensor entities to the ecosystem as you want.

> - `python sensor.py address <sensor-address>`

Address is allowed to be number or string. 
It works as a local identifier for your sensor. Later on it could be used to dynamically call for sensor data at the right spot on your raspberry bus.   

Furthermore it is necessary to add the following attributes to each of your sensors. 
It is important that you specify which sensor entity you are trying to manipulate by giving the sensor-address as an input parameter.
> - `python sensor.py raspyId <sensor-address> <raspy-id>`
> - `python sensor.py name <sensor-address> <sensor-name>`
> - `python sensor.py unit <sensor-address> <raspy-unit>`
> - `python sensor.py highestPossible <sensor-address> <sensors-highest-possible-value>`
> - `python sensor.py lowestPossible <sensor-address> <sensors-lowest-possible-value>`

Apply your changes to the database by running
> - `python sensor.py save`

Change attributes by repeating the specific command followed by the save operation.

After saving your sensors you can find a .json file for each of them within ./target/sensors/

> Take those ids and replace the existing input parameters in the 'saveDataEntry'-method-calls in the main.py module (Lines 33 and 34 at the moment). 
