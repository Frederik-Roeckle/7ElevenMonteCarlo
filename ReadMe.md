### Google APIs
- https://developers.google.com/maps/documentation/geocoding/requests-reverse-geocoding
- https://developers.google.com/maps/documentation/places/web-service/nearby-search
- https://developers.google.com/maps/documentation/places/web-service/text-search
- https://developers.google.com/maps/documentation/places/web-service/place-types#shopping

### Simplifications & Shortcomings
- Longitude/Langitude Coordinates are not directly transformed to meters
  - Distance calculation between dest and orig with manhattan distance is normaly curved
  - Sampling between the grid is also curved, but assume enough locality as the curve is not to strong.
  - Used https://en.wikipedia.org/wiki/Haversine_formula

## Future Work
### Current Limitations
The majority of the distance calculations are based on the Haversine Formulation which is conceptually closer to the shortest line calculatio of the L2 norm. The L1 norm would be more sufficient for this scenario.
### Ideas
- [ ] Analyze area where there is a low density of 7-Eleven stores
- [ ] Find the most far closest point to a 7-Eleven
- [ ] Plot the map of Bangkok with the according sampled points
