import os


SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"]= "gpt-4o-2024-05-13"
from crew import RestaurantCrew
from tools import search_tools
def run():
    inputs = {
        'restaurant' : 'avenueblu',
        'token' : os.getenv("API_TOKEN")
    }
    result  = RestaurantCrew().crew().kickoff(inputs=inputs)
    print("result begins")
    print("##################")
    print("result---->",result)
    print("##################")
    print("result ends")
if __name__ == "__main__":
    run()


