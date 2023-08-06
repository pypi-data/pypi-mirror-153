#!/bin/sh
#runuser -l  pi -c "jupyter notebook --notebook-dir='$1' &"
su - pi -c "jupyter notebook --notebook-dir='$1' &"