# PYTHON_ARGCOMPLETE_OK

# Copyright 2020 Cognicept Systems
# Author: Jakub Tomasek (jakub@cognicept.systems)
# --> Main executable file to handle input arguments

import argparse
import argcomplete
import pkg_resources
from cogniceptshell.configuration import Configuration
local_cfg = Configuration()

container_names = []
if(local_cfg.load_config("~/.cognicept/")):
    container_names = local_cfg.config["COG_AGENT_CONTAINERS"].split(";")
    container_names.append([])
else:
    container_names = ["remote_intervention_agent", "kriya_watchdog", "cgs_diagnostics_agent", "cgs_diagnostics_ecs_api", "cgs_diagnostics_streamer_api", "cgs_bagger_server"]

parser = argparse.ArgumentParser(
        description='Shell utility to configure Cognicept tools.')

parser.add_argument('--version', action='version',
                    version=pkg_resources.require("cognicept-shell")[0].version)

subparsers = parser.add_subparsers(help='', title="Commands")

parser_version = subparsers.add_parser(
    'version', help='Display Cognicept Version')
parser_config = subparsers.add_parser(
    'config', help='Configure Cognicept tools')
parser_status = subparsers.add_parser(
    'status', help='Get status of Cognicept agents')
parser_lastevent = subparsers.add_parser(
    'lastevent', help='Display last event log reported by Cognicept agent')
parser_update = subparsers.add_parser(
    'update', help='Update Cognicept tools')
parser_keyrotate = subparsers.add_parser(
    'keyrotate', help='Rotate Cognicept cloud keys')
parser_restart = subparsers.add_parser(
    'restart', help='Restart Cognicept agents')
parser_start = subparsers.add_parser(
    'start', help='Start Cognicept agents')
parser_stop = subparsers.add_parser('stop', help='Stops Cognicept agents')
parser_orbitty = subparsers.add_parser('orbitty', help='Run Orbitty')
parser_record = subparsers.add_parser(
    'record', help='Manages rosbag recording')
parser_push = subparsers.add_parser(
    'push', help='Pushes stuff to Cognicept cloud')
parser_init = subparsers.add_parser(
    'init', help='Initiate runtime.env')


DEFAULT_PATH = "~/.cognicept/"

parser_version.add_argument(
    '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)
parser_config.add_argument(
    '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)
parser_config.add_argument(
    '--add', help='Add new environmental variable in config file', action='store_true')
parser_config.add_argument(
    '--ssh', help='Configure ssh access during remote intervention', action='store_true')
parser_config.add_argument(
    '--autocomplete', help='Setup autocomplete of cognicept', action='store_true')

parser_config.add_argument(
    '--read', help='Prints Cognicept configuration', action='store_true')


parser_keyrotate.add_argument(
    '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)

parser_status.add_argument(
    '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)

parser_lastevent.add_argument(
    '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)


parser_restart.add_argument('-d', '--detach', action='store_true',
                            help='sets restart to be run in a detached manner. Progress will not be printed')
parser_restart.add_argument(
    '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)
parser_restart.add_argument(
    'list', help='List of agents to restart, leave empty to restart all agents', metavar='list', type=str, nargs='*',choices=container_names)

parser_start.add_argument(
    '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)
parser_start.add_argument(
    'list', help='List of agents to start, leave empty to start all agents', metavar='list', type=str, nargs='*',choices=container_names)


parser_stop.add_argument(
    '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)
parser_stop.add_argument(
    'list', help='List of agents to stop, leave empty to stop all agents', metavar='list', type=str, nargs='*',choices=container_names)

parser_update.add_argument(
    '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)
parser_update.add_argument(
    '--reset', help='Triggers new login before update', action='store_true')
parser_update.add_argument("-d", "--detach", help="Runs update in detached mode", action="store_true")

parser_orbitty.add_argument(
    '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)



parser_record.add_argument(
    '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)
parser_record.add_argument(
    '--start',
    help='Start rosbag recording session. Provide topics to record separated by spaces with their `/` prefix. e.g. cognicept record --start /rosout /odom',
    nargs='+')
parser_record.add_argument(
    '--all', help='Start rosbag recording session to record ALL topics.', action='store_true')
parser_record.add_argument(
    '--stop',
    help='Stop rosbag recording session. Set `STOP` to `autopush` to automatically push latest bag to the Cognicept cloud after stopping',
    type=str, const='nopush', nargs='?')
parser_record.add_argument(
    '--pause', help='Pause rosbag recording session', action='store_true')
parser_record.add_argument(
    '--resume', help='Resume rosbag recording session', action='store_true')
parser_record.add_argument(
    '--status', help='Get current recording session status', action='store_true')


parser_push.add_argument(
    '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)
parser_push.add_argument(
    '--bag',
    help='Pushes rosbag to the Cognicept cloud. By default it pushes the latest bag file recording. Set `BAG` to appropriate bag name in the `PATH` folder to upload a rosbag by name',
    type=str, const='latest', nargs='?')


parser_init.add_argument(
    '--path', default=DEFAULT_PATH)
parser_init.add_argument(
    '--robot_id', help='Input the robot ID', required=True)
parser_init.add_argument(
    '--org_id', help='Input the organisation ID', required=True)    

argcomplete.autocomplete(parser)

from cogniceptshell.agent_life_cycle import AgentLifeCycle
from cogniceptshell.rosbag_record import RosbagRecord
from cogniceptshell.pusher import Pusher

parser_config.set_defaults(func=local_cfg.configure)
parser_keyrotate.set_defaults(func=local_cfg.cognicept_key_rotate)
agent_lifetime = AgentLifeCycle()
parser_version.set_defaults(func=agent_lifetime.display_version)
parser_status.set_defaults(func=agent_lifetime.status)
parser_lastevent.set_defaults(func=agent_lifetime.get_last_event)
parser_restart.set_defaults(func=agent_lifetime.restart)
parser_start.set_defaults(func=agent_lifetime.start)
parser_stop.set_defaults(func=agent_lifetime.stop)
parser_update.set_defaults(func=agent_lifetime.update)
parser_orbitty.set_defaults(func=agent_lifetime.run_orbitty)
record_session = RosbagRecord()
parser_record.set_defaults(func=record_session.record)
pusher_instance = Pusher()
parser_push.set_defaults(func=pusher_instance.push)
parser_init.set_defaults(func=local_cfg.init_config)

def main():

    # Parse the arguments
    args = parser.parse_args()

    if ("path" not in args):
        parser.print_help()
    else:
        local_cfg.load_config(args.path)
        agent_lifetime.configure_containers(local_cfg)
        args.config = local_cfg

        if (hasattr(args, 'func')):
            args.func(args)


if __name__ == "__main__":
    main()
