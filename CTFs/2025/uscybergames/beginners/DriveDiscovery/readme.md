# DriveDiscovery (forensics)
A single zip file is provided

## solution
```
$ unzip drivediscovery.zip
Archive:  drivediscovery.zip
  inflating: DriveDiscoveryDescriptionPUBLIC.txt
  inflating: nothinginterestinghere.001

$ cat DriveDiscoveryDescriptionPUBLIC.txt
We took an image of a suspicious USB drive - can you investigate it in more detail?
We think the user may have tried to cover their tracks.
```

I called strings on the `nothinginterestinghere.001` object but didn't bother to search it thoroughly. Instead I went down a rabbit hole of trying to repair a corrupted disk, learning the sleuthtoolkit along the way (great introduction in the picoPrimer) as wella s [this video](https://www.youtube.com/watch?v=R-IE2j04Chc) by DFIRScience. I will note it down for future forensics learnign. 

But I went back later and did strings again and focused on larger strings at least 10 in length (`strings nothinginterestinghere.001 -n 10 | less`) and actually read through it to find there was a base64 encoded string. 

```
/pub/images/red_herring1.png
HostUrl=https://static.tvtropes.org/pmwiki/pub/images/red_herring1.png
1. Make sure to delete flag.txt before giving this USB drive to anyone.
2. Apparently there's a really secure type of encryption called Base64, I should look into using that.
U1ZCUkd7ZDNsMzczZF9uMDdfZjByNjA3NzNuXzI4MzAyOTM4Mn0=
:?mG^z:;=8
T&vmr|:#>-(
Q6s\Y[&$dx
%tEXtdate:create
2018-03-09T15:51:05-08:00
%tEXtdate:modify
2018-03-09T15:51:05-08:00
tEXtSoftware
Adobe ImageReadyq
A disk read error occurred
BOOTMGR is compressed
```

```
$ echo "U1ZCUkd7ZDNsMzczZF9uMDdfZjByNjA3NzNuXzI4MzAyOTM4Mn0=" | base64 -d
SVBRG{d3l373d_n07_f0r60773n_283029382}
```

The "deleted" reference makes me think there was another solution that did indeed involve disk forensics, but this suffices
