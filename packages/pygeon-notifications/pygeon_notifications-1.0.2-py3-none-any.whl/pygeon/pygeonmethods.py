import requests
import sys
import argparse
import os


class Pygeon:
    
    def __init__(self, ppk, context=None):
        """Main class for creating a Pygeon object with methods to trigger push notifications

        :param ppk: Your pygeon private key
        :type ppk: string
        :param context: reference string to use as a convenience to identify caller script that shows up in notifications, defaults to None
        :type context: string, optional
        """
        
        self.ppk = ppk
        self.context = context
        self.server_url = "https://pygeon.io/api/alert"
        
    def send(self, title, desc=None):
        """method to send push notification to your devices

        :param title: Title of the push notification
        :type title: string
        :param desc: Description of the push notification, defaults to None
        :type desc: string, optional
        :return: response tuple containing success status and response text
        :rtype: (bool, string)
        """
        

        if desc and self.context:
            data = {"ppk": self.ppk, "title": title, "desc": desc, "context": self.context}
        elif desc:
            data = {"ppk": self.ppk, "title": title, "desc": desc}
        elif self.context:
            data = {"ppk": self.ppk, "title": title, "context": self.context}
        else:
            data = {"ppk": self.ppk, "title": title}
        
        res = requests.post(self.server_url, json = data)
        print(res.text)
        return res.status_code==200, res.text


def _cli_alert():
    parser = argparse.ArgumentParser(description='Pygeon CLI tool to send alerts to your phone. Make sure to run pygeon-init with your private key before use. Checkout https://pygeon.io for full documentation')
    parser.add_argument('-title', type=str,
                    help='Title of the alert', required=True)
    parser.add_argument('-body', type=str, default=None,
                    help='Optional body of the alert, maximum 200 characters')
    args = parser.parse_args()
    ppk = open(os.path.join(os.path.expanduser('~'), ".pygeon/pygeon.conf")).read().split('\n')[0]
    alerts = Pygeon(ppk)
    body = args.body[:200] if args.body else None
    alerts.send(args.title, body)
    

def _cli_init():
    parser = argparse.ArgumentParser(description='Tool to initialize Pygeon with a private key')
    parser.add_argument('private_key', type=str,
                    help='Pygeon private key')
    args = parser.parse_args()
    conf_dir = os.path.join(os.path.expanduser('~'), ".pygeon")
    os.makedirs(conf_dir, exist_ok=True)
    with open(os.path.join(conf_dir, "pygeon.conf"), "w") as f:
        f.write(f"{args.private_key}\n")
    print(f"Private key successfully stored in {conf_dir}")
    



if __name__ == "__main__":
    my = Pygeon("YOUR_PRIVATE_KEY", context="Cool Context")
    my.send(f"Cool Title", "Cooler body")