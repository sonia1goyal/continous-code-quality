import requests
import pandas as pd


def get_data():
    # Read all the public project on github
    df = pd.read_csv('../data/sonarcube_data_with_repo_link.csv')

    """
        Filter data for github python projects
    """
    filtered_data = df.dropna()
    filtered_data = filtered_data[(filtered_data.project_type == "github")]
    filtered_data = filtered_data[filtered_data['languages'].str.contains("py", case=False, na=False)]
    print(filtered_data.head(20))
    print(filtered_data.shape)

    project_keys = filtered_data['project_key']
    project_keys = project_keys.unique()

    """
        Get metrics for projects -
        Metrics: 
            1. ncloc,
            2. complexity,
            3. violations,
            4. bugs,
            5. code_smells
    """
    ls = []
    for project_key in project_keys:
        dict1 = {}
        print(project_key)
        url = 'https://sonarcloud.io/api/measures/component?' \
              'component=' + str(project_key) + '&metricKeys=ncloc,complexity,violations,bugs,code_smells'

        response = requests.request("GET", url, headers={}, data={})
        response = response.json()
        try:
            measures = response['component']['measures']
            dict1['project_key'] = project_key
            for i in measures:
                if i['metric'] == 'complexity':
                    dict1['complexoty'] = i['value']
                elif i['metric'] == 'bugs':
                    dict1['bugs'] = i['value']
                elif i['metric'] == 'code_smells':
                    dict1['code_smell'] = i['value']
                elif i['metric'] == 'ncloc':
                    dict1['ncloc'] = i['value']
                elif i['metric'] == 'violations':
                    dict1['violations'] = i['value']
        except KeyError:
            continue

        ls.append(dict1)

    df1 = pd.DataFrame(ls)
    # print(df1.head())
    """
        Merge all data together in single csv file
    """
    df = pd.merge(filtered_data, df1, on=['project_key'])

    df.to_csv('sonarcube_data.csv', index=False, mode='a', header=True)


if __name__ == '__main__':
    get_data()
