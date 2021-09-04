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

