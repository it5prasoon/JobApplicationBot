from docx2txt import process as process_docx


def edit_cover_letter(recruiter_name, position, location):
    all_text = process_docx(f"cover letter manish.docx")
    all_text = all_text.replace(' at Neighborhood Trust Financial Partners', '')
    all_text = all_text.replace('[The HR @ Neighborhood Trust Financial Partners]', recruiter_name)
    all_text = all_text.replace('Hiring Manager', recruiter_name.split(' ')[0])
    all_text = all_text.replace('[', '').replace(']', '')
    all_text = all_text.replace('successful CTO', f'successful {position}')
    all_text = all_text.replace('\nmkothary@gmail.com', '')
    all_text = all_text.replace("Vice President of Innovation", position).replace("New York City",
                                                                                  location)  # replacing the keywords
    # accordingly

    return all_text  # returning the updated cover letter
