import uuid
import yaml
import argparse
import os


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTIONS] ...",
        description="Generate configuration files for Avista IoT",
        epilog="Copyright (C) 2020, 2021 Idaho State University Empirical SE Lab"
    )
    parser.add_argument("-t", "--dbtype", action="store", type=str, required=True, help="DBMS Type")
    parser.add_argument("-n", "--dbname", action="store", type=str, required=True, help="DBMS Name")
    parser.add_argument("-i", "--dbip", action="store", type=str, required=True, help="DBMS IP/Hostname")
    parser.add_argument("-o", "--dbport", action="store", type=str, required=True, help="DBMS Port")
    parser.add_argument("-p", "--dbpass", action="store", type=str, required=True, help="DBMS Password")
    parser.add_argument("-u", "--dbuser", action="store", type=str, required=True, help="DBMS Username")
    parser.add_argument("-s", "--hostname", action="store", type=str, required=True, help="Server Host Name")
    parser.add_argument("-r", "--hostport", action="store", type=str, required=True, help="Server Host Port")
    parser.add_argument("-v", "--version", action="version", version=f'{parser.prog} version 1.0.0')

    return parser

def generate_logs_directory():
    if not os.path.isdir('logs'):
        os.mkdir('logs')
        open('logs/server.log', 'w').close()


def generate_server_config(dbtype, dbname, dbip, dbport, dbuser, dbpass, hostname, hostport):
    config = {
        'DBMS Type': dbtype,
        'DBMS Name': dbname,
        'DBMS IP Address': dbip,
        'DBMS Port': dbport,
        'DBMS Username': dbuser,
        'DBMS Password': dbpass,
        'Hostname': hostname,
        'Port': hostport,
    }

    with open('conf/config.yml', 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    dic = vars(args)

    dbtype = dic['dbtype']
    dbname = dic['dbname']
    dbip = dic['dbip']
    dbport = dic['dbport']
    dbpass = dic['dbpass']
    dbuser = dic['dbuser']
    host = dic['hostname']
    port = dic['hostport']

    generate_server_config(dbtype, dbname, dbip, dbport, dbuser, dbpass, host, port)
    generate_logs_directory()


if __name__ == '__main__':
    main()
