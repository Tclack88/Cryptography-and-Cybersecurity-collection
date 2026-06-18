description: Dimitrios & Shalin

inspecting the source code we see a comment:

 ```
 TODO: ClippyGPT devs — use 'cl1ppy123!!!' as signing key and change ai_mode to 'debug' for internal testing. Remove before prod!
 ```

First thought was to enter those into the chat `!ai_mode=debug` or `!get_flag cl1ppy123!!!` But these weren't working, only the valid commands were accepted.

Then I went to cookies and saw this session id:

`clippygpt_session:"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoidXNlciIsImFpX21vZGUiOiJzYWZlIn0.ik848j8GI-XTLZZNtKDQMXUI9DQozVfpW-P9s9JxqYw"`

I checked just to see if it was base64 and it was! The decoded value read:

`{"alg":"HS256","typ":"JWT"}{"role":"user","ai_mode":"safe"}"<tem(4]B=3UVljc`

So I changed it to:

`{"alg":"HS256","typ":"JWT"}{"role":"user","ai_mode":"debug	"}"<tem(4]B=3UVljc`

But then was met with an error that it has been tampered with. I tried changing `<tem(4]B=3UVljc` to `cl1ppy123!!!`, role to dev , no change. Then I noticed that thing at the front `{"alg":"HS256","typ":"JWT"}` and researched online and found this site:

[jwtsecrets](https://jwtsecrets.com/blog/hs256-vs-rs256-jwt-algorithm)

Fortunately it wasn't a "jehovah's witness" secrets or anything, it's a signing algorithm of some sort which is where the connection to the signing key note was. I searched again online for how to sign this [medium blog](https://adityaprakash-2811.medium.com/encryption-series-part-3-symmetric-signing-with-hs256-jwts-a3e218e7650b)

The relevant information was this:
```
pip install PyJWT

import jwt
secret = "supersecret123"
token = jwt.encode({"user": "alice"}, secret, algorithm="HS256")
```

So I changed "user" to "dev" and added the `ai_mode=debug`. This allowed me to see the `debug_stats`, but `!get_flag` informed me I needed the role of admin. Changing "user" to admin didn't work for me, so I changed it to "role"

```python
import jwt
secret = "cl1ppy123!!!"
token = jwt.encode({"role": "admin","ai_mode":"debug"}, secret, algorithm="HS256")
decoded = jwt.decode(token, secret, algorithms=["HS256"])
```

printed out this: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4iLCJhaV9tb2RlIjoiZGVidWcifQ.fnnbmKHlUcWEwWc2NK5ENIX6O1RfEjBfGJjhe_mAa1I` which after replacing the cooking with this finally gave the flag:

`SVIBGR{jw7_4i_7rus7_issu3}`

