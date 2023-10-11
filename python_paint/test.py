from paint import *


# Create the original Paint object
p = Paint()

# Create and add the design variables to paint
THRUST = DesignVariable( "AC.start", "AC.py", "%THRUST%", 50000, 40000, 60000, 3 )
SW = DesignVariable( "AC.py", "AC.py", "%SW%", 200, 150, 250, 3 )
AR = DesignVariable( "AC.py", "AC.py", "%AR%", 7, 6, 8, 3 )
p.addDesignVariable( THRUST )
p.addDesignVariable( SW )
p.addDesignVariable( AR )

# Set the execute command for the created AC.py file
p.setExecute( "py AC.py" )

# Create and set the objective
TOGW = Objective( "AC.out", "TOGW", after, Min )
p.setObjective( TOGW )

# Create and add limits (contraints)
TOFL = Limit( "AC.out", "TOFL", after, 11000, Max )
VAPP = Limit( "AC.out", "VAPP", after, 160, Max )
p.addLimit( TOFL )
p.addLimit( VAPP )

# Optimize
p.optimize()

# Check constraints
TOFL.check()
VAPP.check()

# Check that the constraints are met
print( VAPP.good )
print( TOFL.good )

# Final value for Take-off gross weight
print( TOGW.value )
