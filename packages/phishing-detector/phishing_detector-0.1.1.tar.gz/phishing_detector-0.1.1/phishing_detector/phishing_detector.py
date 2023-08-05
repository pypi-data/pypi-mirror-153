import requests
import validators
import pandas as pd
from concurrent.futures import ThreadPoolExecutor


API_URL = "http://api.phishingdetector.live/api/"


class Detector:
    def __init__(self, api_key: str):
        """
        Initialize the PhishingDetector class with api key.
        API key is required to use the PhishingDetector class.

        :param api_key: Your unique api key
        :type api_key: str
        """
        authentication = self.__auth(api_key)
        if authentication:
            self.api_key = api_key
        else:
            raise Exception("Invalid API Key")

    def __auth(self, api_key: str):
        """
        Authenticates the api key.

        :param api_key: Your unique api key
        :type api_key: str
        """
        print("Authenticating...")
        api_url = f"{API_URL}authority/api-key/"
        headers = {
            "Authorization": f"Token {api_key}"
        }
        response = requests.get(api_url, headers=headers)

        if response.text == '"Invalid API Key"':
            return False

        if "success" in response.json().keys():
            self.headers = {
                "Authorization": f"Token {api_key}"
            }
            return True

        return False

    def query(self, url: str):
        """
        Queries whether the url is phishing or not.

        :param url: The url to query
        :type url: str
        """
        if validators.url(url):
            api_url = f"{API_URL}get-url/?url={url}"
            # post operation for query
            response = requests.get(api_url, headers=self.headers)
            # returns str -> Phishing or Legitimate
            return response.text.split('"')[1]

        raise Exception("Invalid URL (should be http://example.com)")

    def query_by_file(self, file: str, output_file: str = None, max_workers: int = 10):
        """
        Loops through the file and queries each URL in it.

        :param file: The file to query
        :type file: str

        :param (optional) output_file: The output filename, if it is not set, it saves into input file.
        :type output_file: str

        :param (optional) max_workers: The maximum number of workers to use
        :type max_workers: int
        """
        if not file.endswith("csv"):
            raise Exception(f"Invalid File: {file}, file type must be .csv")

        try:
            df = pd.read_csv(file)
        except Exception as e:
            raise Exception(f"Invalid File: {file}, file type must be .csv")

        urls = df["url"].tolist()
        self.results = {}

        print("Querying...")

        with ThreadPoolExecutor(max_workers=max_workers) as exe:
            exe.map(self.__query_list, urls)

        if output_file:
            data = {"url": urls, "output": []}
            for url in data["url"]:
                if url in self.results.keys():
                    data["output"].append(self.results[url])
                else:
                    data["output"].append("couldn't connect")
            df = pd.DataFrame.from_dict(data)
            df.to_csv(output_file, index=False)

        else:
            df["output"] = ""
            for i in self.results:
                df.loc[df["url"] == i, "output"] = self.results[i]
            df.to_csv(file, index=False)

    def query_by_list(self, url_list: list[str], output_file: str, max_workers: int = 10):
        """
        Loops through the url list and queries each URL in it.

        :param list: The list of URLs to query
        :type list: str

        :param output_file: The output filename
        :type output_file: str

        :param (optional) max_workers: The maximum number of workers to use
        :type max_workers: int
        """

        self.results = {}

        print("Querying...")

        with ThreadPoolExecutor(max_workers=max_workers) as exe:
            exe.map(self.__query_list, url_list)

        data = {"url": [], "output": []}
        for i in self.results:
            data["url"].append(i)
            data["output"].append(self.results[i])
        df = pd.DataFrame.from_dict(data)
        df.to_csv(output_file, index=False)

    def __query_list(self, url: str):
        if validators.url(url):
            api_url = f"{API_URL}get-url/?url={url}"
            # post operation for query
            response = requests.get(api_url, headers=self.headers)
            # returns str -> Phishing or Legitimate
            self.results[url] = response.text.split('"')[1]
