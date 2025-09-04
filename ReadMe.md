### Simplifications & Shortcomings
- Longitude/Langitude Coordinates are not directly transformed to meters
  - Distance calculation between dest and orig with manhattan distance is normaly curved
  - Sampling between the grid is also curved, but assume enough locality as the curve is not to strong.