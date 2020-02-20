# Alternative Text analysis on Tweets photos

This project looks into analyzing the amount of tweets with photos that contain alternative text on accessibility related accounts. We compare the self made alt text with captions generated using the Computer Vision REST API from Azure Cognitive Services, calculating their similarity using the built-in python library difflib.

## How To
1. Download or clone repository
2. Open project
3. Open twitter_accessibility.py
4. Modify code as per “What’s needed?” section
5. Execute twitter_accessibility.py
6. See results in terminal


## What’s needed?

* Twitter API. You’ll need the following credentials to be able to run the project. You will need to assign the credential values to the variables in the code. 
  * Consumer_key = “ “ # twitter app’s API key
  * Consumer_secret = “ “ # twitter app’s API secret Key

* Computer Vision API. You will need to add your computer vision subscription key and endpoint to your environment variables. To obtain these you will need to create a new Computer Vision resource group in Microsoft Azure. Information on how to set the environment variables can be found on: https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account?tabs=multiservice%2Cwindows#configure-an-environment-variable-for-authentication 
Alternatively you can do this manually by accessing Environment Variables through System Properties on windows. No need for code modification.
  * Set COMPUTER_VISION_SUBSCRIPTION_KEY
  * Set COMPUTER_VISION_ENDPOINT

* Selenium:
  * Chromedriver.exe (included in the repository) might need to be replaced depending on the installed google chrome version. Versions can be found on: https://chromedriver.chromium.org/downloads 

* Twitter Account to Analyze. You can modify the account to be analyzed by changing the parameter “screen_name” on the “tweets” variable in the code. 

