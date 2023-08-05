import matplotlib.pyplot as plt
import peegy.io.generic_csv_reader as cvsr

file_path1 = r'D:\Measurements\IRU\CAP_Infants\AllData\001\20190409 12-23-21 - sub01_block1_sig0_1_65db.txt'
file_path2 = r'D:\Measurements\IRU\CAP_Infants\AllData\001\20190409 12-23-21 - sub01_block1_sig0_1_65db.txt'

header = cvsr.read_header(file_path1)
data, ev, _ = cvsr.read_channel(header=header)

plt.plot(data)
plt.plot(ev)
plt.show()
