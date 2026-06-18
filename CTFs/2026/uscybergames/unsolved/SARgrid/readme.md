Description:

```
We found some route data from a SAR grid system. Each route state is a 2x2 matrix mod n.

The docs say encryption is just a secret change of coordinates:

C = A^-1 M A mod n
The archive has a few training routes where both the original matrix and the encrypted matrix are known. The live route is split into encrypted matrices.

Recover the live route and read out the flag.
```
