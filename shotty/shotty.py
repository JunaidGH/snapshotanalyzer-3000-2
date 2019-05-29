import boto3
#import sys
import click

#session = boto3.Session(profile_name='DEV6888', region_name='eu-west-1')
#ec2 = session.resource('ec2')
ec2 = boto3.resource('ec2')

@click.command()
#@click.option('--project', default=None,
#    help="Only instanaces for project (tag ProjectL<name>)")
def list_instances():
    for i in ec2.instances.all():
        "List the EC2 Instances"
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.instance_id,
            i.image_id,
            i.public_dns_name)))
    running_instances()
    return

def running_instances():
    instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        print(instance.id, instance.instance_type)

if __name__ == "__main__":
    #print(sys.argv)
    list_instances()
    #running_instances()
