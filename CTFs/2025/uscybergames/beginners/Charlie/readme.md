# Charlie (forensics)
A picture is provided. I haven't done any stegonography before this, so I've had to learn how information could probably by hidden

## contents
	* charlie.jpg
	* failed_attempts/ -- just my initial gueses
		* somehex.py -- a weird attempt to find "hex shifted" strings
		* stegbrute -- downloaded this program to bruteforce a password
	
	* _charlie.jpg-0.extracted/ -- extracted from binwalk

## attempts and solution

Of course I tried using strings and exiftool to see any metadata or obvious things. Then I thought perhaps the strings were present but shifted because that's a way to evade a strings command. So I wrote a `somehex.py` that would shift it between -50 to +50. I only focused on the top because most of the other stuff I assumed would make up the image.

Finally, I researched and came across something called binwalk. I used it and it gave the `_charlie.jpg-0.extracted/` folder included which also has a `flag.txt` The contents of this is however still a mess, not just plaintext:

`/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQE .......... Nj+zle/AX/hQLfE/7VNcfGgfFv8AtMfFP/hGtwVv+EU8FYI/4R0HJDn5iPujbQB//9k=` over 70,000 characters of this. However, it's clearly base64

`cat flag | base64 -d | less` Also seemed superficially to churn out binary nonsense. But I decided to pipe it to a file

```
$ cat flag.txt | base64 -d > output

$ file output
output: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, baseline, precision 8, 1000x1000, components 3
```

Great! It's a JPEG, so it can just be viewed in a file explorer (after a name change). It's just a picture of the flag as text (`SBVGR{B1NW4LK_F7N}`)
