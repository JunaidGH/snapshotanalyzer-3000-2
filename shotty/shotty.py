import boto3
import click
import botocore

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
def cli():
    """Shotty manages snapshots"""


@cli.group('snapshots')
def snapshots():
    """ Commands for Snapshots"""

@snapshots.command('list')
@click.option('--test', default=None,
    help="Only volumes for project (tag Test:<name>)")
@click.option('--all', 'list_all', default=False, is_flag=True,
    help="List all snapshots for each volume, not just the most recent")
def list_snapshots(test, list_all):
        "List EC2 Snapshots"

        instances = filter_instances(test)

        for i in instances:
            for v in i.volumes.all():
                for s in v.snapshots.all():
                    print(", ".join((
                        s.id,
                        v.id,
                        i.id,
                        s.state,
                        s.progress,
                        s.start_time.strftime("%c")
                    )))

                    if s.state == 'completed' and not list_all: break
        return

@cli.group('volumes')
def volumes():
    """ Commands for Volumes"""


@volumes.command('listv')
@click.option('--test', default=None,
    help="Only volumes for project (tag Test:<name>)")
def list_volumes(test):
        "List the EC2 Volumes"

        instances = filter_instances(test)

        for i in instances:
            for v in i.volumes.all():
                print(", ".join((
                    v.id,
                    i.id,
                    v.state,
                    str(v.size) + "GiB",
                    v.encrypted and "Encrypted" or "Not Encrypted"
                )))

        return

@cli.group('instances')
def instances():
    """Command for instances"""

@instances.command('snapshot',
    help="Create snapshots of all volumes")
@click.option('--test', default=None,
    help="Only instances for project (tag Test:<name>)")
def create_snapshots(test):
        "Create snapshot for EC2 instances"

        instances = filter_instances(test)

        for i in instances:
            print("Stopping {0}...".format(i.id))

            i.stop()
            i.wait_until_stopped()

            for v in i.volumes.all():
                print("Creating snapshot of {0}".format(v.id))
                v.create_snapshot(Description="Created by SnapShotTest")

            print("Starting {0} ...".format(i.id))

            i.start()
            i.wait_until_running()

        print("Job Done")

        return

@instances.command('list')
@click.option('--test', default=None,
    help="Only instances for project (tag Test:<name>)")
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
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print("Could not start {0}".format(i.id) + str(e))
            continue

    return

@instances.command('stop')
@click.option('--test', default=None,
    help='Only instances for Test prefix')
def stop_instances(test):
    "Stop EC2 instances"

    instances = filter_instances(test)

    for i in instances:
        print("Stopping {0} ....".format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print("Could not stop {0}".format(i.id) + str(e))
            continue

    return

if __name__ == "__main__":
    #instances()
    cli()
