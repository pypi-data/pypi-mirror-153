import argparse
import os

from sysflow.utils.common_utils.file_utils import dump, is_empty, load
import ruamel.yaml

import smtplib
import ssl

# email service
port = 587  # For SSL
smtp_server = "smtp.gmail.com"

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
user_config = os.path.join(BASE_DIR, "email_user.yaml")


def send_mail(message):
    try: 
        _send_mail(message)
    except Exception as e:
        print('allow the access here: https://www.google.com/settings/security/lesssecureapps. And read more here: https://stackoverflow.com/questions/16512592/login-credentials-not-working-with-gmail-smtp')
    
def _send_mail(message):
    info_dict = load_info()
    sender_email = info_dict['email']  # Enter your address
    receiver_email = info_dict['email']  # Enter receiver address
    password = info_dict['key']

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    print(message)
    print()

def load_info():
    try: 
        user_args_dict = load(user_config)
        return user_args_dict
    except: 
        assert False, "no email configuration found, please run smail config: `smail config --email <email> --key <key>` "
        
def status(args=None):
    print()
    print('the current email configuration: ')
    user_args_dict = load_info()
    res = ''.join(ruamel.yaml.round_trip_dump(user_args_dict, indent=5, block_seq_indent=3).splitlines(True))
    print(res)

def config(args=None):
    parser = argparse.ArgumentParser(
        prog="smail config",
        description="personalize configurations for the email.",
        argument_default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--email", type=str, help="the email to notify when the jobs are finished"
    )
    parser.add_argument(
        "--key", type=str, help="the password to the email account"
    )
    args = parser.parse_args(args)

    args_dict = vars(args)
    
    dump(args_dict, user_config)
    status()

    
def main(args=None):
    parser = argparse.ArgumentParser(
        prog="smail", description="A program to generate email command lines."
    )
    parser.add_argument(
        "command",
        help="specify the sub-command to run, possible choices: config",
    )
    parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="arguments to be passed to the sub-command",
    )

    args = parser.parse_args(args)

    # sepatate all sub_command to make them useable independently
    if args.command.upper() == "CONFIG":
        sub_command = config
    elif args.command.upper() == "STATUS":
        sub_command = status
    else:
        return ValueError(f"unsupported sub-command: {args.command}")

    sub_command(args.args)

if __name__ == "__main__":
    main()


