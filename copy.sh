
if [ "$1" = "train" ]
then
    scp -i ~/.ssh/pi_rsa \
    pi@raspberrypi.local:~/dumbbell/*.json \
    ./
    exit
fi



scp -i ~/.ssh/pi_rsa \
./*.py \
pi@raspberrypi.local:~/dumbbell/

if [ "$1" = "full" ]
then
    scp -i ~/.ssh/pi_rsa \
    -r ./ \
    pi@raspberrypi.local:~/dumbbell
fi

if [ "$1" = "run" ]
then
    ssh -i ~/.ssh/pi_rsa pi@raspberrypi.local "python ~/dumbbell/start.py"
    exit
fi

