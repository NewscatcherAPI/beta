# Getting Started
## Authentication
Newscatcher supports authentication with the API key. Once you received a key, you are allowed to make API requests.



## Endpoints

There are 2 available endpoints  `/search` and `/all`:
- Text search `/search` - the main method for searching through news articles based on parameters like __text__,  __date__ and/or __source__. This is a perfect tool when you want to look for articles on a specific subject on a single source or on worldwide news sources. 
- Lastest articles `/all` - an auxiliary method that allows you to choose a time-lapse and get the latest news on specific or multiple sources.

<br/><br/>

The request consists of:
- URL of the API
- endpoint followed by a question mark `?` to pass parameters
- parameters separated by `&`
- API Key to be put in Headers



## Endpoints Description



### `/search` endpoint

You can specify your search using several parameters. All results are sorted by the score of accuracy to the requested word or phrase.
##### Required Parameters
- `phrase=[string]` - word or phrase that will be searched inside articles' content. By default, it is searched through both `title` and `summary` fields

##### Optional Parameters
- `source=[string, string]` - one or more news resources can be specified for searching. Better enter URL of official websites of news sources. It should be the normal form of the URL, for example, __nytimes.com__, __theguardian.com__ (~~https://www.nytimes.com/~~, ~~https://www.theguardian.com/international~~)

- `from` and `to` - to search for a specific time period. In order to avoid errors, use on of the presented forms:`YYYY-MM-DD`, `DD/MM/YYYY`, `YYYY-MM-DD HH:MI:SS`, `DD/MM/YYYY HH:MI:SS`

- `title=False` - set `True` to search only inside articles' title

- `summary=False` - set `True` to search only inside articles' bodies

- `maxsize=20` - number of received results in one call. Restricted to 100

- `bydate=False` - set `True` to sort articles by date

- `isranked=True` - by default, only sources which are in  [Majestic top million](https://majestic.com/reports/majestic-million) are returned. Set to `False` if you want to see all the results


<br/><br/>
<br/><br/>

### `/all` endpoint
You can use this method for exploring the latest articles of one or more news sources within a specific time-lapse. Articles are sorted by the rank of a news source.


All parameters are optional, however, you can use either `hours` or `from` and `to`, not both at the same time.  

##### Optional Parameters
- `source=[string, string]` - one or more news resources can be specified for searching. Better enter URL of official websites of news sources

- `from` and `to` - search for a specific time period. In order to avoid errors, use the next form `YYYY-MM-SS HH:MI:SS` or `DD/MM/YYYY`

- `hours=[integer]` - articles published for the last `hours` will be displayed

- `maxsize=20` - number of received results in one call. Restricted to 100

- `bydate=False` - set `True` to sort articles by date

- `isranked=True` - by default, only sources which are in  [Majestic top million](https://majestic.com/reports/majestic-million) are returned. Set to `False` if you want to see all the results

<br/><br/>

<br/><br/>


### Response object for `/search` and `/all` endpoints

1.  ___status__ - the status of the response
2. ___total__ - how many articles are found. 10,000 is a limit 
3. __articles__ - list of found articles

<br/><br/>

__articles__:

- ___id__ - The unique id of an article

- ___score__ - Relevance score for  

- ___source__ - The list of main relevant information of the article

  * __author__ - The main author of the article
  * __authors__ - The list of authors
    * name - The name of author
  * __clean_url__ - The official URL of the news source
  * __comments__ - The URL to the comments part
  * __domain__ - The official domain of the news source
  * __feed_update__ - The last time when the news feed was updated
  * __language__ - The language of the article
  * __link__ - The direct URL of the article
  * __maj_ref_ips__ - Referring IPs to the main domain according to [Majestic](https://majestic.com/)
  * __maj_ref_subnets__ - Referring subnets to the main domain according to [Majestic](https://majestic.com/)
  * __parse_date__ - The date when the article was added to the database
  * __published__ - The date when the article was published, in UTC
  * __rank__ - The rank of the news source according to [Majestic](https://majestic.com/)
  * __rights__ - The copyright
  * __summary__ - The description of the article
  * __tags__ - The list of tags or keywords concerning the article
    * label - Not relevant
    * scheme - Not relevant
    * term - The keyword of the article
  * __title__ - The title of the article




## Examples





#### HTTP request
##### `/search`
1. 50 latest articles on COVID-19 
<br/><br/>
```<API_URL>/search?phrase=COVID-19&maxsize=50```
<br/><br/>
2. 50 latest articles on COVID-19 from NYTimes, WSJ and The Guardian
<br/><br/>
```<API_URL>/search?phrase=COVID-19&source=nytimes.com,wsj.com,theguardian.com&maxsize=50```
<br/><br/>
3. 50 latest articles on COVID-19 from NYTimes, WSJ and The Guardian for the specific date
<br/><br/>
```<API_URL>/search?phrase=COVID-19&source=nytimes.com,wsj.com,theguardian.com&from=2020-03-25&to=2020-03-26&maxsize=50```
<br/><br/>

##### `/all`
1. 25 latest articles from NYTimes and Foxnews for the last 24 hours sorted by date
<br/><br/>
```<API_URL>/all?hours=24&source=nytimes.com,foxnews.com&bydate=True&maxsize=25```
<br/><br/>
2. 25 latest articles from NYTimes and Foxnews for the specific date
<br/><br/>
```<API_URL>/all?source=nytimes.com,foxnews.com,theguardian.com&bydate=True&maxsize=25&from=2020-03-25&to=2020-03-26```
<br/><br/>
<br/><br/>

#### Python snippet
``` 
import requests

def print_results(results, variable):
      for i in results['articles']:
            try:
                  print(i['_source'][str(variable)])
            except:
                  print('Variable is not available for id - ' + str(i['_id']))


def save_variable(results, variable):
      output = []
      for i in results['articles']:
            try:
                  output.append(i['_source'][str(variable)])
            except:
                  if str(variable) in ['tags', 'authors']:
                        output.append(['Nothing found'])
                  else:
                        output.append('Nothing found')
      return output


url = <API_URL> + 'search?' \
      'phrase= Paris Coronavirus&' \
      'title=True'

API_KEY = <YOUR_KEY>

response = requests.get(url, headers={'x-api-key': API_KEY})

result = response.json()

print('Number of found matches - ' + str(result['_total']))

print_results(result, 'title')

content = save_variable(result, 'summary')
tags = save_variable(result, 'tags')

```
<br/><br/>
<br/><br/>
#### cURL
```
curl -H "X-API-KEY: <PUT_YOUR_API_KEY> <API_URL>/search?phrase=Trump&title=True
```
<br/><br/>
<br/><br/>
### `search_ui` and `all_ui` methods
There is an option to display results using a simple UI interface. Parameters are identical, only names of endpoints are different. Use an extension to your browser to be able to put an API KEY inside the headers. https://addons.mozilla.org/en-US/firefox/addon/modify-header-value/





