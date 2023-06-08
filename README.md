# ML Dataset_Utilities

PIL_contain_MD5_savename.py
-----Resize and Save as MD5
-----PIL.ImageOps.contain()  and save with MD5 hashlib calculation

PIL_contain_threaded.py
-----Resize and Save - PIL.ImageOps.contain() - multi-thread
  
bing_dl_tags_v3.py
-----download bing images by keyword(s), and save titles/meta data as .txt files
-----Also extracts keyframes from video files
  
classmates_yearbooks.py
-----hehehehe

color_ngram_sort.py

-----i accidentally copied about 300k images from multiple post-processing sources together, 
-----but i pondered what i would do if they all werent backed up these were all lossy JPGs and MD5s don't match even though nearly identical, 
-----so i wrote a python script to blur everything slightly, contain the images to a (64,64) pixel size constraint, 
-----sliced the array to (-1,4) and re-mapped the RGBA  colour palette by summing the RGB values and adding a slight normalization function
-----converted the normalized values into hex values then joined the array into a string of 4,096 hex "words", 
-----then tokenized them and used tf-idf to rank the word cluster frequencies then rename for the top 10 sorted words + md5 + zfill(4)
-----good for finding duplicate pictures with different MD5s, or like-pictures

colormod.py
-----just a bunch of color functions for text output

heic_to_JPG.py
-----I really dislike Apple.

txt_to_IPTC.py
-----write .TXT tags to IPTC, allows for Windows Explorer searching for tags/keywords
  
iptc_to_txt.py
-----IPTC to .TXT files

keyword_move_copy.py
-----move/copy files based on keywords

move_video_frames_to_dirs.py
-----use FFMPEG to extract keyframes, then run this to create directories and move the images to a folder with the video file name

outlook_msg_parse_to_mssql.py
-----WIP - parse outlook messages, and save email metadata
-----will be adding Summarization functions later

unique_keywords_list.py
-----simple directory search for TXT, save all keywords, and output an ordered unique-only list

whisper_transcription.py
-----uses OpenAI Whisper to transcribe, saves to .TXT / .JSON


WIP - Utility Script / Menu Modules 
-----(personal all-in-one to stop editing hundreds of scripts all the time, and make dataset management easier)
