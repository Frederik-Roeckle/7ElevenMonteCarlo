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
