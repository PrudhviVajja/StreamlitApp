import streamlit as st
import requests
import collections 
import json
from google.cloud import storage
import time

storage_client = storage.Client(project='faas-297022')
bucket = storage_client.bucket('faasimages')

def generate(url, filename):
    link = 'https://us-central1-faas-297022.cloudfunctions.net/sent_freq'
    param = {'link': url}
    r = requests.post(link, json=param)
    data = json.loads(r.text) 

    st.write("frequency counts are being sent to second function.... it takes a minute for the first time..")
    
    link = 'https://us-central1-faas-297022.cloudfunctions.net/plot_data'
    param = {'data': data, 'filename': filename}
    
    r = requests.post(link, json=param)
    st.image("https://storage.googleapis.com/faasimages/" + filename[:-3] + "png")
    
    st.write("Done")
    
def main():
    st.title("Find the Distribution of sentence lengths in a file")
    
    url = st.text_input('Url of the book:')
    filename = url.split('/')[-1] #+ '.abc'
    
    if st.button('Submit url'):
        if storage.Blob(bucket=bucket, name=filename[:-3]+"png").exists(storage_client):
            st.write("This is a Cached Image:")
            st.image("https://storage.googleapis.com/faasimages/" + filename[:-3] + "png")
#             if st.button("If you want to run it anyway and see for yourself"):
#                 generate(url, filename)
        else:
            generate(url, filename)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    st.write("Time taken to calculate output ==> " + str(start-end))
