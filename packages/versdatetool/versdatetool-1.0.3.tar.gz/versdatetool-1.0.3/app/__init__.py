
__app_name__ = "versdate"
__version__ = "1.0.0"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    CSV_READ_ERROR,
    CSV_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(7)

ERRORS = {
    DIR_ERROR: "directory error",
    FILE_ERROR: "Input File not found error",
    CSV_READ_ERROR: "CSV read error",
    CSV_WRITE_ERROR: "CSV write error",
    ID_ERROR: "to-do id error",
}