#!/bin/sh

# Server ssh addresses in the form user@address.
TASK_ADDRS=("ubuntu@ec2-54-183-196-119.us-west-1.compute.amazonaws.com" "ubuntu@ec2-13-52-220-64.us-west-1.compute.amazonaws.com" "ubuntu@ec2-18-144-90-156.us-west-1.compute.amazonaws.com")

ASSIGNER_ADDR="ubuntu@ec2-13-52-254-255.us-west-1.compute.amazonaws.com"

DISTRIBUTOR_ADDR="ubuntu@ec2-54-183-226-148.us-west-1.compute.amazonaws.com"

CLIENT_ADDR="ubuntu@ec2-13-57-229-155.us-west-1.compute.amazonaws.com"

# Launch task servers.
for i in "${TASK_ADDRS[@]}"
do
    cat launch-scripts/task.sh | ssh $i &
done

# Launch assigner.
cat launch-scripts/assigner.sh | ssh $ASSIGNER_ADDR &

# Launch distributor.
cat launch-scripts/distributor.sh | ssh $DISTRIBUTOR_ADDR &

# Launch client.
cat launch-scripts/client.sh | ssh $CLIENT_ADDR &

wait
