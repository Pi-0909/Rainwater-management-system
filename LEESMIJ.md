Hallo! Dit is onze code voor de Raspberry-pi competitie 2025-2026. We hadden besloten om een regenwater odrinatoor systeem te maken omdat het handig is om water te besparen.



Het werkt als volgt:


1. De code checkt meerdere dingen tegerlijkertijd, zoals zien of het droog wordt in de volgende 2 dagen, of het tijd is om de plantjes water te geven.

2. De code kijkt of er genoeg water in de tank is doormiddel van een echo geluid afstands-meter, op basis van dat maakt het een beslissing of het de water zal planten of niet, als er teveel water in de tank zit, dan dumpt het het in de riolen.

3. De code checkt ook of er heel veel percipitatie aankomt in de volgende 2 dagen (van >20mm/uur of hoger), als dat zo is, dan dumpt het al het water naar de riolen om zodra het regent, nieuwe water te ontvangen.
De code houd er ook rekening mee om de plantjes niet te veel water te geven omdat dat niet gezond voor hun is.




Deze code is volledig open source en mag vrij worden gebruikt voor eigen doeleinden, inclusief het klonen, bewerken en eruit leren voor eigen gebruik.
