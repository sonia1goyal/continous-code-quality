import requests
import pandas as pd


def get_data():
    # Read all the public project on github
    df = pd.read_csv('../data/travis_data.csv')

    """
        Filter data for github python projects
    """

    project_keys = df['project_url']
    project_keys = project_keys.unique()
    print(len(project_keys))

    payload = {}
    headers = {
        'Travis-API-Version': '3',
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.travis-ci.2.1+json',
        'User-Agent': 'Core3Client/1.0.0',
        'Authorization': 'token qf00G3R2sgd2tqzE_wy_2A'
    }

    ls = []
    for project_key in project_keys:
        print(project_key)
        slug = project_key.split("/")[-2] + "%2F" + project_key.split("/")[-1]
        url = 'https://api.travis-ci.com/repo/' + str(slug) + '/builds?limit=20'
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()

        if response['@type'] == 'error':
            continue
        else:
            builds = response['builds']
            print(builds)
            for i in builds:
                dict1 = {}
                dict1['project_url'] = project_key
                dict1['id'] = i['id']
                dict1['state'] = i['state']
                dict1['started_at'] = i['started_at']
                dict1['finished_at'] = i['finished_at']
                dict1['commit_id'] = i['commit']['id']
                dict1['commit_message'] = i['commit']['message']

                ls.append(dict1)
        # except Exception as e:
        #     continue

    df = pd.DataFrame(ls)
    print(df.head())

    df.to_csv('../data/travis_data_1.csv', index=False, header=True)


if __name__ == '__main__':
    get_data()
