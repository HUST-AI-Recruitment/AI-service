def describe_job(position):
    id = position['id']
    title = position['title']
    description = position['description']
    location = position['location']
    salary = position['salary']
    company = position['company_name']
    created = position['create_at']
    return f"""
    This is one of the jobs to be considered, please consider the job description and the resume file,
    rate this job by 1-100, 100 is the best match, 1 is the worst match. Just answer one number as score.
    The job title is {title}, the company requires {description}, and the work location is {location}.
    The salary is {salary} RMB per month, the company name is {company}.
    """

