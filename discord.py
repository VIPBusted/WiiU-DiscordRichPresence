from pypresence import Presence
from tcpgecko import TCPGecko
from wiiu_info import WiiU_Titles
import time

exit = 0

f = open("wiiu_rp.cfg", "r")
ip_addr = f.read()

if "." not in ip_addr:
	print("Please modify the 'wiiu_rp.cfg' and put your Wiiu Local IP Address")

tcp = TCPGecko(ip_addr.replace("IP= ", "").replace(" ", ""))

titles = WiiU_Titles(tcp)
titles.init_titles()

while exit == 0:
	ret_val, cid, state, details, start, end, large_image, large_text, party_id, party_size = titles.call_handler_for_tid(titles.OSGetTitleID())

	if ret_val == 0:
		try:
			p = Presence(cid)
			p.connect()
			p.update(state=state, details=details, start=start, end=end, large_image=large_image, large_text=large_text, party_id=party_id, party_size=party_size)
		except:
			ret_val += 1

	time.sleep(15)
