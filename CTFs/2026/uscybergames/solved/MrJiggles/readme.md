Description:
Mr Jiggles my pet cat ran away and when I put up flyers this was the photo I used. I feel it really captures his catty essence. Regardless, I think it would have been helpful if I had been able to extract data about him and maybe learn more about his whereabouts. (He came home 2 weeks ago don’t worry)


First I tried the `strings` command and grepped for `BGR` or `flag` with no luck. Then I looked at the output of `file`. Then I looked at more metat data using `exiftool` and saw this interesting comment:

```
.
.
.
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
Comment                         : U1ZJQlJHe1kwdV9GMHVuRF9Ncl9KMUdnTDMkIX0=
Exif Byte Order                 : Big-endian (Motorola, MM)
Orientation                     : Horizontal (normal)
X Resolution                    : 72
Y Resolution                    : 72
Resolution Unit                 : inches
.
.
.
```

Clearly a base64 encoded string

`echo U1ZJQlJHe1kwdV9GMHVuRF9Ncl9KMUdnTDMkIX0= | base64 -d` gives the result:

`SVIBRG{Y0u_F0unD_Mr_J1GgL3$!}`
