# the goal of this was to put the output of ./hack to /the and /planet
# simulatneously. Process substitution helps there
# tee defaults to stdout and another file. But with process substitution,
# everything is treated as a file
# eg. ls -1 | tee >(wc -l)  This would list everything (each item on one lint) 
# then it would put that to wc -l which itself would also print

/challenge/hack | tee >(/challenge/the) >(/challenge/planet)
