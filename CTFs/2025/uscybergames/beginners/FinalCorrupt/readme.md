# Final Corrupt
A single (corrupt) zip file is provided:

`FinalCorruptZip.zip`

NOTE: I solved this and to my disappointment was about 4 minutes past the deadline. (Otherwise I would have gotten 1100 points and been boosted up to 142nd place, practically grazing the frontlines)

## contents

* `FinalCorruptZip.zip` -- the original unedited file
* solution -- a directory where the repair and unzipping can occur

(An unedited version is provded in the  directory)

## Solution

```
$ file FinalCorruptZip.zip
FinalCorruptZip.zip: Zip archive data, made by v2.0 UNIX, extract using at least v2.0, last modified Wed Mar 21 18:11:21 2018, uncompressed size 13239, method=deflate
```

Nothing seems correupt about this so trying to unzip it:

```
t$ un
zip FinalCorruptZip.zip
Archive:  FinalCorruptZip.zip
file #1:  bad zipfile offset (local header sig):  0
```

Okay, certainly a problem

A few attempts with like binwalk proved nothing. After some deliberation, I checked out the magic bytes of a zip folder on [Wikipedia](https://en.wikipedia.org/wiki/List_of_file_signatures), there are a few conventions

```
1F 9D 	␟□ 	0 	z
tar.z 	compressed file (often tar zip) using Lempel-Ziv-Welch algorithm

1F A0 	␟⍽ 	0 	z
tar.z 	Compressed file (often tar zip) using LZH algorithm

50 4B 03 04
50 4B 05 06 (empty archive)
50 4B 07 08 (spanned archive) 	
```

Opening with hexedit:

```
00000000   41 4B 03 04  14 00 08 00  08 00 49 A0  AK........I.
0000000C   B2 5A 00 00  00 00 00 00  00 00 00 00  .Z..........
00000018   00 00 0E 00  20 00 43 6F  72 72 75 70  .... .Corrup
00000024   74 50 4E 47  2E 70 6E 67  75 78 0B 00  tPNG.pngux..
.
.
.
```

Clearly the `41 4B 03 04` is nearly identical to  `50 4B 03 04` So changing that just by typing it in and hitting `<ctrl-x>` to save and quit (it doesn't use a vim-like interface :/  )

No problem unzipping now

```
$ unzip FinalCorruptZip.zip
Archive:  FinalCorruptZip.zip
inflating: CorruptPNG.png

$ file CorruptPNG.png
CorruptPNG.png: data
```

Another corrput file, the same wikipedia link shows PNG magic bytes. But there's only one `89 50 4E 47 0D 0A 1A 0A`

Opening with hexidit the top shows that some one changed the middle bytes to `LOL`,(`89 4C 4F 4C  0D 0A`)  what a silly goose.

```
00000000   89 4C 4F 4C  0D 0A 1A 0A  00 00 00 0D  .LOL........
0000000C   49 48 44 52  00 00 03 B0  00 00 01 A2  IHDR........
```

After repairing, it's simply an image of the flag

`SVBGR{m4g1C_B1t3s_yUmmmmm}`
