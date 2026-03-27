Hello! This is our code for the 'Raspberry Pi competitie 2025-2026'. We decided to make a rainwater management system as it is handy for saving water.



Here’s how it works:


1. The code checks several things at once, such as whether it will be dry over the next two days, or whether it’s time to water the plants.

2. The code checks if there is enough water in the tank using an ultrasonic distance sensor; based on that, it decides whether to water the plants or not. If there is too much water in the tank, it drains it into the sewer.

3. The code also checks if a significant amount of precipitation is expected in the next 2 days (20 mm/hour or higher). If so, it drains all the water into the sewer so that it can receive fresh water as soon as it rains.
The code also takes care not to overwater the plants, as this is unhealthy for them.
