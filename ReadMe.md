# How far away is the next 7-Eleven in Bangkok?
Link to the blog post: https://frederikroeckle.com/blog/posts/7-Eleven-Monte-Carlo/

This small fun project came to me on my last vacation to Thailand. Almost everywhere you can spot a 7-Eleven in Bangkok!

I wanted to get a more analytical answer on how many stores there might are and how long it would take you on average to find the next one.

This project tries to find some answers on these simple questions. The project has some more or less severe limitations which makes the actual results more a rule of thumb than a precise answer.
  1. Get all 7-Eleven stores in Bangkok
  2. Run a Monte Carlo (MC) simulation to estimate the average distance to the next 7-Eleven

In my somehow arbitrary defined area of Bangkok there are 988 7-Eleven stores and on average the next 7-Eleven is 193.5m away!  

### Simplifications, Shortcomings and Limitations
  - Longitude/Langitude Coordinates are not directly transformable to meters
  - The majority of the distance calculations are based on the Haversine Formulation which is conceptually closer to the shortest line of the L2 distance then to the L1 distance. However, the later one would be more sufficient for this scenario.
  - Risk for undersampling and miss of 7-Eleven stores
  - No measurement on the convergence criteria of the MC simulation - 193.5m after 2e7 sample points

### Ideas
- [ ] Analyze area where there is a low density of 7-Eleven stores
- [ ] Find the most far closest point to a 7-Eleven
- [ ] Calculate convergence criterias and increase sample size for MC simulation
