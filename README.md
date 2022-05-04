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
Arriving shuttles:
1636'er in 3-4 min
crimson cruiser in 10 min
quad sec express in 22 min
 
