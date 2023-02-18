import requests
import pandas as pd


def get_data():
    # Read data for all the projects
    df = pd.read_csv('../data/sonarcube_data_projects.csv')


    project_keys = df['key']
    project_keys = project_keys.unique()

    """
        Get project url and qualityProfiles for all the projects
    """
    batch = 500
    for i in range(7501, len(project_keys)+1, batch):
        proj_batch = project_keys[i:i+batch]
        ls = []
        for project_key in proj_batch:
            dict1 = {}
            url = 'https://sonarcloud.io/api/navigation/component?component=' + project_key

            response = requests.request("GET", url, headers={}, data={})
            response = response.json()
            dict1['project_key'] = project_key

            try:
                dict1['project_url'] = response['alm']['url']
                dict1['project_type'] = response['alm']['key']
            except KeyError:
                dict1['project_url'] = None
                dict1['project_type'] = None

            language_list = ''
            try:
                for qp in response['qualityProfiles']:
                    language_list = language_list + qp['language'] + '|'
                dict1['languages'] = language_list
            except KeyError:
                dict1['languages'] = language_list

            ls.append(dict1)


        """
            Write data to a csv
        """
        df1 = pd.DataFrame(ls)
        print(df1.head())
        df1.to_csv('sonarcube_data_with_repo_link.csv', index=False, mode='a', header=False)


if __name__ == '__main__':
    get_data()
