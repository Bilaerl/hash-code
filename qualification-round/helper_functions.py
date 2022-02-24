def read_file(input_file_path):
    contributors = {}
    projects = {}

    with open(input_file_path, 'r') as input_file:
        input_file = [line.replace('\n','') for line in input_file]
        # print(input_file)
        no_of_contributors, no_of_projects = input_file[0].split()
        no_of_contributors = int(no_of_contributors)
        no_of_projects = int(no_of_projects)
        idx = 1

        for i in range(no_of_contributors):
            contributor, contributor_skills = input_file[idx].split()
            contributor_skills = int(contributor_skills)

            contributors[contributor] = {}

            for j in range(contributor_skills):
                idx += 1
                contributor_skill, skill_level = input_file[idx].split()
                skill_level = int(skill_level)

                contributors[contributor][contributor_skill] = skill_level

            idx += 1

        for i in range(no_of_projects):
            # print(input_file[idx])
            project, project_days, project_score, project_best_before, no_of_project_roles = input_file[idx].split()
            project_days, project_best_before, = int(project_days), int(project_best_before)
            project_score, no_of_project_roles = int(project_score), int(no_of_project_roles)

            projects[project] = {}

            projects[project]['days'] = project_days
            projects[project]['score'] = project_score
            projects[project]['best_before'] = project_best_before
            projects[project]['roles'] = {}

            for j in range(no_of_project_roles):
                idx += 1
                skill, skill_level = input_file[idx].split()
                skill_level = int(skill_level)

                projects[project]['roles'][skill] = skill_level

            idx += 1

    return contributors, projects


if __name__ == '__main__':
    contributors, projects = read_file('input_data/b_better_start_small.in.txt')
    for contributor, skills in contributors.items():
        print(contributor)
        print(skills)
        print()

    for project, project_specs in projects.items():
        print(project)
        print(project_specs)
        print()
