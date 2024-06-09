import streamlit as st

st.set_page_config(
    page_title="Vid2Post AI",
    page_icon="./files/logo.ico",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.fiverr.com/mouniraziz91',
        'About': "Vid2Post AI is a web app that generates a blog article and tweets from your Youtube video. Created by: https://www.fiverr.com/mouniraziz91."
    }
)

from pytube import YouTube
import os
from download_pdf import create_download_link, open_pdf_as_bytes

from extract_audio import extract
from langchain_helper import produce
from save_pdf import md_to_pdf
from speech_to_text import transcript


if 'run_button' not in st.session_state:
    st.session_state.generating = False
    st.session_state.regenerating = True

def disable():
    st.session_state.generating = True
    st.session_state.regenerating = False

def enable():
    st.session_state.generating = False
    st.session_state.regenerating = True
    
# func to save BytesIO on a drive
def write_bytesio_to_file(filename, bytesio):
    with open(filename, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(bytesio.getbuffer())
    outfile.close()

def on_progress(stream, total_size, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent = bytes_downloaded / total_size * 100
    progress_text = "Downloading the video... Please wait."
    my_bar.progress(int(percent), text=progress_text)


def Download(link):
    youtubeObject = YouTube(link, on_progress_callback=on_progress)
    stream = youtubeObject.streams.get_highest_resolution()
    yt_title = youtubeObject.title
    yt_author = youtubeObject.author
    yt_views = youtubeObject.views
    yt_description = youtubeObject.description
    yt_publish_date= youtubeObject.publish_date
    yt_link = link
    if os.path.exists("./files/video.mp4"):
        os.remove("./files/video.mp4")
    try:
        stream.download(filename='./files/video.mp4')
    except:
        print("An error has occurred")
    print("Download is completed successfully")
    return [yt_title, yt_author, yt_views, yt_description, yt_publish_date, yt_link]

yt_info = []

with st.sidebar:
    grid = st.columns(6)
    with grid[1]:
        st.image("./files/logo.png", width=200)
    st.markdown("<h1 style='text-align: center;'>Vid2Post AI v0.1.0</h1>", unsafe_allow_html=True)
    google_api_key = st.text_input("API Key", placeholder = 'Enter your Google API key...', disabled=st.session_state.generating,type="password")
    video_type = st.selectbox(
        "How would you like to provide the video?",
        ("From youtube", "From your device"), disabled=st.session_state.generating
    )
    saved = False
    if video_type=="From your device":
        saved=False
        upload_file = st.file_uploader("Upload a Video", disabled=st.session_state.generating, type=["mp4"])
        if upload_file is not None:
            temp_file_to_save = './files/video.mp4'
            write_bytesio_to_file(temp_file_to_save, upload_file)
            saved=True
            st.video("./files/video.mp4")
            st.markdown('''
            <style>
                .uploadedFile {display: none}
            <style>''',
            unsafe_allow_html=True)
        else:
            st.info('Upload a Video From Your Device', icon="💁")

    if video_type=="From youtube":
        youtube_link = st.text_input("Youtube video link", disabled=st.session_state.generating, placeholder="Enter a youtube video link...")
        if youtube_link:
            if youtube_link.startswith("https://www.youtube.com/watch?v="):
                saved=True
            else:
                st.sidebar.warning('Invalid Youtube Video Link', icon="⚠️")
        else:
            st.info('Enter a Youtube Video Link', icon="💁")

    generate_btn = st.button("Generate a report", use_container_width=True , key="run_button", on_click=disable, type ="primary" ,disabled=not saved or not google_api_key or st.session_state.generating)

st.title("Vid2Post AI Generator")
st.write("#### Generate a blog article and tweets from your favorite videos.")

report_success = None 
container= st.container(border=True)

if generate_btn and saved:
    container.empty()
    blank = container.write("")
    container.empty()
    blank = container.write("")
    container.empty()
    if(video_type=="From youtube"):
        my_bar = container.progress(0, text="")
        progress_text = "Downloading the video... Please wait."
        my_bar.progress(0, text=progress_text)
        yt_info = Download(youtube_link)
        my_bar.progress(100, text="Downloading is Completed")
        my_bar.empty()
    header = container.header("Generating Report...")
    generation_bar = container.progress(0, text="")
    extract("./files/video.mp4", "./files/audio.mp3")
    generation_bar.progress(30, text="")
    transcript("./files/audio.mp3","./files/transcript.txt")
    generation_bar.progress(60, text="")
    article, tweets, clean_output= produce(google_api_key)
    generation_bar.progress(100, text="")
    header.empty()
    generation_bar.empty()
    container.video("./files/video.mp4")
    if (yt_info!=[]):
        container.write("Title: "+yt_info[0])
        container.write("Author: "+yt_info[1])
        container.write("Number of Views: "+str("{:,}".format(yt_info[2]))+" views")
        container.write("Published Date: "+str('%s/%s/%s' % (yt_info[4].month, yt_info[4].day, yt_info[4].year)))
        container.write("Link: "+ yt_info[5])
    container.write("## Blog Article 📰")
    container.write(article)
    container.write("## Tweets 🐤")
    container.write(tweets)
    generated_output = "## Blog Article 📰"+"""\n"""+article+"""\n"""+"## Tweets 🐤"+"""\n"""+tweets
    with open("./files/generated_text.md", "w", encoding="utf-8") as f:
        f.write(generated_output)
    f.close()
    with open("./files/generated_text_clean.md", "w", encoding="utf-8") as f:
        f.write(clean_output)
    f.close()
    report_success = container.success('Report Genrerated Successfuly!', icon="✅")
    save_pdf_btn = container.button("Save the report to a pdf file", type="primary", use_container_width=True)

with st.sidebar:
    regenerate_btn = st.button("Generate again", use_container_width=True , on_click=enable, disabled= st.session_state.regenerating or (report_success is None))

if report_success is None:
    container.empty() 
    if os.path.exists("./files/generated_text.md"):
        container.video("./files/video.mp4")
        if (yt_info!=[]):
            container.write("Title: "+yt_info[0])
            container.write("Author: "+yt_info[1])
            container.write("Number of Views: "+str("{:,}".format(yt_info[2]))+" views")
            container.write("Published Date: "+str('%s/%s/%s' % (yt_info[4].month, yt_info[4].day, yt_info[4].year)))
            container.write("Link: "+ yt_info[5])
        container.header("Last Generated Report")
        with open("./files/generated_text.md", "r", encoding="utf-8") as f:
                report = f.read()
        f.close()
        container.write(report)
        st.session_state.allow_pdf_save = True
        save_pdf_btn = container.button("Save the report to a pdf file", type="primary", use_container_width=True)

if save_pdf_btn:
    md_to_pdf("./files/generated_text.pdf")
    st.success('Pdf Generated Successfuly!', icon="✅")
    pdf_file_path = './files/generated_text.pdf'  # Change this to the path of your PDF file
    pdf_bytes = open_pdf_as_bytes(pdf_file_path)
    download_link = create_download_link(pdf_bytes, 'generated_report')
    st.markdown(download_link, unsafe_allow_html=True)

if regenerate_btn and report_success is not None:
    st.rerun()