import csv
import glob
import os
import sys

import matplotlib.pyplot as plt
import math

def Opening_files (Hash_list, Ac_list, i, input_files, index_range) :
    for index in range(index_range):
        csv_file = open(input_files[index + i], 'r', encoding='utf-8')
        csv_reader = csv.reader(csv_file)
        Hash_value = list()
        Ac_value = list()
        header = next(csv_reader)
        Making_list(Hash_value, Ac_value, csv_reader)
        Hash_list.append(Hash_value)
        Ac_list.append(Ac_value)
        csv_file.close()

def Opening_files_Babo (Hash_list, Ac_list, i, input_files) :
    csv_file = open(input_files[i], 'r', encoding='utf-8')
    csv_reader = csv.reader(csv_file)
    Hash_value = list()
    Ac_value = list()
    header = next(csv_reader)
    Making_list(Hash_value, Ac_value, csv_reader)
    Hash_list.append(Hash_value)
    Ac_list.append(Ac_value)
    csv_file.close()

def Making_list (Hash_value, Ac_value, csv_reader) :

    for line in csv_reader :
        if len(line) == 0 :
            continue
        else:
            Hash_value.append(float(line[0]))
            Ac_value.append(int(line[1]))

def ploting_LineartoLinear_Babo(Hash_list, Ac_list, input_file_name, reinvestment_ratio_list, HorC) :
    if HorC == 0:
        if len(input_file_name) == 99:
            output_file_name = input_file_name[68:95] + 't1.png'
        else:
            output_file_name = input_file_name[68:96] + 't1.png'
    else:
        if len(input_file_name) == 109:
            output_file_name = input_file_name[78:105] + 't1.png'
        else:
            output_file_name = input_file_name[78:106] + 't1.png'
    for index in range(len(Hash_list[0])):
        Hash_list[0][index] += 1
    plt.plot(Hash_list[0], Ac_list[0], linewidth = 0.5)
    plt.scatter(Hash_list[0], Ac_list[0], s = 1)
    if HorC == 0:
        plt.title('Hash-Accumulated Frequency')
        plt.xlabel('Hash')
    else:
        plt.title('Cryptocurrency-Accumulated Frequency')
        plt.xlabel('Cryptocurrency')
    plt.ylabel('Accumulated Frequency')
    plt.savefig(output_file_name, dpi = 350)

    plt.close()

def ploting_LineartoLog_Babo(Hash_list, Ac_list, input_file_name, reinvestment_ratio_list, HorC):
    if HorC == 0:
        if len(input_file_name) == 99:
            output_file_name = input_file_name[68:95] + 't2.png'
        else:
            output_file_name = input_file_name[68:96] + 't2.png'
    else:
        if len(input_file_name) == 109:
            output_file_name = input_file_name[78:105] + 't2.png'
        else:
            output_file_name = input_file_name[78:106] + 't2.png'

    for index in range(len(Hash_list[0])):
        Ac_list[0][index] = math.log(Ac_list[0][index])
    plt.plot(Hash_list[0], Ac_list[0], linewidth=0.5)
    plt.scatter(Hash_list[0], Ac_list[0], s=1)
    if HorC == 0 :
        plt.title('Hash-log(Accumulated Frequency)')
        plt.xlabel('Hash')
    else :
        plt.title('Cryptocurrency-log(Accumulated Frequency)')
        plt.xlabel('Cryptocurrency')
    plt.ylabel('log(Accumulated Frequency)')
    plt.savefig(output_file_name, dpi=350)

    plt.close()

def ploting_LogtoLog_Babo(Hash_list, Ac_list, input_file_name, reinvestment_ratio_list, HorC):
    if HorC == 0:
        if len(input_file_name) == 99:
            output_file_name = input_file_name[68:95] + 't3.png'
        else:
            output_file_name = input_file_name[68:96] + 't3.png'
    else:
        if len(input_file_name) == 109:
            output_file_name = input_file_name[78:105] + 't3.png'
        else:
            output_file_name = input_file_name[78:106] + 't3.png'

    for index in range(len(Hash_list[0])):
            Hash_list[0][index] = math.log(Hash_list[0][index])
    plt.plot(Hash_list[0], Ac_list[0], linewidth=0.5)
    plt.scatter(Hash_list[0], Ac_list[0], s=1)
    if HorC == 0:
        plt.title('log(Hash)-log(Accumulated Frequency)')
        plt.xlabel('log(Hash)')
    else:
        plt.title('log(Cryptocurrency)-log(Accumulated Frequency)')
        plt.xlabel('log(Cryptocurrency)')
    plt.ylabel('log(Accumulated Frequency)')
    plt.savefig(output_file_name, dpi=350)

    plt.close()


def ploting_LineartoLinear(Hash_list, Ac_list, input_file_name, reinvestment_ratio_list, HorC, total_length, path_length) :

    output_file_name = input_file_name[path_length + 1 : total_length - 12] + 't1.png'

    for i in range(len(reinvestment_ratio_list)) :
        Max_val = Hash_list[i][0]
        Min_val = Hash_list[i][len(Hash_list[i]) - 1]
        division_ratio = Max_val - Min_val
        if division_ratio == 0:
            division_ratio = 1
        for index in range(len(Hash_list[i])) :
            Hash_list[i][index] = (((Hash_list[i][index] - Min_val) * 9.0) / division_ratio) + 1
            #Hash_list[i][index] = Hash_list[i][index]/Min_val
        plt.plot(Hash_list[i], Ac_list[i], label = reinvestment_ratio_list[i], linewidth = 0.5)
        plt.scatter(Hash_list[i], Ac_list[i], s = 1)
    if HorC == 0:
        plt.title('Hash-Accumulated Frequency')
        plt.xlabel('Hash')
    else:
        plt.title('Cryptocurrency-Accumulated Frequency')
        plt.xlabel('Cryptocurrency')
    plt.ylabel('Accumulated Frequency')
    plt.legend()
    plt.savefig(output_file_name, dpi = 350)

    plt.close()

def ploting_LineartoLog(Hash_list, Ac_list, input_file_name, reinvestment_ratio_list, HorC, total_length, path_length):
    output_file_name = input_file_name[path_length + 1: total_length - 12] + 't2.png'

    for i in range(len(reinvestment_ratio_list)):
        for index in range(len(Hash_list[i])):
            Ac_list[i][index] = math.log(Ac_list[i][index])
        plt.plot(Hash_list[i], Ac_list[i], label=reinvestment_ratio_list[i], linewidth=0.5)
        plt.scatter(Hash_list[i], Ac_list[i], s=1)
    if HorC == 0 :
        plt.title('Hash-log(Accumulated Frequency)')
        plt.xlabel('Hash')
    else :
        plt.title('Cryptocurrency-log(Accumulated Frequency)')
        plt.xlabel('Cryptocurrency')
    plt.ylabel('log(Accumulated Frequency)')
    plt.legend()
    plt.savefig(output_file_name, dpi=350)

    plt.close()

def ploting_LogtoLog(Hash_list, Ac_list, input_file_name, reinvestment_ratio_list, HorC, total_length, path_length):
    output_file_name = input_file_name[path_length + 1 : total_length - 12] + 't3.png'


    for i in range(len(reinvestment_ratio_list)):
        for index in range(len(Hash_list[i])):
            Hash_list[i][index] = math.log(Hash_list[i][index])
        plt.plot(Hash_list[i], Ac_list[i], label=reinvestment_ratio_list[i], linewidth=0.5)
        plt.scatter(Hash_list[i], Ac_list[i], s=1)
    if HorC == 0:
        plt.title('log(Hash)-log(Accumulated Frequency)')
        plt.xlabel('log(Hash)')
    else:
        plt.title('log(Cryptocurrency)-log(Accumulated Frequency)')
        plt.xlabel('log(Cryptocurrency)')
    plt.ylabel('log(Accumulated Frequency)')
    plt.legend()
    plt.savefig(output_file_name, dpi=350)

    plt.close()

def ploting_LineartoLinear_SDis(Hash_list, Ac_list, input_file_name, reinvestment_ratio_list, HorC, total_length, path_length) :
    for j in range(4):
        output_file_name = input_file_name[path_length + 1: total_length - 14] + 'di' + str(j) + 't1.png'
        for i in range(len(reinvestment_ratio_list)) :
            Max_val = Hash_list[i*4 + j][0]
            Min_val = Hash_list[i*4 + j][len(Hash_list[i*4 + j]) - 1]
            division_ratio = Max_val - Min_val
            if division_ratio == 0:
                division_ratio = 1
            for index in range(len(Hash_list[i*4 + j])) :
                Hash_list[i*4 + j][index] = (((Hash_list[i*4 + j][index] - Min_val) * 9.0) / division_ratio) + 1
                #Hash_list[i][index] = Hash_list[i][index]/Min_val
            plt.plot(Hash_list[i*4 + j], Ac_list[i*4 + j], label = reinvestment_ratio_list[i], linewidth = 0.5)
            plt.scatter(Hash_list[i*4 + j], Ac_list[i*4 + j], s = 1)
        if HorC == 0:
            plt.title('Hash-Accumulated Frequency')
            plt.xlabel('Hash')
        else:
            plt.title('Cryptocurrency-Accumulated Frequency')
            plt.xlabel('Cryptocurrency')
        plt.ylabel('Accumulated Frequency')
        plt.legend()
        plt.savefig(output_file_name, dpi = 350)

        plt.close()

def ploting_LineartoLog_SDis(Hash_list, Ac_list, input_file_name, reinvestment_ratio_list, HorC, total_length, path_length):
    for j in range(4):
        output_file_name = input_file_name[path_length + 1: total_length - 14] + 'di' + str(j) + 't2.png'

        for i in range(len(reinvestment_ratio_list)):
            for index in range(len(Hash_list[i*4 + j])):
                Ac_list[i*4 + j][index] = math.log(Ac_list[i*4 + j][index])
            plt.plot(Hash_list[i*4 + j], Ac_list[i*4 + j], label=reinvestment_ratio_list[i], linewidth=0.5)
            plt.scatter(Hash_list[i*4 + j], Ac_list[i*4 + j], s=1)
        if HorC == 0 :
            plt.title('Hash-log(Accumulated Frequency)')
            plt.xlabel('Hash')
        else :
            plt.title('Cryptocurrency-log(Accumulated Frequency)')
            plt.xlabel('Cryptocurrency')
        plt.ylabel('log(Accumulated Frequency)')
        plt.legend()
        plt.savefig(output_file_name, dpi=350)

        plt.close()

def ploting_LogtoLog_SDis(Hash_list, Ac_list, input_file_name, reinvestment_ratio_list, HorC, total_length, path_length):
    for j in range(4):
        output_file_name = input_file_name[path_length + 1 : total_length - 14] + 'di' + str(j) + 't3.png'


        for i in range(len(reinvestment_ratio_list)):
            for index in range(len(Hash_list[i*4 + j])):
                Hash_list[i*4 + j][index] = math.log(Hash_list[i*4 + j][index])
            plt.plot(Hash_list[i*4 + j], Ac_list[i*4 + j], label=reinvestment_ratio_list[i], linewidth=0.5)
            plt.scatter(Hash_list[i*4 + j], Ac_list[i*4 + j], s=1)
        if HorC == 0:
            plt.title('log(Hash)-log(Accumulated Frequency)')
            plt.xlabel('log(Hash)')
        else:
            plt.title('log(Cryptocurrency)-log(Accumulated Frequency)')
            plt.xlabel('log(Cryptocurrency)')
        plt.ylabel('log(Accumulated Frequency)')
        plt.legend()
        plt.savefig(output_file_name, dpi=350)

        plt.close()

def ploting_LineartoLinear_Rewardbase(Hash_list, Ac_list, input_file_name, reinvestment_ratio_list, HorC, total_length, path_length):
    pass

def ploting_LineartoLog_Rewardbase(Hash_list, Ac_list, input_file_name, reinvestment_ratio_list, HorC, total_length, path_length):
    pass

def ploting_LogtoLog_Rewardbase(Hash_list, Ac_list, input_file_name, reinvestment_ratio_list, HorC, total_length, path_length):
    pass

if __name__ == '__main__':

    #input_path_Hash = "E:\Dropbox\PhD Research\Blockchain_Code\Python\Data\Babo model\Hash"
    #input_path_crypto = "E:\Dropbox\PhD Research\Blockchain_Code\Python\Data\Babo model\Cryptocurrency"
    #input_path_Hash = "E:\Dropbox\PhD Research\Blockchain_Code\Python\Data\Selective Reinvestment\Hash"
    #input_path_crypto = "E:\Dropbox\PhD Research\Blockchain_Code\Python\Data\Selective Reinvestment\Cryptocurrency"
    #input_path_Hash = "E:\Dropbox\PhD Research\Blockchain_Code\Python\Data\Simplest Model\Hash"
    #input_path_crypto = "E:\Dropbox\PhD Research\Blockchain_Code\Python\Data\Simplest Model\Cryptocurrency"
    input_path_Hash = r"C:\Users\wingo\Workspace\Dropbox\PhD Research\Blockchain_Code\Python\Data\Exp1\Hash\Rit1"
    input_path_crypto = r"C:\Users\wingo\Workspace\Dropbox\PhD Research\Blockchain_Code\Python\Data\Exp1\Cryptocurrency\Rit1"
    input_files_Hash = glob.glob(os.path.join(input_path_Hash, '*.csv'))
    input_files_crypto = glob.glob(os.path.join(input_path_crypto, '*.csv'))
    #reinvestment_ratio_list = [0.0001, 0.0005, 0.025, 0.05, 0.075, 0.00875, 0.1,
    #                           0.5, 0.001, 0.00125, 0.0025, 0.005, 0.0075, 0.00875, 0.01, 0.0125]
    reinvestment_ratio_list = [0.0001, 0.001, 0.01, 0.1]
    #reinvestment_ratio_list = ['0.0001, rt0', '0.0001, rt1', '0.001, rt0', '0.001, rt1', '0.01, rt0', '0.01, rt1', '0.1, rt0', '0.1, rt1']

"""
    i = 0
    while i < len(input_files_Hash):
        Hash_list = list()
        Ac_list = list()
        Opening_files(Hash_list, Ac_list, i, input_files_Hash, 16)
        ploting_LineartoLinear_SDis(Hash_list, Ac_list, input_files_Hash[i], reinvestment_ratio_list, 0, len(input_files_Hash[i]), len(input_path_Hash))
        ploting_LineartoLog_SDis(Hash_list, Ac_list, input_files_Hash[i], reinvestment_ratio_list, 0,
                                    len(input_files_Hash[i]), len(input_path_Hash))
        ploting_LogtoLog_SDis(Hash_list, Ac_list, input_files_Hash[i], reinvestment_ratio_list, 0,
                                    len(input_files_Hash[i]), len(input_path_Hash))
        i = i +16

        j = 0
        while j < len(input_files_crypto):
            crypto_list = list()
            Ac_list = list()
            Opening_files(crypto_list, Ac_list, j, input_files_crypto, 16)
            ploting_LineartoLinear_SDis(crypto_list, Ac_list, input_files_crypto[j], reinvestment_ratio_list, 1, len(input_files_crypto[j]), len(input_path_crypto))
            ploting_LineartoLog_SDis(crypto_list, Ac_list, input_files_crypto[j], reinvestment_ratio_list, 1, len(input_files_crypto[j]), len(input_path_crypto))
            ploting_LogtoLog_SDis(crypto_list, Ac_list, input_files_crypto[j], reinvestment_ratio_list, 1, len(input_files_crypto[j]), len(input_path_crypto))
            j = j + 16


    i = 0
    while i < len(input_files_Hash):
        Hash_list = list()
        Ac_list = list()
        Opening_files(Hash_list, Ac_list, i, input_files_Hash, len(reinvestment_ratio_list))
        ploting_LineartoLinear(Hash_list, Ac_list, input_files_Hash[i], reinvestment_ratio_list, 0, len(input_files_Hash[i]), len(input_path_Hash))
        ploting_LineartoLog(Hash_list, Ac_list, input_files_Hash[i], reinvestment_ratio_list, 0, len(input_files_Hash[i]), len(input_path_Hash))
        ploting_LogtoLog(Hash_list, Ac_list, input_files_Hash[i], reinvestment_ratio_list, 0, len(input_files_Hash[i]), len(input_path_Hash))
        i = i + 4
    j = 0
    while j < len(input_files_crypto):
        crypto_list = list()
        Ac_list = list()
        Opening_files(crypto_list, Ac_list, j, input_files_crypto, len(reinvestment_ratio_list))
        ploting_LineartoLinear(crypto_list, Ac_list, input_files_crypto[j], reinvestment_ratio_list, 1, len(input_files_crypto[j]), len(input_path_crypto))
        ploting_LineartoLog(crypto_list, Ac_list, input_files_crypto[j], reinvestment_ratio_list, 1, len(input_files_crypto[j]), len(input_path_crypto))
        ploting_LogtoLog(crypto_list, Ac_list, input_files_crypto[j], reinvestment_ratio_list, 1, len(input_files_crypto[j]), len(input_path_crypto))
        j = j + 4
   
    for i in range(len(input_files_Hash)):
        Hash_list = list()
        Ac_list = list()
        Opening_files_Babo(Hash_list, Ac_list, i, input_files_Hash)
        ploting_LineartoLinear_Babo(Hash_list, Ac_list, input_files_Hash[i], reinvestment_ratio_list, 0)
        ploting_LineartoLog_Babo(Hash_list, Ac_list, input_files_Hash[i], reinvestment_ratio_list, 0)
        ploting_LogtoLog_Babo(Hash_list, Ac_list, input_files_Hash[i], reinvestment_ratio_list, 0)

        crypto_list = list()
        Ac_list2 = list()
        Opening_files_Babo(crypto_list, Ac_list2, i, input_files_crypto)
        ploting_LineartoLinear_Babo(crypto_list, Ac_list2, input_files_crypto[i], reinvestment_ratio_list, 1)
        ploting_LineartoLog_Babo(crypto_list, Ac_list2, input_files_crypto[i], reinvestment_ratio_list, 1)
        ploting_LogtoLog_Babo(crypto_list, Ac_list2, input_files_crypto[i], reinvestment_ratio_list, 1)

    
    i = 0
    while i < len(input_files_Hash) :
        Hash_list = list()
        Ac_list = list()
        Opening_files(Hash_list, Ac_list, i, input_files_Hash)
        ploting_LineartoLinear(Hash_list, Ac_list, input_files_Hash[i], reinvestment_ratio_list, 0)
        ploting_LineartoLog(Hash_list, Ac_list, input_files_Hash[i], reinvestment_ratio_list, 0)
        ploting_LogtoLog(Hash_list, Ac_list, input_files_Hash[i], reinvestment_ratio_list, 0)
        i = i + 16
    j = 0
    while j < len(input_files_crypto) :
        crypto_list = list()
        Ac_list = list()
        Opening_files(crypto_list, Ac_list, j, input_files_crypto)
        ploting_LineartoLinear(crypto_list, Ac_list, input_files_crypto[j], reinvestment_ratio_list, 1)
        ploting_LineartoLog(crypto_list, Ac_list, input_files_crypto[j], reinvestment_ratio_list, 1)
        ploting_LogtoLog(crypto_list, Ac_list, input_files_crypto[j], reinvestment_ratio_list, 1)
        j = j + 16

    """


