import pandas as pd
import csv, glob

pert_id_dirs = glob.glob('clue/touchstone/*')

cmap_csv ='cmap.csv'

# # 建立表格的列名
# test_cell_path = pert_id_dirs[0] + '/pert_id_cell.gct'
# test_summary_path = pert_id_dirs[0] + '/pert_id_summary.gct'
#
# filednames = ['pert_id']

log = open('log.txt', 'w+', newline='', encoding='utf-8')
# with open(test_cell_path, 'r') as cell_f:
#     for line in cell_f.readlines()[3:]:
#         filednames.append(line.strip().split('\t')[0])
# with open(test_summary_path, 'r') as cell_f:
#     for line in cell_f.readlines()[3:]:
#         filednames.append(line.strip().split('\t')[0]+':Summary')

header = ['pert_id', 'pert_cell', 'Score']
with open(cmap_csv, 'w', newline='') as cmap:
    writer = csv.DictWriter(cmap, fieldnames=header)
    writer.writeheader()
    # 写入dict的同时是否也可以吸入index
    for pert_id_dir in pert_id_dirs:
        try:
            with open(pert_id_dir + '/pert_id_cell.gct', 'r') as cell_file:
                lines = cell_file.readlines()
                pert_id = lines[2].strip().split('\t')[-1]
                for line in lines[3:]:
                    pert_dict = {header[0]: pert_id}
                    key, value = line.strip().split('\t')
                    pert_dict[header[1]] = key
                    pert_dict[header[2]] = value
                    writer.writerow(pert_dict)

            with open(pert_id_dir + '/pert_id_summary.gct', 'r') as summary_file:
                lines = summary_file.readlines()
                pert_id = lines[2].strip().split('\t')[-1]
                for line in lines[3:]:
                    pert_dict = {header[0]: pert_id}
                    key, value = line.strip().split('\t')
                    pert_dict[header[1]] = key+':Summary'
                    pert_dict[header[2]] = value
                    writer.writerow(pert_dict)

        except Exception as e:
            print(e, file=log)
log.close()
