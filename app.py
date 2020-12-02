import streamlit as st
import requests
import collections 
import json

def generate():
    link = 'https://us-central1-faas-297022.cloudfunctions.net/sent_freq'
    param = {'link': url}
    r = requests.post(link, json=param)
    data = json.loads(r.text) 

    st.write("frequency counts are being sent to second function.... it takes a minute for te first time..")
    
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
        try:
            st.write("This is a Cached Image:")
            st.image("https://storage.googleapis.com/faasimages/" + filename[:-3] + "png")
            if st.button("If you want to run it anyway and see for yourself"):
                generate()
        except:
            generate()

if __name__ == "__main__":
    main()
