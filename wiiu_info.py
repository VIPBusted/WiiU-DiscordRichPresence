from tcpgecko import TCPGecko
import struct, time
import urllib.request
import urllib.parse
import json

# Black Ops II
BO2_JAP = 0x0005000010113700
BO2_USA = 0x0005000010113500
BO2_EUR = 0x0005000010113400

# WiiU Menu
HOME_MENU_JAP = 0x0005001010040000
HOME_MENU_USA = 0x0005001010040100
HOME_MENU_EUR = 0x0005001010040200

# Mii Maker
MIIMAKER_JAP = 0x000500101004A000
MIIMAKER_USA = 0x000500101004A100
MIIMAKER_EUR = 0x000500101004A200

# YouTube
YOUTUBE_ALL = 0x0005000010105700

def make_string(buf):
	print(buf)
	nbuf = ""
	for c in buf:
		if c == "\x00":
			return nbuf
		else:
			nbuf += c

def Handle_HomeMenu(self):
	return 0, "533260406886760458", "In the Menu", "{} titles installed".format(self.MCP_GetTitleCount(self.MCP_Open()) - 68), time.time(), None, "wiiu", "WiiU Menu", None, None

def Handle_Unknown(self, tid_hi, tid_low):
	url = "https://cemui.com/api/v2/GetGame/title_id/"
	f1 = "%08x" % tid_hi
	f2 = "%08x" % tid_low
	url = url + f1 + "-" + f2
	data = urllib.request.urlopen(url).read().decode("utf-8")
	ret = json.loads(data)
	return 0, "535590879503843328", ret["game_publisher"], ret["game_title"], time.time(), None, None, None, None, None

class WiiU_Titles():

	def __init__(self, tcp):
		self.tcp = tcp
		self.Total_TitleID = []
		self.MCP_GetTitleCount = self.tcp.get_symbol("coreinit.rpl", "MCP_TitleCount", True)
		self.MCP_Open = self.tcp.get_symbol("coreinit.rpl", "MCP_Open", True)

	def init_titles(self):

		# You can add yours

		self.Total_TitleID.append(BO2_JAP)
		self.Total_TitleID.append(BO2_USA)
		self.Total_TitleID.append(BO2_EUR)

		self.Total_TitleID.append(HOME_MENU_JAP)
		self.Total_TitleID.append(HOME_MENU_USA)
		self.Total_TitleID.append(HOME_MENU_EUR)

		self.Total_TitleID.append(MIIMAKER_JAP)
		self.Total_TitleID.append(MIIMAKER_USA)
		self.Total_TitleID.append(MIIMAKER_EUR)

		self.Total_TitleID.append(YOUTUBE_ALL)

	def OSGetTitleID(self):

		return struct.unpack(">Q", self.tcp.readmem(0x10013C10, 8))[0]

	def call_handler_for_tid(self, tid):

		if tid in self.Total_TitleID:

			if tid == BO2_JAP or tid == BO2_USA or tid == BO2_EUR:
				return Handle_BlackOps2()

			if tid == HOME_MENU_JAP or tid == HOME_MENU_USA or tid == HOME_MENU_EUR:
				return Handle_HomeMenu(self)

			if tid == MIIMAKER_JAP or tid == MIIMAKER_USA or tid == MIIMAKER_EUR:
				return Handle_MiiMaker()

			if tid == YOUTUBE_ALL:
				return Handle_MiiMaker()


		else:
			tid_hi = tid >> 32
			tid_low = tid & 0xFFFFFFFF
			return Handle_Unknown(self, tid_hi, tid_low)