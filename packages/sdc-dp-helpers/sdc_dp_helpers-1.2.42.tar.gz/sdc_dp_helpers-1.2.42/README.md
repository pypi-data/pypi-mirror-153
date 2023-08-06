# SDC DataPipeline Helpers

Contains building blocks for data pipelines, specifically those that ingest data and run on ECS. It leverages the the packages in `./sdc_dp_helpers/` code to improve reusability and creating new pipelines by sharing python classes. It achieves this by abstracting functionality that is commonly reused but still allows the user to write for their own use-case by exteding base class functionality.

### Requirements

- GCP service account with `Google Analytics read policy`
- GCP `service account email` added to Google Analytics

## Quick Start

Getting started with pulling batch data from ga and dumping in to .json

1. Make sure your python environment is set up.

2. Place \<client-secret-key\>.p12 in a folder like `./google_secrets` directory

3. Run

```
    make install-requirements
```
    You can find a requirements.yml in the repository.
3. Create an initial config.yaml

    Run the following code once off to create an initial data pipeline config.
    You can either write a python script or open a python repl to run the following:

```
    from sdc_dp_helpers.google_analytics.utils import init_config

    init_config('data_pipeline_config.yaml')
```
Remember to add the:
- client_secret _(in the reader config portion of the config)_
- scopes _(in the reader config portion of the config)_
- service_account_email _(in the reader config portion of the config)_
- viewIDs _(in the query config portion of the config)_

3. Writing your first pipeline.

    Start with the file provided at: `./data_pipeline.py`

4. Run the code

    note: this config should be in the same directory as data_pipeline.py

## More Ethical Queries

We use decorators to handle both request ethicality and request errors.
See `sdc_dp_helpers/api_utilities/retry_managers.py` for a deeper look at the decorator code.

### (1.) Ethical queries using WAIT and BACKOFF

Make use of the `sdc_dp_helpers/api_utilities/retry_managers.py` `request_handler` function.
The suggested workflow is adding the following to your environment variables. Testing locally you may consider adding these to your `.env` file, keeping in mind that python does not automatically load ENV vars. So use something like `python-dotenv`, find out more [here](https://github.com/theskumar/python-dotenv).

```
REQUEST_WAIT_TIME=1
REQUEST_BACKOFF_FACTOR=0.01
REQUEST_BACKOFF_METHOD='random'
```

And making use the following functionality.

```
    @request_handler(
        wait=int(os.environ.get('REQUEST_WAIT_TIME', 0)),
        backoff_factor=float(os.environ.get('REQUEST_BACKOFF_FACTOR', 0.01)),
        backoff_method=os.environ.get('REQUEST_BACKOFF_METHOD', 0.01)
    )
    def myfunction():

        ## code here
        pass

```

### (2.) Handling Errors

Make use of the `sdc_dp_helpers/api_utilities/retry_managers.py` `retry_handler` function.

Making use the following functionality.

```
    @retry_handler(Exception, total_tries=2)
    def myfunction():

        ## code here
        pass

```


## Using & Extending

The data pipeline comprises 4 components, namely:
| components | description |
|---|---|
| reader class | reader class which pulls data through a request to the external API or source |
| writer class | writer class which writes data to file or destination |
| config_manager class | config loader, parser and query builder |
| data_pipeline script | `your data pipeline` script which executes the your pipeline |

The code is set up to simplify the the creation of new data pipelines and allow code sharing when it comes to data pipelines.
As such, when a pipeline has been constructed previously from a given external API or source, a new user need only write a `data pipeline script`. In some cases, a new user may require a different destination writer and can easily add this to the `writer class` 

## References
These are helpful references which someone may use to learn more about what you have done here.

- `Introduction to Analytics v4 API`: https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py
- `GA and Sampling`: [Understanding GA report sampling](https://www.bounteous.com/insights/2013/06/24/how-solve-google-analytics-sampling-8-ways-get-more-data/) 
- `GA sampling when samples > 500k`: [Setting queries to keep samples below GA sample limit](https://www.getresponse.com/blog/using-google-analytics)
- `Components of A query in GA`: [Understanding various parts incl. Metrics, Sampling, Dimensions, etc](https://medium.com/analytics-for-humans/a-cheat-sheet-for-mastering-google-analytics-api-requests-39d36e0f3a4a)
- `Duplicate records pulled`: [Is this Transaction duplicates](https://www.simoahava.com/analytics/prevent-google-analytics-duplicate-transactions-with-customtask/)
- `dateRange are inclusive`: [GA startDate, endDates are inclusive](https://stackoverflow.com/questions/21303291/google-analytics-api-start-and-end-date)
- `PyYaml: Extending the functionality`: [Extending the YAML loader with PyYaml](https://pyyaml.org/wiki/PyYAMLDocumentation)
- `Data completeness: isDataGolden` : [isDataGolden is True when a new request will not return any new results](https://developers.google.com/analytics/devguides/reporting/core/v4/rest/v4/reports/batchGet)
