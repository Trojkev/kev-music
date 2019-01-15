import xlrd

from account.backend.services import StateService


def read_data_from_excel(excel_file):
	# reads data from an excel_file
	file_path = str(excel_file)
	
	# create a workbook using the excel file received
	w_book = xlrd.open_workbook(file_path)
	
	# open the excel_sheet with the data
	sheet = w_book.sheet_by_index(0)
	
	# import the database model Albums
	from music.models import Album
	
	# instantiate a state
	state = StateService().get(name = 'Active')
	# loop through the data printing all the data
	
	for row in range(1, sheet.nrows):
		# print (str(sheet.cell_value(row, col))),
		obj = Album(
				artist = sheet.cell_value(row, 0),
				album_title = sheet.cell_value(row, 1),
				genre = sheet.cell_value(row, 2),
				state = state)
		print('album added')
		obj.save()

	return 'Success'
