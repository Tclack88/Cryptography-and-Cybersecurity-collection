# this the output of ./hack has a stdout and stderr. Here we were supposed
# to pip the output of stderr to "the" and stdout to "planet
# I think I did this in a different way than intended
/challenge/hack  > >(/challenge/planet) 2> >(/challenge/the)

# Asking an AI, this was suggested:
#
# /challenge/hack  > >(cat > /challenge/planet) 2> >(cat > /challenge/the)
# with or without  ^this first ">" (with is more explicit)
# I asked whether or not it could be done with tee and it raised a valid point
# namelt, tee only deals with stdout
