import pandas as pd
from datetime import datetime


def get_metrics():
    df_sonarcube = pd.read_csv('../data/sonar_quality_profile.csv')
    df_travis = pd.read_csv('../data/travis_data_1.csv')

    project_url = df_travis['project_url']
    project_url = project_url.unique()
    print(len(project_url))

    """
        Metric 1
    """
    df = pd.DataFrame()
    for project in project_url:
        df_sonarcube_sub = df_sonarcube.loc[df_sonarcube['project_url'] == project]
        df_travis_sub = df_travis.loc[df_travis['project_url'] == project]
        df_sonarcube_sub = df_sonarcube_sub.sort_values(by=['quality_profile_date']).reset_index()
        df_travis_sub = df_travis_sub.sort_values(by=['started_at']).reset_index()
        df_travis_sub['sonar_build'] = 0
        for i in range(df_travis_sub.shape[0]-1):
            build1 = df_travis_sub.loc[i, 'started_at']
            build2 = df_travis_sub.loc[i+1, 'started_at']
            rows = df_sonarcube_sub.query('quality_profile_date >= @build1 and quality_profile_date <= @build2')
            if rows.shape[0] > 0:
                df_travis_sub.loc[i, 'sonar_build'] = 1

        df = pd.concat([df, df_travis_sub], ignore_index=True)


    print("Metric 1: Code quality checking rate")
    number_builds_with_ccq = df.loc[df['sonar_build'] == 1].shape[0]
    print(f"CQCR: {number_builds_with_ccq/ df.shape[0]}")

    """
            Metric 2
    """
    ls = []
    for project in project_url:
        df_sub = df.loc[df['project_url'] == project]
        df_sub = df_sub.loc[df['sonar_build'] == 1].reset_index()
        for i in range(df_sub.shape[0] - 1):
            build1 = df_sub.loc[i, 'started_at']
            build2 = df_sub.loc[i + 1, 'started_at']
            day_diff = datetime.strptime(build2, '%Y-%m-%dT%H:%S:%fZ') - datetime.strptime(build1, '%Y-%m-%dT%H:%S:%fZ')
            ls.append(day_diff.days)

    print("Metric 2: Elapsed Time between checks")
    etc = sum(ls)/len(ls)
    print(f"ETC: {etc}")

    """
            Metric 3
    """
    ls = []
    for project in project_url:
        df_sonarcube_sub = df_sonarcube.loc[df_sonarcube['project_url'] == project]
        df_travis_sub = df_travis.loc[df_travis['project_url'] == project]
        df_sonarcube_sub = df_sonarcube_sub.sort_values(by=['quality_profile_date']).reset_index()
        df_travis_sub = df_travis_sub.sort_values(by=['started_at']).reset_index()
        for i in range(df_sonarcube_sub.shape[0]-1):
            build1 = df_sonarcube_sub.loc[i, 'quality_profile_date']
            build2 = df_sonarcube_sub.loc[i+1, 'quality_profile_date']
            rows = df_travis_sub.query('started_at >= @build1 and started_at <= @build2')
            ls.append(rows.shape[0])

    print("Metric 3: Elapsed Frame between checks")
    efc = sum(ls) / len(ls)
    print(f"EFC: {efc}")


if __name__ == '__main__':
    get_metrics()
