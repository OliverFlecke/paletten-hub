# Temperature

Sensors are connected to the follwing pins:

| Place   | Pin |
| ------- | --- | 
| Inside  | 4   |
| Outside | 27  |

## Broker topics

Each sensor publishes data to the following topics:

- `temperature/<place>` contains the latest temperature in degrees Celcius
- `humidity/<place>` contains the latest humidity between 0 and 100
- `history/<place>` has data from the last 24 hours

This project also contains a temperature control, which listens to the inside temperature sensor and turn on the heaters if needed.

- `temperature/set` can be used to set the desired temperature. If the temperature from the sensor is below this value, the heaters will be turned on. Note that while it accepts any value, the heaters will not go above ~25 degrees Celsius.
- `temperature/auto` can be used to enable/disable the temperature control feature. It accepts `true` or `false` as strings.

