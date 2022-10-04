
class Generate():
    def __init__(self, writer) -> None:
        self.writer = writer

    def generate(self, file_name, applicant_infos):
        workbook = self.writer.Workbook(file_name)
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        worksheet.write(0, 0, 'ID', bold)
        worksheet.write(0, 1, 'Full Name', bold)
        worksheet.write(0, 2, 'Identify Number', bold)
        worksheet.write(0, 3, 'Phone Number', bold)
        worksheet.write(0, 4, 'Email', bold)
        worksheet.write(0, 5, 'Date of Birth', bold)
        worksheet.write(0, 6, 'Country', bold)
        worksheet.write(0, 7, 'Status', bold)
        worksheet.write(0, 8, 'Permanent Residence', bold)
        worksheet.write(0, 9, 'Nationality', bold)
        worksheet.write(0, 10, 'New Applicant', bold)
        worksheet.write(0, 11, 'Place', bold)

        row = 1
        col = 0
        for applicant in applicant_infos:
            id = str(applicant.id)
            name = applicant.name
            identify_number = applicant.identify_number
            phone_number = applicant.phone_number
            email = applicant.email
            dob = applicant.dob
            country = applicant.country
            permanent_residence = applicant.permanent_residence
            nationality = applicant.nationality.value
            status = applicant.status.value
            new_applicant = applicant.new_applicant
            place = applicant.place
            worksheet.write(row, col, id)
            worksheet.write(row, col + 1, name)
            worksheet.write(row, col + 2, identify_number)
            worksheet.write(row, col + 3, phone_number)
            worksheet.write(row, col + 4, email)
            worksheet.write(row, col + 5, dob)
            worksheet.write(row, col + 6, country)
            worksheet.write(row, col + 7, permanent_residence)
            worksheet.write(row, col + 8, nationality)
            worksheet.write(row, col + 9, status)
            worksheet.write(row, col + 10, new_applicant)
            worksheet.write(row, col + 11, place)
            row += 1
        workbook.close()
