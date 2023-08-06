import os
from utils.Csv import Csv


rpath = os.path.join("..", "data", "input.csv")
wpath = os.path.join("..", "data", "csv_out.csv")

# print(path)
csvrObj = Csv(rpath)

# result = csvrObj.read_all()

# print(type(result))
#
# for lines in result:
#     print(lines)

csvwobj = Csv(wpath)

# rowHeader = ["name", "repo", "version", "version_satisfied"]
rowHeader = ["name", "repo", "version", "version_satisfied", "update_pr"]
rowOne = ["surya", "myrepo", "v1.0.2", "yes", "https://github.com/surya-x/PlagAnalyser"]

csvwobj.write_row(rowHeader)
csvwobj.append_row(rowOne)