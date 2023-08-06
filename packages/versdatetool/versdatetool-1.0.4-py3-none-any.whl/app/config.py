# Enter Your Github Personal access token here
API_KEY = 'ENTER YOUR token'

FILENAME = "package.json"

INPUT_CSV_PATH = "../data/input.csv"
OUTPUT_CSV_PATH = "../data/output.csv"

output_header = ["name", "repo", "version", "version_satisfied"]
output_header_with_pr = ["name", "repo", "version", "version_satisfied", "update_pr"]

GITHUB_FOLDER = "github_repos"
BRANCH_NAME = "versdate-update"
BASE_BRANCH = "main"