#!/bin/sh

# Server ssh addresses in the form user@address.
TASK_ADDRS=("ubuntu@ec2-54-241-208-105.us-west-1.compute.amazonaws.com" "ubuntu@ec2-18-144-148-168.us-west-1.compute.amazonaws.com" "ubuntu@ec2-52-9-0-84.us-west-1.compute.amazonaws.com")

ASSIGNER_ADDR="ec2-184-169-220-191.us-west-1.compute.amazonaws.com"

CLIENT_ADDR="ec2-52-9-194-232.us-west-1.compute.amazonaws.com"

# Launch task servers.
for i in "${TASK_ADDRS[@]}"
do
    cat launch-scripts/task.sh | ssh $i > /dev/null 2>&1
done

# Launch assigner.
cat launch-scripts/assigner.sh | ssh $ASSIGNER_ADDR > /dev/null 2>&1

# Launch client.
cat launch-scripts/client.sh | ssh $CLIENT_ADDR > /dev/null 2>&1

echo "Successfully (re)launched slicer."
