import boto3
import click

ec2 = boto3.resource('ec2')

def filter_instances(test):
    instances = []

    if test:
        filters = [{'Name':'tag:TEST', 'Values':["DEVP_VM_AM_ML_SPRINT"]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        #instances = ec2.instances.all()
        print("No action - DUMMY Message")
    return instances

@click.group()
def instances():
    """Command for instances"""

@instances.command('list')
@click.option('--test', default=None,
    help="Only instances for project (tag ProjectL<name>)")
def list_instances(test):
        "List the EC2 Instances"

        instances = filter_instances(test)

        for i in instances:
            tags = { t['Key']: t['Value'] for t in i.tags or []}
            print(', '.join((
                i.id,
                i.instance_type,
                i.placement['AvailabilityZone'],
                i.state['Name'],
                i.instance_id,
                i.image_id,
                i.public_dns_name,
                tags.get('Name', '<no project>'))))
        #running_instances()
        return

def running_instances():
    instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        print(instance.id, instance.instance_type)



@instances.command('start')
@click.option('--test', default=None,
    help='Only instances for Test prefix')
def stop_instances(test):
    "Start EC2 instances"

    instances = filter_instances(test)

    for i in instances:
        print("Starting {0} ....".format(i.id))
        i.start()

    return



@instances.command('stop')
@click.option('--test', default=None,
    help='Only instances for Test prefix')
def stop_instances(test):
    "Stop EC2 instances"

    instances = filter_instances(test)

    for i in instances:
        print("Stopping {0} ....".format(i.id))
        i.stop()

    return



if __name__ == "__main__":
    instances()
