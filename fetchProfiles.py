import os                                                   
import json 
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import linkedin_compliance_fix

# In case the `redirect_url` does not implement https     
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' 

# Credentials received from registering a new application
client_id = input('Enter your LinkedIn App Client Id: ')
client_secret = input('Enter your LinkedIn App Client Secret: ')
redirect_url = input('Enter your authorized redirect URL from LinkedIn config: ')

# OAuth endpoints
authorization_base_url = 'https://www.linkedin.com/oauth/v2/authorization'
token_url = 'https://www.linkedin.com/oauth/v2/accessToken'

# Authorized Redirect URL (from LinkedIn config)
linkedin = OAuth2Session(client_id, redirect_uri=redirect_url)
linkedin = linkedin_compliance_fix(linkedin)

# Redirect user to LinkedIn for authorization
authorization_url, state = linkedin.authorization_url(authorization_base_url)
print('Please go here and authorize,', authorization_url)

# Callback url
redirect_response = input('Paste the full redirect URL here:')

# Fetch the access token
linkedin.fetch_token(token_url, client_secret=client_secret,
                     authorization_response=redirect_response)

# Fetch user profile
r = linkedin.get('https://api.linkedin.com/v1/people/~:(id,first-name,last-name,formatted-name,num-connections,location,specialties,positions,email-address,headline,summary)?format=json')
parsed = json.loads(r.content)
print(parsed)