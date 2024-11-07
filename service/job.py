allowing_modes = ['recommend-resume', 'recommend-description', 'rank-candidates']

def describe_job(position, mode):
    assert mode in allowing_modes
    id = position['id']
    title = position['title']
    description = position['description']
    demand = position['demand']
    location = position['location']
    salary = position['salary']
    company = position['company']
    # created = position['create_at']
    job_type = position['job_type']
    owner_id = position['owner_id']
    if mode in ['recommend-resume', 'recommend-description']:
        return f"""
        In the following is one of the jobs to be considered, its id is {id}, please consider the job description and my resume,
        rate this job by 1-100, 100 is the best match, 1 is the worst match. Just answer one number as score.
        The job title is {title}, and can be described as {description}, and the work location is {location}.
        The company requires {demand}. While the salary is {salary} RMB per month, the company name is {company}.
        """
    elif mode == 'rank-candidates':
        return f"""
        This is one of the candidates to be considered by the company, please consider the job description and the resume,
        rate the candidate by 1-100, 100 is the best match, 1 is the worst match. Just answer one number as score.
        The job title is {title}, and can be described as {description}, and the work location is {location}.
        The company requires {demand}. While the salary is {salary} RMB per month, the company name is {company}.
        """


def describe_player(resume, mode):
    assert mode in allowing_modes
    raise NotImplementedError