import random
import sys
import shutil
import glob
import os
import subprocess


k = 4

os.chdir("all")
all_files = glob.glob("*.csv")
# random.shuffle(all_files)
# test_files = random.sample(all_files, len(all_files)//k)
# train_files = list(set(all_files) - set(test_files))
os.chdir("..")
test_files = ['0914.csv', '0480.csv', '0362.csv', '0140.csv', '0779.csv', '0181.csv', '0172.csv', '0414.csv', '0250.csv', '0205.csv', '0404.csv', '0039.csv', '0407.csv', '0930.csv', '0885.csv', '0460.csv', '0322.csv', '1045.csv', '0114.csv', '0355.csv', '0975.csv', '0690.csv', '0174.csv', '0199.csv', '0856.csv', '0438.csv', '0840.csv', '0716.csv', '0531.csv', '0633.csv', '0073.csv', '1014.csv', '0126.csv', '0240.csv', '0580.csv', '1029.csv', '0288.csv', '0676.csv', '0442.csv', '0697.csv', '0443.csv', '0216.csv', '0616.csv', '0150.csv', '0447.csv', '0819.csv', '1009.csv', '0493.csv', '1054.csv', '0622.csv', '1025.csv', '0836.csv', '0211.csv', '0667.csv', '0703.csv', '0610.csv', '0320.csv', '0906.csv', '0682.csv', '0623.csv', '0451.csv', '0119.csv', '0235.csv', '0889.csv', '0793.csv', '0585.csv', '0596.csv', '0503.csv', '0308.csv', '0312.csv', '0476.csv', '0754.csv', '0239.csv', '0428.csv', '0487.csv', '0956.csv', '0802.csv', '0743.csv', '0650.csv', '0831.csv', '0720.csv', '1040.csv', '1001.csv', '0044.csv', '0019.csv', '0817.csv', '0721.csv', '0768.csv', '0574.csv', '0203.csv', '0466.csv', '0278.csv', '0265.csv', '0786.csv', '0471.csv', '0201.csv', '0669.csv', '0054.csv', '0731.csv', '0815.csv', '0241.csv', '0611.csv', '1050.csv', '0258.csv', '0711.csv', '0967.csv', '0867.csv', '0894.csv', '0518.csv', '0692.csv', '0219.csv', '1067.csv', '0630.csv', '0304.csv', '0999.csv', '0828.csv', '0918.csv', '0128.csv', '0534.csv', '0353.csv', '0968.csv', '0825.csv', '0012.csv', '0058.csv', '0655.csv', '1017.csv', '0701.csv', '0243.csv', '0935.csv', '0259.csv', '0321.csv', '0735.csv', '0557.csv', '0427.csv', '0154.csv', '0522.csv', '0723.csv', '0023.csv', '0117.csv', '0824.csv', '0387.csv', '0749.csv', '0352.csv', '1004.csv', '1076.csv', '0046.csv', '0346.csv', '1074.csv', '0299.csv', '0358.csv', '0866.csv', '0842.csv', '0483.csv', '0138.csv', '0348.csv', '0087.csv', '0280.csv', '0535.csv', '0898.csv', '0059.csv', '0780.csv', '0925.csv', '0392.csv', '0614.csv', '0037.csv', '0521.csv', '0873.csv', '0970.csv', '0916.csv', '0853.csv', '0467.csv', '0991.csv', '0759.csv', '0713.csv', '0277.csv', '1068.csv', '0997.csv', '0136.csv', '0328.csv', '0593.csv', '0245.csv', '0984.csv', '0345.csv', '0510.csv', '0306.csv', '0942.csv', '0847.csv', '0439.csv', '0987.csv', '1065.csv', '0843.csv', '0875.csv', '0671.csv', '0269.csv', '1037.csv', '0903.csv', '0256.csv', '0349.csv', '0771.csv', '0091.csv', '0444.csv', '0152.csv', '1006.csv', '1048.csv', '0560.csv', '0341.csv', '0196.csv', '0375.csv', '0354.csv', '0042.csv', '0185.csv', '0083.csv', '0583.csv', '0937.csv', '0380.csv', '0162.csv', '0895.csv', '0396.csv', '0384.csv', '0973.csv', '0053.csv', '0486.csv', '0533.csv', '0093.csv', '0040.csv', '0463.csv', '0705.csv', '0877.csv', '0086.csv', '0270.csv', '0344.csv', '0990.csv', '0473.csv', '1024.csv', '0652.csv', '0561.csv', '0310.csv', '1018.csv', '0319.csv', '0566.csv', '0477.csv', '1021.csv', '0760.csv', '0142.csv', '0821.csv', '0171.csv', '0772.csv', '0569.csv', '0478.csv', '0284.csv', '0156.csv', '0852.csv', '1061.csv', '0303.csv', '0386.csv', '0960.csv', '0455.csv', '0774.csv', '0625.csv', '0157.csv', '0262.csv', '0548.csv', '0283.csv', '0634.csv', '0972.csv', '0553.csv', '0879.csv', '0811.csv', '0357.csv'] 
 


# for each_files in test_files:
#     shutil.copy2(str("all/"+each_files), str("data/dev/"+each_files))

# for each_files in train_files:
#     shutil.copy2(str("all/"+each_files), str("all/train/"+each_files))

for each_file in all_files:
    if each_file in test_files:
        shutil.copy2(str("all/" + each_file), str("data/dev/" + each_file))
    else:
        shutil.copy2(str("all/" + each_file), str("data/train/" + each_file))

print("TEST: ",len(test_files))
# print("TRAIN: ",len(train_files))