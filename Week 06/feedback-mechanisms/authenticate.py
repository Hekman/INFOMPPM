import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd

def authenticate():

	#0. Load users
	df_users = pd.read_json('users.json')
	
	#1. retrieve user credentials
	names = df_users['name'].tolist()
	passwords = df_users['password'].tolist()

	#2. create a hash for each passwords so that we do not send these in the clear
	hashed_passwords = stauth.Hasher(passwords).generate()

	#3. create the authenticator which will create an authentication session cookie with an expiry interval
	authenticator = stauth.Authenticate(names, names, hashed_passwords, 'streamlit-auth-0','streamlit-auth-0-key',cookie_expiry_days=1)

	#4. display the login form in the sidebar 
	name, authentication_status, username = authenticator.login('Login','sidebar')

	#5. the streamlit_authenticator library keeps state of the authentication status in streamlit's st.session_state['authentication_status']

	# > if the authentication succeeded (i.e. st.session_state['authentication_status'] == True)
	if st.session_state['authentication_status']:
		# display name on the sidebar
		with st.sidebar:
			st.text(name)			

		# set user id in session state
		user_id = int(df_users[df_users['name'] == name]['id'].iloc[0])
		st.session_state['user'] = user_id
		
	# > if the authentication failed
	elif st.session_state['authentication_status'] == False:
		# write an error message on the sidebar
		with st.sidebar:
			st.error('Username/password is incorrect')

	# > if there are no authentication attempts yet (e.g., first time visitors)
	elif st.session_state['authentication_status'] == None:
		# write an warning message on the sidebar
		with st.sidebar:			
			st.warning('Please enter your username and password in the sidebar')