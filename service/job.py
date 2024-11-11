allowing_modes = ['recommend-resume', 'recommend-description', 'rank-candidates']
player_status = ['have graduated and could start work rightnow', 'have not graduated and could start work in one month',
                 'have not graduated and consider to work', 'have not graduated and do not consider to start work']
status_bias = 1
degree_names = ['bachelor', 'master', 'doctor']
education_bias = 1

def describe_job(position, mode):
    assert mode in allowing_modes
    # print(position)
    # id = position['id']
    title = position['title']
    description = position['description']
    demand = position['demand']
    location = position['location']
    salary = position['salary']
    company = position['company']
    # created = position['create_at']
    job_type = position['job_type']
    # owner_id = position['owner_id']
    if mode in ['recommend-resume', 'recommend-description']:
        return f"""
        In the following is one of the jobs to be considered please consider the job description and my resume,
        rate this job by 1-100, 100 is the best match, 1 is the worst match. Just answer one number as score.
        The job title is {title}, and can be described as {description}, and the work location is {location}.
        The job type is {job_type}. The company requires {demand}. While the salary is {salary} RMB per month, the company name is {company}.
        """
    elif mode == 'rank-candidates':
        return f"""
        The job title is {title}, and can be described as {description}, and the work location is {location}.
        The job type is {job_type}. The company requires {demand}. While the salary is {salary} RMB per month, the company name is {company}.
        """


def describe_player(resume, mode):
    assert mode in allowing_modes
    
    if mode == 'recommend-resume':
        id = resume['id']
        user_id = resume['user_id']
        name = resume['name']
        gender = 'male' if resume['gender'] == 1 else 'female'
        phone = resume['phone']
        email = resume['email']
        wechat = resume['wechat']
        state = player_status[resume['state'] - status_bias]
        description = resume['description']
        education = resume['education']
        experience = resume['experience']
        project = resume['project']
        
        if education is not None and education != []:
            highest_education = sorted(education, key=lambda x: x['degree'], reverse=True)[0]
            highest_degree = degree_names[highest_education['degree'] - education_bias]
        else:
            highest_education = None
            highest_degree = "Unknown"
            education = []
        
        if experience is not None and experience != []:
            latest_experience = sorted(experience, key=lambda x: x['end_time'], reverse=True)[0]
        else:
            latest_experience = {
                'position': 'Unknown',
                'company': 'Unknown',
                'start_time': 'Unknown',
                'end_time': 'Unknown'
            }
            experience = []
        
        if project is not None and project != []:
            pass
        else:
            project = []
        
        return f"""
        I am look into jobs. In the following is my resume.
        My name is {name}, my gender is {gender}, and I {state}. I could describe myself as {description}.
        My highest degree is {highest_degree}. I have {len(experience)} work experiences.
        For my last job, I worked as {latest_experience['position']} at {latest_experience['company']} from {latest_experience['start_time']} to {latest_experience['end_time']}.
        I have {len(project)} projects which is related to my field.
        """
    elif mode == 'recommend-description':
        if not isinstance(resume, str):
            raise ValueError("The resume should be a string")
        description = resume
        return f"""
        I am look into jobs. I request the job to satisfy {description}.
        """
    elif mode == 'rank-candidates':
        id = resume['id']
        user_id = resume['user_id']
        name = resume['name']
        gender = 'male' if resume['gender'] == 1 else 'female'
        phone = resume['phone']
        email = resume['email']
        wechat = resume['wechat']
        state = player_status[resume['state'] - status_bias]
        description = resume['description']
        education = resume['education']
        experience = resume['experience']
        project = resume['project']
    
        if education is not None and education != []:
            highest_education = sorted(education, key=lambda x: x['degree'], reverse=True)[0]
            highest_degree = degree_names[highest_education['degree'] - education_bias]
        else:
            highest_education = None
            highest_degree = "Unknown"
            education = []
        
        if experience is not None and experience != []:
            latest_experience = sorted(experience, key=lambda x: x['end_time'], reverse=True)[0]
        else:
            latest_experience = {
                'position': 'Unknown',
                'company': 'Unknown',
                'start_time': 'Unknown',
                'end_time': 'Unknown'
            }
            experience = []
        
        if project is not None and project != []:
            pass
        else:
            project = []
        
        heorshe = 'he' if gender == 'male' else 'she'
        himselfherself = 'himself' if gender == 'male' else 'herself'
        hisher = 'his' if gender == 'male' else 'her'
        
        return f"""
        This is one of the candidates to be considered by the company, please consider the job description and the resume,
        rate the candidate by 1-100, 100 is the best match, 1 is the worst match. Just answer one number as score.
        {hisher} name is {name}, gender is {gender}, and the candidate {state}. {heorshe} could describe {himselfherself} as {description}.
        {hisher} highest degree is {highest_degree}, and have {len(experience)} work experiences.
        For {hisher} last job, {heorshe} worked as {latest_experience['position']} at {latest_experience['company']} from {latest_experience['start_time']} to {latest_experience['end_time']}.
        {heorshe} have {len(project)} projects which is related to {hisher} field.
        """
        
    