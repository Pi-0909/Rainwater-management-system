NEDERLANDS

Hallo! Dit is onze code voor de Raspberry-pi competitie 2025-2026. We hadden besloten om een regenwater odrinatoor systeem te maken omdat het handig is om water te besparen.



Het werkt als volgt:


1. De code checkt meerdere dingen tegerlijkertijd, zoals zien of het droog wordt in de volgende 2 dagen, of het tijd is om de plantjes water te geven.

2. De code kijkt of er genoeg water in de tank is doormiddel van een echo geluid afstands-meter, op basis van dat maakt het een beslissing of het de water zal planten of niet, als er teveel water in de tank zit, dan dumpt het het in de riolen.

3. De code checkt ook of er heel veel percipitatie aankomt in de volgende 2 dagen (van >20mm/uur of hoger), als dat zo is, dan dumpt het al het water naar de riolen om zodra het regent, nieuwe water te ontvangen.
De code houd er ook rekening mee om de plantjes niet te veel water te geven omdat dat niet gezond voor hun is.

ENGLISH

Hello! This is our code for the 'Raspberry Pi competitie 2025-2026'. We decided to make a rainwater management system as it is handy for saving water.



Here’s how it works:


1. The code checks several things at once, such as whether it will be dry over the next two days, or whether it’s time to water the plants.

2. The code checks if there is enough water in the tank using an ultrasonic distance sensor; based on that, it decides whether to water the plants or not. If there is too much water in the tank, it drains it into the sewer.

3. The code also checks if a significant amount of precipitation is expected in the next 2 days (20 mm/hour or higher). If so, it drains all the water into the sewer so that it can receive fresh water as soon as it rains.
The code also takes care not to overwater the plants, as this is unhealthy for them.
