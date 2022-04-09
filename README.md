# shuttleWYA
Textbot built with Python, Flask and Twilio for Harvard students to get shuttle updates without having to use Passio Go!

The flask webapp will interpret input recieved at the Twilio number. I will use the Beautiful Soup module to scrape http://shuttle.harvard.edu/ and get relevant live shuttle updates to send to the user via text.

Desired functionality is allowing users to text the bot one fo the following shuttle stops:
- memorial / mem drive / memorial drive / 784 memorial drive (+ other aliases)
- widener / widener gate
- mather / mather house
- inn / the Inn
- maxwell dworkin / maxwell / dworkin / md
- science center / sci center / sc (+ other aliases)
- memorial hall / mem hall
- lamont / lamont library
- lev / leverett / leverett house
- quad / quadrangle / radcliffe quadrangle (+ other aliases)
- sec (+ other aliases)
- etc.

Example output from bot:
"1. 1636'er in 3-4 min
 2. crimson cruiser in 10 min
 3. quad/sec express in 22 min
 Respond with 1, 2, or 3 to get a 5 min and 2 min warning for shuttle arrival"

Current state:
- Twilio phone number set up and tested
- basic flask code set up

TODO:
- web scrapping functionality
- 5 min + 2 min warning code
- testing