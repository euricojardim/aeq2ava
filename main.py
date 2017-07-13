import sys, os
from pydub import AudioSegment
from BeautifulSoup import BeautifulSoup

### Must have pydub and BeautifulSoup
### pydub uses ffmpeg or avlib

#html_filepath = "/Volumes/gestores/TSF_Arquivo/Emissao16.htm"
#sound_path = "/Volumes/gestores/Emissao16/SOUND"
#export_sound_path = "/Users/ejardim/Projects/python_workspace/aeq2ava/MP3"

def main(html_filepath, sound_path, export_sound_path, *args):

	html_file = open(html_filepath, "r")
	html_content = html_file.read()

	soup = BeautifulSoup(html_content)

	for table_row in soup.findAll("tr"):
		cells = table_row.findAll("td")
		if len(cells) > 0:
			title = cells[0].text.strip()
			creator = cells[3].text.strip()
			wav_filename = cells[8].text.strip()
			if wav_filename and wav_filename[-4:].upper() == '.WAV':
				wav_filepath = os.path.join(sound_path, wav_filename)				
				if os.path.isfile(wav_filepath):
					print("Processing file " + wav_filepath + " ... [" + title + "]")
					song = AudioSegment.from_wav(wav_filepath)
					mp3_filename = wav_filename[:-4] + ".mp3"
					mp3_filepath = os.path.join(export_sound_path, mp3_filename)
					if not os.path.isfile(mp3_filepath):
						song.export(mp3_filepath, format="mp3", bitrate="128k", tags={'artist': creator, 'title': title})
					else:
						print("   Skipping file " + wav_filename + " - MP3 already exists!")	
				else:
					print("Skipping inexistent file " + wav_filepath)

if __name__ == "__main__":

	reload(sys)
	sys.setdefaultencoding('utf-8')

	if len(sys.argv) != 5:
		raise SyntaxError("Invalid arguments.")
	else:
		main(sys.argv[2], sys.argv[3], sys.argv[4])

	