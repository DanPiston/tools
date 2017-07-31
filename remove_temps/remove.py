import argparse
import requests 

'''This tool is to remove all custom templates from within an account.  It must be passed the AID of the customer when running the module'''

parser = argparse.ArgumentParser()
parser.add_argument('aid')
args = parser.parse_args()
aid = args.aid
headers = {'Content-Type': 'application/json', 'x-aweber-customer-id': aid}

#get list of templates in account
def get_temps(aid):
    templates_url = 'http://messageeditor-api1.lbl.csh/message-editor/v1/accounts/{}/templates'.format(aid)
    r = requests.get(templates_url, headers=headers)
    content = r.json()['content']
    temps = []
    for temp in content:
        temps.append(temp['_id'])
    return temps

#delete list of custom templates
def delete_temp(list_of_temps):
    for temp_id in list_of_temps:
        delete_url = 'http://messageeditor-api1.lbl.csh/message-editor/v1/accounts/{}/templates/{}'.format(aid, temp_id)
        r = requests.delete(delete_url, headers=headers)
        print(r.status_code)


def main():
    print('Started with {}'.format(len(get_temps(aid))))
    delete_temp(get_temps(aid))
    print('Ended with {}'.format(len(get_temps(aid))))

if __name__ == '__main__':
    main()


