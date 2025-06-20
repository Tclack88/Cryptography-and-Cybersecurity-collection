The image is of Chad from nickelback. Suspecting it's a steghide, we can grep rockyou.txt for all references to nickelback

`cat rockyou.txt | grep "nickelback" > nb.txt

In general steghide extraction on an image looks like this:

`steghide extract -sf lookatthis.jpg`, then you're prompted for a password

Or a one liner with bash for loop:

`for pass in $(cat nb.txt); do steghide extract -sf lookatthis.jpg -p $pass; done`

(note, this would split on whitespace if it exists, not a problem here, but it's not as general)

A more general approach:

``` bash
while IFS= read -r pass; do
  echo "password: $pass"
done < nb.txt
```
