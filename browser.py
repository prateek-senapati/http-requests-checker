import streamlit as st
import requests
import csv
import os

st.title('BROWSER')
st.header('HTTP Requests Checker')
http_request = st.sidebar.selectbox(
label='Choose HTTP Request Method:',
options=['', 'HEAD', 'GET', 'POST', 'PUT', 'DELETE']
)

if http_request == 'GET' or http_request == 'HEAD':
    # create a dictionary to store URL parameters before sending HTTP request
    params = dict()
    url = st.sidebar.text_input(label='URL:', value='')
    params_checkbox = st.sidebar.checkbox(
    label='Check this box to add URL parameters.'
    )
    if params_checkbox:
        # payloads.csv stores URL parameters one by one - before adding them to params dict()
        with open('payloads.csv', 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            param_key = st.sidebar.text_input(label='Parameter Key:', value='')
            param_value = st.sidebar.text_input(label='Parameter Value:', value='')
            add_param = st.sidebar.button(label='Add Parameter')
            if add_param:
                # add the given URL parameter to payloads.csv
                csv_writer.writerow([param_key, param_value])
                st.sidebar.success('Parameter added successfully!')

    send_request = st.sidebar.button(label=f'Send {http_request} Request')
    if send_request:
        if params_checkbox:
            with open('payloads.csv', 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                # read all the URL parameters from payloads.csv, and add them to params dict()
                for line in csv_reader:
                    params[line[0]] = line[1]
            # delete payloads.csv - so that it can be used as a new file for a new request
            os.remove('payloads.csv')
        st.sidebar.success(f'{http_request} request sent.')
        try:
            # send HTTP request according to user's choice, and fetch the response
            if http_request == 'GET':
                r = requests.get(url=url, params=params)
            elif http_request == 'HEAD':
                r = requests.head(url=url, params=params)
            st.subheader('URL')
            st.write(r.url)
            st.subheader('Status Code')
            if r.ok:
                st.success(r.status_code)
            else:
                st.error(r.status_code)
            if http_request == 'GET':
                st.subheader("Server's Reponse Headers")
                st.write(r.headers)
        except Exception as e:
            st.exception(e.__class__)

elif http_request == 'DELETE':
    url = st.sidebar.text_input(label='URL:', value='')
    send_request = st.sidebar.button(label='Send DELETE Request')
    if send_request:
        st.sidebar.success(f'{http_request} request sent.')
        try:
            r = requests.delete(url=url)
            st.subheader('URL')
            st.write(r.url)
            st.subheader('Status Code')
            if r.ok:
                st.success(r.status_code)
            else:
                st.error(r.status_code)
            st.subheader("Server's Reponse Headers")
            st.write(r.headers)
        except Exception as e:
            st.exception(e.__class__)

elif http_request == 'POST' or http_request == 'PUT':
    # create a dictionary to store form data before sending HTTP request
    data = dict()
    # create a dictionary to store file data before sending HTTP request
    files = dict()
    url = st.sidebar.text_input(label='URL:', value='')
    data_checkbox = st.sidebar.checkbox(
    label='Check this box to add form data.'
    )
    if data_checkbox:
        # payloads.csv stores form data one by one - before adding them to data dict()
        with open('payloads.csv', 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            data_key = st.sidebar.text_input(label='Form Data Key:', value='')
            data_value = st.sidebar.text_input(label='Form Data Value:', value='', type='password')
            add_data = st.sidebar.button(label='Add Form Data')
            if add_data:
                # add the given form data to payloads.csv
                csv_writer.writerow([data_key, data_value])
                st.sidebar.success('Form Data added successfully!')
    files_checkbox = st.sidebar.checkbox(
    label='Check this box to add files.'
    )
    if files_checkbox:
        # files.csv stores file data one by one - before adding them to files dict()
        with open('files.csv', 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            file_name = st.sidebar.text_input(label='File Name (Key):', value='')
            file_data = st.sidebar.file_uploader('Choose a file:')
            add_file = st.sidebar.button(label='Add File')
            if add_file:
                # add the given file data to files.csv
                # read() is used to read the file as bytes
                csv_writer.writerow([file_name, file_data.read()])
                st.sidebar.success('File added successfully!')

    send_request = st.sidebar.button(label=f'Send {http_request} Request')
    if send_request:
        if data_checkbox:
            with open('payloads.csv', 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                # read all the form data from payloads.csv, and add them to data dict()
                for line in csv_reader:
                    data[line[0]] = line[1]
            # delete payloads.csv - so that it can be used as a new file for a new request
            os.remove('payloads.csv')
        if files_checkbox:
            with open('files.csv', 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                # read all the file data from files.csv, and add them to files dict()
                for line in csv_reader:
                    files[line[0]] = line[1]
            # delete files.csv - so that it can be used as a new file for a new request
            os.remove('files.csv')
        st.sidebar.success(f'{http_request} request sent.')
        try:
            # send HTTP request according to user's choice, and fetch the response
            if http_request == 'POST':
                r = requests.post(url=url, data=data, files=files)
            elif http_request == 'PUT':
                r = requests.put(url=url, data=data, files=files)
            st.subheader('URL')
            st.write(r.url)
            st.subheader('Status Code')
            if r.ok:
                st.success(r.status_code)
            else:
                st.error(r.status_code)
            st.subheader("Server's Reponse Headers")
            st.write(r.headers)
        except Exception as e:
            st.exception(e.__class__)
