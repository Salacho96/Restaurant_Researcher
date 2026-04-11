import json
import os

from fastapi import HTTPException
import requests
from langchain.tools import tool


class SearchTools():

  @tool("Search the internet")
  def search_internet(query):
    """Useful to search the internet
    about a a given topic and return relevant results"""
    top_result_to_return = 4
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.environ['SERPER_API_KEY'],
        'content-type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # check if there is an organic key
    if 'organic' not in response.json():
      return "Sorry, I couldn't find anything about that, there could be an error with you serper api key."
    else:
      results = response.json()['organic']
      string = []
      for result in results[:top_result_to_return]:
        try:
          string.append('\n'.join([
              f"Title: {result['title']}", f"Link: {result['link']}",
              f"Snippet: {result['snippet']}", "\n-----------------"
          ]))
        except KeyError:
          next

      return '\n'.join(string)
  
  @tool("review analytics")
  def get_review_and_session_analytics(restaurant_name: str, token: str, timeframe: str) -> dict:
      """Fetch review and session analytics for a given restaurant within a specified timeframe."""
      
      base_url = "https://api.payfud.com/r"
      
      # Endpoint for Google reviews analytics
      google_reviews_url = f"{base_url}/{restaurant_name}/v1/google-reviews/analitycs?timeframe={timeframe}"
      
      # Endpoint for general analytics (sessions)
      general_analytics_url = f"{base_url}/{restaurant_name}/v1/general-analytics/analitycs_type?type_filter=sessions&timeframe=90&start_date=2024-04-18"
      
      headers = {
          'Authorization': f'Bearer {token}'
      }
      print(google_reviews_url)
      # Make the request to Google reviews analytics endpoint
      google_reviews_response = requests.get(google_reviews_url, headers=headers)
      if google_reviews_response.status_code != 200:
          raise HTTPException(status_code=google_reviews_response.status_code, detail=f"Error fetching Google reviews analytics for {restaurant_name}")
      
      # Make the request to general analytics endpoint
      general_analytics_response = requests.get(general_analytics_url, headers=headers)
      if general_analytics_response.status_code != 200:
          raise HTTPException(status_code=general_analytics_response.status_code, detail=f"Error fetching session analytics for {restaurant_name}")
      
      # Parse the JSON responses
      google_reviews_data = google_reviews_response.json()
      general_analytics_data = general_analytics_response.json()
      
      # Combine the results into a single dictionary
      analytics_data = {
          "google_reviews": google_reviews_data,
          "session_analytics": general_analytics_data
      }
      
      return analytics_data

