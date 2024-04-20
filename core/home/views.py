from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def gen_resume(request):
    if request.method == 'POST':
        # Retrieve the data from the statically added input boxes
        name = request.POST.get('name')
        age = request.POST.get('age')
        about = request.POST.get('about')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Retrieve the data from the dynamically added input boxes
        work_data = []
        project_data = []
        education_data = []
        skill_data = {}
        achievement_data = {}
        language_data = {}

        # Get the initial education data
        initial_degree = request.POST.get('degree')
        initial_college = request.POST.get('college')
        initial_year = request.POST.get('year')
        
        # Check if initial education fields are not empty before adding them
        if initial_degree and initial_college and initial_year:
            education_data.append({
                'degree': initial_degree,
                'college': initial_college,
                'year': initial_year
            })

        # Loop through the keys of request.POST to extract the values of dynamically added input boxes
        for key, value in request.POST.items():
            if key.startswith('worktitle'):
                # Extract the index from the key
                index = key.replace('worktitle', '')
                try:
                    # Attempt to convert the index to an integer
                    work_index = int(index)
                except ValueError:
                    # Skip this iteration if the index is not a valid integer
                    continue
                # Add work title, duration, and description to the corresponding work entry
                if len(work_data) >= work_index:
                    # If the entry already exists, update its values
                    work_data[work_index - 1]['worktitle'] = value
                else:
                    # If the entry doesn't exist yet, create a new entry
                    work_data.append({'worktitle': value, 'workduration': '', 'workdes': ''})
            elif key.startswith('workduration'):
                # Extract the index from the key and update work duration
                index = key.replace('workduration', '')
                try:
                    work_index = int(index)
                except ValueError:
                    continue
                if len(work_data) >= work_index:
                    work_data[work_index - 1]['workduration'] = value
                else:
                    # If work title is not set, create a new entry with duration
                    work_data.append({'worktitle': '', 'workduration': value, 'workdes': ''})
            elif key.startswith('workdes'):
                # Extract the index from the key and update work description
                index = key.replace('workdes', '')
                try:
                    work_index = int(index)
                except ValueError:
                    continue
                if len(work_data) >= work_index:
                    work_data[work_index - 1]['workdes'] = value
                else:
                    # If work title is not set, create a new entry with description
                    work_data.append({'worktitle': '', 'workduration': '', 'workdes': value})
            # Add other conditions for processing skill, achievement, language, and education data as needed

            # Check if the key starts with 'titles' to identify work data
            # if key.startswith('worktitle'):
            #     work_data[key] = value

            # Check if the key starts with 'title' to identify project data
            elif key.startswith('title'):
                # Check if it's the initial project box or dynamically added project box
                if key == 'title':
                    # If it's the initial project box, add it directly to project_data
                    project_data.append({'title': value, 'duration': '', 'des': ''})
                else:
                    # If it's a dynamically added project box, extract the index and add it to project_data
                    index = key.replace('title', '')
                    try:
                        project_index = int(index)
                    except ValueError:
                        continue  # Skip this iteration if the index is not a valid integer
                    # Add the title to the corresponding project
                    if len(project_data) >= project_index:
                        project_data[project_index - 1]['title'] = value
                    else:
                        project_data.append({'title': value, 'duration': '', 'des': ''})
            # Check if the key starts with 'duration' to identify project duration data

            elif key.startswith('duration'):
                # Get the index of the corresponding project
                index = key.replace('duration', '')
                try:
                    project_index = int(index)
                except ValueError:
                    continue  # Skip this iteration if the index is not a valid integer
                # Add duration to the corresponding project
                if len(project_data) >= project_index:
                    project_data[project_index - 1]['duration'] = value
                else:
                    project_data.append({'title': '', 'duration': value, 'des': ''})
            # Check if the key starts with 'des' to identify project description data
            elif key.startswith('des'):
                # Get the index of the corresponding project
                index = key.replace('des', '')
                try:
                    project_index = int(index)
                except ValueError:
                    continue  # Skip this iteration if the index is not a valid integer
                # Add description to the corresponding project
                if len(project_data) >= project_index:
                    project_data[project_index - 1]['des'] = value
                else:
                    project_data.append({'title': '', 'duration': '', 'des': value})


            # Check if the key starts with 'skill' to identify skill data
            elif key.startswith('skill'):
                if key == 'skill':
                    skill_data[key] = value
                else:
                    index = key.split('skill')[1]
                    skill_data[f'skill{index}'] = value
            # Check if the key starts with 'ach' to identify achievement data
            elif key.startswith('ach'):
                if key == 'ach':
                    achievement_data[key] = value
                else:
                    index = key.split('ach')[1]
                    achievement_data[f'ach{index}'] = value
            # Check if the key starts with 'lang' to identify language data
            elif key.startswith('lang'):
                if key == 'lang':
                    language_data[key] = value
                else:
                    index = key.split('lang')[1]
                    language_data[f'lang{index}'] = value
            # Check if the key starts with 'degree' to identify dynamically added education data
            elif key.startswith('degree') and not key == 'degree':
                index = key.split('degree')[1]
                education_entry = {
                    'degree': value,
                    'college': request.POST.get(f'college{index}'),
                    'year': request.POST.get(f'year{index}')
                }
                education_data.append(education_entry)

        # Pass the retrieved data to the resume.html template
        return render(request, 'resume.html', {
            'name': name,
            'about': about,
            'age': age,
            'email': email,
            'phone': phone,
            'education_data': education_data,
            'work_data': work_data,
            'project_data': project_data,
            'skill_data': skill_data,
            'achievement_data': achievement_data,
            'language_data': language_data,
        })

    # If the request method is not POST, render the index.html template
    return render(request, 'index.html')
