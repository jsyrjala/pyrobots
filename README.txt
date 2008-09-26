# methods:

# distance to nearest robot or nil
# relative version
int scan(heading, arc)
# absolute version (0 is north of arena)
int scan_abs(direction, arc)

# shoot to direction, return true if shot
bool cannon(heading, distance)
bool cannon_abs(direction, distance)

# speed change
int drive(heading, speed)
int drive_abs(direction, speed)

# robot status
[health, direction, speed, location, time] = status()
