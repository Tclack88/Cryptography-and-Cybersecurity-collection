description: I asked ChatGPT to help me vibe code an app to hide my flags and it told me I was totally secure. Maybe help double check?

This opened an instance of a website. I inspected it and didn't see anything "dumb and obvious" like the flag in the comments. Just for fun I tried curl from the command line to see if anything was in the header info. Nothing, but I did notice at the very end of the curl operation this:

```html
        </div>
      </main>
    </div>

    <script src="/static/secret.js"></script>
  </body>
```
So I went to the url and added `/static/secret.js` and voila there it was


`SVIBGR{@lwAys_Ch3ck_Th3_S0urc3s`


