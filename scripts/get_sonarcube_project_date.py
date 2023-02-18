import requests
import pandas as pd


def get_data():
    df_travis = pd.read_csv('../data/travis_data.csv')
    df_sonarcube = pd.read_csv('../data/sonarcube_data_with_repo_link.csv')
    df = pd.merge(df_travis, df_sonarcube, on='project_url', how='inner')

    project_keys = df['project_key']
    project_keys = project_keys.unique()
    print(len(project_keys))

    ls = []
    for project_key in project_keys:
        url = 'https://sonarcloud.io/api/project_analyses/search?project=' + str(
            project_key) + '&ps=20&category=QUALITY_PROFILE'
        response = requests.request("GET", url)
        response = response.json()
        if 'errors' in response:
            continue
        else:
            analyses = response['analyses']
            dates = []
            key_dates = {}
            for dt in analyses:
                ls.append((project_key, dt['date']))

    df1 = pd.DataFrame(ls, columns=['project_key', 'quality_profile_date'])
    final_df = pd.merge(df, df1, on='project_key', how='inner')
    final_df.to_csv('../data/sonar_quality_profile.csv', index=False, header=True)


if __name__ == '__main__':
    get_data()
