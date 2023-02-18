import requests
import pandas as pd


def get_sonarcube_data():
    """
        Get all the public projects available in sonarcube
    """
    df = pd.DataFrame()
    for i in range(1, 210):
        print(f"====== Interation {i} ======")
        url = "https://sonarcloud.io/api/components/search_projects?boostNewProjects=false&facets=ncloc%2Clanguages&p=" + \
              str(i) + "&ps=50&f=analysisDate&s=analysisDate&asc=false"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 400:
            break
        else:
            response = response.json()
            sub_df = pd.DataFrame(response['components'])
            df = pd.concat([df, sub_df])

    """
        Write data into a csv
    """
    df = df.sort_values(by='organization')
    df.to_csv('../data/sonarcube_data_projects.csv', index=False)


if __name__ == '__main__':
    get_sonarcube_data()

